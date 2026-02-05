from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Tip, Vote
from .serializers import (CategorySerializer, TipListSerializer, TipDetailSerializer,
                           CreateTipSerializer, VoteTipSerializer, FlagTipSerializer)
from django.core.paginator import Paginator


class TipListView(generics.ListAPIView):
    """List all tips with pagination"""
    queryset = Tip.objects.select_related('category').prefetch_related('votes').order_by('-created_at')
    serializer_class = TipListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer)

    def paginate_queryset(self, queryset):
        paginator = Paginator(queryset, 20)
        page_number = self.request.query_params.get('page', 1)
        page_obj = paginator.page(page_number)
        return page_obj

    def get_paginated_response(self, data):
        return Response({
            'count': data.paginator.count,
            'total_pages': data.paginator.num_pages,
            'current_page': data.number,
            'next': data.has_next() and data.next_page_number() else None,
            'previous': data.has_previous() and data.previous_page_number() else None,
            'results': data.object_list,
        })


class TipDetailView(generics.RetrieveAPIView):
    """Get detail view for a specific tip"""
    queryset = Tip.objects.select_related('category', 'votes')
    serializer_class = TipDetailSerializer
    lookup_field = 'id'


class CategoryListView(generics.ListAPIView):
    """List all categories with tips count"""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """Get category details with its tips"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        tips = Tip.objects.filter(category=category).select_related('category').order_by('-created_at')
        from rest_framework.pagination import LimitOffsetPagination
        paginator = LimitOffsetPagination()
        page = self.paginate_queryset(tips, LimitOffsetPagination())
        serializer = TipListSerializer(page.object_list, many=True)
        return Response({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'tips': serializer.data,
        })


@api_view(['GET'])
def search_tips(request):
    """Search tips by title or description"""
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=400)

    tips = Tip.objects.filter(
        title__icontains=query
    ).select_related('category').prefetch_related('votes')[:20]

    serializer = TipListSerializer(tips, many=True)
    return Response(serializer.data)


# Existing views (keep these)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited
from django.utils import timezone
from .models import Tip, Vote, ModerationFlag, ModerationLog
from .utils import moderate_content
import hashlib
import requests
from django.conf import settings


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def hash_ip(ip):
    """Hash IP address for privacy."""
    return hashlib.sha256(ip.encode()).hexdigest()


@csrf_exempt
@require_http_methods(["POST"])
def tip_vote(request, tip_id):
    """Handle voting on a tip. One vote per IP per tip."""
    try:
        tip = Tip.objects.get(id=tip_id)
    except Tip.DoesNotExist:
        return JsonResponse({"error": "Tip not found"}, status=404)

    try:
        data = (
            request.POST
            if request.content_type == "multipart/form-data"
            else request.GET
            if request.content_type == "application/x-www-form-urlencoded"
            else {}
        )
        if not data:
            import json as json

            data = json.loads(request.body)

        effectiveness = int(data.get("effectiveness"))
        difficulty = int(data.get("difficulty"))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Invalid effectiveness or difficulty values"}, status=400
        )

    if effectiveness < 1 or effectiveness > 10:
        return JsonResponse(
            {"error": "Effectiveness must be between 1 and 10"}, status=400
        )

    if difficulty < 1 or difficulty > 10:
        return JsonResponse(
            {"error": "Difficulty must be between 1 and 10"}, status=400
        )

    ip = get_client_ip(request)
    ip_hash = hash_ip(ip)

    if Vote.objects.filter(tip=tip, ip_hash=ip_hash).exists():
        return JsonResponse({"error": "You have already voted on this tip"}, status=400)

    Vote.objects.create(
        tip=tip, effectiveness=effectiveness, difficulty=difficulty, ip_hash=ip_hash
    )

    votes = tip.votes.all()
    if votes.exists():
        tip.effectiveness_avg = sum(v.effectiveness for v in votes) / votes.count()
        tip.difficulty_avg = sum(v.difficulty for v in votes) / votes.count()
        tip.success_rate = tip.calculate_success_rate()
    tip.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Vote recorded successfully",
            "effectiveness_avg": tip.effectiveness_avg,
            "difficulty_avg": tip.difficulty_avg,
            "success_rate": tip.success_rate,
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def create_tip(request):
    """
    Create a new tip with rate limiting (5 posts/hour per IP).
    Performs both keyword and AI moderation before saving.
    """
    if is_ratelimited(request, group="create_tip", increment=True):
        return JsonResponse(
            {"error": "Rate limit exceeded. Maximum 5 tips per hour."}, status=429
        )

    try:
        import json as json

        data = json.loads(request.body)

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        category_id = data.get("category_id")

        if not title or not description or not category_id:
            return JsonResponse(
                {"error": "Missing required fields: title, description, category_id"},
                status=400,
            )

        # Verify Turnstile token
        turnstile_token = data.get("turnstile_token")
        if not turnstile_token and not settings.DEBUG:
            return JsonResponse({"error": "Turnstile token is required"}, status=400)

        if turnstile_token:
            verify_response = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': settings.TURNSTILE_SECRET_KEY,
                    'response': turnstile_token
                }
            )
            if not verify_response.json().get('success'):
                return JsonResponse({"error": "Invalid Turnstile token"}, status=403)

        combined_text = f"{title} {description}"

        moderation_result = moderate_content(combined_text, use_ai=True)

        if moderation_result["is_flagged"]:
            ip_hash = hash_ip(get_client_ip(request))

            flag = ModerationFlag.objects.create(
                tip=None,
                flag_type="ai"
                if moderation_result.get("method") != "keyword"
                else "keyword",
                category=moderation_result["category"],
                confidence=moderation_result["confidence"],
                status="pending",
                matched_terms=moderation_result.get("all_scores", {}),
                reason=moderation_result["reason"],
                ip_hash=ip_hash,
            )

            ModerationLog.objects.create(
                action="flag_created",
                flag=flag,
                ip_hash=ip_hash,
                details={
                    "flag_type": flag.flag_type,
                    "category": flag.category,
                    "confidence": flag.confidence,
                    "reason": flag.reason,
                },
            )

            return JsonResponse(
                {
                    "error": "Content violates community guidelines",
                    "reason": moderation_result["reason"],
                    "category": moderation_result["category"],
                },
                status=403,
            )

        tip = Tip.objects.create(
            title=title, description=description, category_id=category_id
        )

        return JsonResponse(
            {
                "success": True,
                "tip_id": tip.id,
                "title": tip.title,
                "message": "Tip created successfully",
            },
            status=201,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def flag_content(request):
    """
    Flag content for moderation (20 flags/day per IP).
    Used by users to report inappropriate content.
    """
    if is_ratelimited(request, group="flag_content", increment=True):
        return JsonResponse(
            {"error": "Rate limit exceeded. Maximum 20 flags per day."}, status=429
        )

    try:
        import json as json

        data = json.loads(request.body)
        tip_id = data.get("tip_id")
        reason = data.get("reason", "").strip()

        if not tip_id or not reason:
            return JsonResponse(
                {"error": "Missing required fields: tip_id, reason"}, status=400
            )

        try:
            tip = Tip.objects.get(id=tip_id)
        except Tip.DoesNotExist:
            return JsonResponse({"error": "Tip not found"}, status=404)

        ip_hash = hash_ip(get_client_ip(request))

        flag = ModerationFlag.objects.create(
            tip=tip,
            flag_type="manual",
            category="user_report",
            confidence=1.0,
            status="pending",
            matched_terms=[],
            reason=reason,
            ip_hash=ip_hash,
        )

        ModerationLog.objects.create(
            action="flag_created",
            flag=flag,
            ip_hash=ip_hash,
            details={
                "flag_type": flag.flag_type,
                "category": flag.category,
                "confidence": flag.confidence,
                "reason": flag.reason,
            },
        )

        return JsonResponse(
            {"success": True, "message": "Flag created successfully"}, status=201
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
