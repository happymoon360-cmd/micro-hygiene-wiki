# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportUnknownArgumentType=false, reportAttributeAccessIssue=false, reportUnusedImport=false, reportDuplicateImport=false, reportImplicitOverride=false, reportUnreachable=false

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Tip, Vote, AffiliateProduct
from .serializers import (CategorySerializer, TipListSerializer, TipDetailSerializer,
                           CreateTipSerializer, VoteTipSerializer, FlagTipSerializer,
                           AffiliateProductSerializer)
from django.core.paginator import Paginator
import json


class TipListView(generics.ListAPIView):
    """List all tips with pagination"""
    queryset = Tip.objects.select_related('category').prefetch_related('votes').order_by('-created_at')
    serializer_class = TipListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page.object_list, many=True)
        return self.get_paginated_response(page, serializer.data)

    def paginate_queryset(self, queryset):
        paginator = Paginator(queryset, 20)
        page_number = self.request.query_params.get('page', 1)
        page_obj = paginator.page(page_number)
        return page_obj

    def get_paginated_response(self, data, results=None):
        return Response({
            'count': data.paginator.count,
            'total_pages': data.paginator.num_pages,
            'current_page': data.number,
            'next': data.next_page_number() if data.has_next() else None,
            'previous': data.previous_page_number() if data.has_previous() else None,
            'results': results if results is not None else data.object_list,
        })


class TipDetailView(generics.RetrieveAPIView):
    """Get detail view for a specific tip"""
    queryset = Tip.objects.select_related('category').prefetch_related('votes')
    serializer_class = TipDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'tip_id'


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
        serializer = TipListSerializer(tips, many=True)
        return Response({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'tips': serializer.data,
        })


class AffiliateProductList(generics.ListAPIView):
    """List all active affiliate products"""

    queryset = AffiliateProduct.objects.filter(is_active=True)
    serializer_class = AffiliateProductSerializer
    permission_classes = []  # Public access


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
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited
from django.utils import timezone
from .models import Tip, Vote, ModerationFlag, ModerationLog
from .utils import moderate_content
import hashlib
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


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


@api_view(['POST'])
def tip_vote(request, tip_id):
    """Handle voting on a tip. One vote per IP per tip."""
    try:
        tip = Tip.objects.get(id=tip_id)
    except Tip.DoesNotExist:
        return Response({"error": "Tip not found"}, status=404)

    try:
        data = (
            request.POST
            if request.content_type == "multipart/form-data"
            else request.GET
            if request.content_type == "application/x-www-form-urlencoded"
            else {}
        )
        if not data:
            data = json.loads(request.body)

        effectiveness = int(data.get("effectiveness") or 0)
        difficulty = int(data.get("difficulty") or 0)
    except (ValueError, TypeError, json.JSONDecodeError):
        return Response(
            {"error": "Invalid effectiveness or difficulty values"}, status=400
        )

    if effectiveness < 1 or effectiveness > 5:
        return Response(
            {"error": "Effectiveness must be between 1 and 5"}, status=400
        )

    if difficulty < 1 or difficulty > 5:
        return Response(
            {"error": "Difficulty must be between 1 and 5"}, status=400
        )

    ip = get_client_ip(request)
    ip_hash = hash_ip(ip)

    if Vote.objects.filter(tip=tip, ip_hash=ip_hash).exists():
        return Response({"error": "You have already voted on this tip"}, status=400)

    Vote.objects.create(
        tip=tip, effectiveness=effectiveness, difficulty=difficulty, ip_hash=ip_hash
    )

    votes = tip.votes.all()
    if votes.exists():
        tip.effectiveness_avg = sum(v.effectiveness for v in votes) / votes.count()
        tip.difficulty_avg = sum(v.difficulty for v in votes) / votes.count()
        tip.success_rate = tip.calculate_success_rate()
    tip.save()

    return Response(
        {
            "success": True,
            "message": "Vote recorded successfully",
            "effectiveness_avg": tip.effectiveness_avg,
            "difficulty_avg": tip.difficulty_avg,
            "success_rate": tip.success_rate,
        }
    )


@api_view(['POST'])
def create_tip(request):
    """
    Create a new tip with rate limiting (5 posts/hour per IP).
    Performs both keyword and AI moderation before saving.
    """
    if is_ratelimited(request, group="create_tip", increment=True):
            return Response(
                {"error": "Rate limit exceeded. Maximum 5 tips per hour."}, status=429
            )

    try:
        data = json.loads(request.body)

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        category_id = data.get("category_id")

        if not title or not description or not category_id:
            return Response(
                {"error": "Missing required fields: title, description, category_id"},
                status=400,
            )

        # Validate category early to avoid returning 500 for bad input.
        category = Category.objects.filter(id=category_id).first()
        if not category:
            return Response({"error": "Invalid category_id"}, status=400)

        # Verify Turnstile token
        turnstile_token = data.get("turnstile_token")
        if not turnstile_token and not settings.DEBUG:
            return Response({"error": "Turnstile token is required"}, status=400)

        if turnstile_token:
            try:
                import requests  # Lazy import prevents startup failure if dependency is missing.
            except ImportError:
                logger.exception("requests dependency is missing while verifying Turnstile.")
                return Response(
                    {"error": "CAPTCHA verification unavailable"}, status=503
                )

            verify_response = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': settings.TURNSTILE_SECRET_KEY,
                    'response': turnstile_token
                }
            )
            if not verify_response.json().get('success'):
                return Response({"error": "Invalid Turnstile token"}, status=403)

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

            return Response(
                {
                    "error": "Content violates community guidelines",
                    "reason": moderation_result["reason"],
                    "category": moderation_result["category"],
                },
                status=403,
            )

        tip = Tip.objects.create(title=title, description=description, category=category)

        return Response(
            {
                "success": True,
                "tip_id": tip.id,
                "title": tip.title,
                "message": "Tip created successfully",
            },
            status=201,
        )

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)
    except Exception:
        logger.exception("Unexpected error while creating tip.")
        return Response({"error": "Internal server error"}, status=500)


@api_view(['POST'])
def flag_content(request, tip_id):
    """
    Flag content for moderation (20 flags/day per IP).
    Used by users to report inappropriate content.
    """
    if is_ratelimited(request, group="flag_content", increment=True):
            return Response(
                {"error": "Rate limit exceeded. Maximum 20 flags per day."}, status=429
            )

    try:
        data = json.loads(request.body)
        reason = data.get("reason", "").strip()

        if not reason:
            return Response(
                {"error": "Missing required field: reason"}, status=400
            )

        try:
            tip = Tip.objects.get(id=tip_id)
        except Tip.DoesNotExist:
            return Response({"error": "Tip not found"}, status=404)

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

        return Response(
            {"success": True, "message": "Flag created successfully"}, status=201
        )

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=400)
    except Exception:
        logger.exception("Unexpected error while flagging content.")
        return Response({"error": "Internal server error"}, status=500)
