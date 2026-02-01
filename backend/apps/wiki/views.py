import hashlib
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited
from django.utils import timezone
from .models import Tip, Vote, ModerationFlag, ModerationLog
from .utils import moderate_content


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
            import json

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
@ratelimit(key="ip", rate="5/h", method="POST")
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
        import json

        data = json.loads(request.body)

        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        category_id = data.get("category_id")

        if not title or not description or not category_id:
            return JsonResponse(
                {"error": "Missing required fields: title, description, category_id"},
                status=400,
            )

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
@ratelimit(key="ip", rate="20/d", method="POST")
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
        import json

        data = json.loads(request.body)

        tip_id = data.get("tip_id")
        reason = data.get("reason", "User reported content").strip()

        if not tip_id:
            return JsonResponse({"error": "Missing tip_id"}, status=400)

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
            tip=tip,
            ip_hash=ip_hash,
            details={"flag_type": flag.flag_type, "reason": flag.reason},
        )

        return JsonResponse(
            {
                "success": True,
                "flag_id": flag.id,
                "message": "Content flagged successfully",
            },
            status=201,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_moderation_stats(request):
    """
    Get moderation statistics for admin dashboard.
    """
    try:
        total_flags = ModerationFlag.objects.count()
        pending_flags = ModerationFlag.objects.filter(status="pending").count()
        approved_flags = ModerationFlag.objects.filter(status="approved").count()
        rejected_flags = ModerationFlag.objects.filter(status="rejected").count()

        by_category = {}
        for flag in ModerationFlag.objects.all():
            category = flag.category
            by_category[category] = by_category.get(category, 0) + 1

        return JsonResponse(
            {
                "total_flags": total_flags,
                "pending_flags": pending_flags,
                "approved_flags": approved_flags,
                "rejected_flags": rejected_flags,
                "by_category": by_category,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def review_flag(request):
    """
    Review a moderation flag (admin only).
    Approve or reject a flag and take appropriate action.
    """
    try:
        import json

        data = json.loads(request.body)

        flag_id = data.get("flag_id")
        status = data.get("status")
        action = data.get("action", "none")

        if not flag_id or status not in ["approved", "rejected"]:
            return JsonResponse(
                {"error": "Missing or invalid flag_id or status"}, status=400
            )

        try:
            flag = ModerationFlag.objects.get(id=flag_id)
        except ModerationFlag.DoesNotExist:
            return JsonResponse({"error": "Flag not found"}, status=404)

        flag.status = status
        flag.reviewed_by = request.user if request.user.is_authenticated else None
        flag.reviewed_at = timezone.now()
        flag.save()

        ModerationLog.objects.create(
            action=f"flag_{status}",
            flag=flag,
            tip=flag.tip,
            ip_hash=flag.ip_hash,
            details={
                "reviewed_by": flag.reviewed_by.username
                if flag.reviewed_by
                else "Anonymous",
                "action_taken": action,
            },
        )

        if status == "approved" and flag.tip:
            if action == "delete_tip":
                tip_title = flag.tip.title
                flag.tip.delete()
                ModerationLog.objects.create(
                    action="tip_rejected",
                    flag=flag,
                    ip_hash=flag.ip_hash,
                    details={"deleted_tip_title": tip_title},
                )
            elif action == "warn_user":
                ModerationLog.objects.create(
                    action="user_warned",
                    flag=flag,
                    ip_hash=flag.ip_hash,
                    details={"warning_sent": True},
                )

        return JsonResponse(
            {
                "success": True,
                "flag_id": flag.id,
                "status": flag.status,
                "message": f"Flag {status} successfully",
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
