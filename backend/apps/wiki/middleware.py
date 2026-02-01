import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.cache import cache
from django.utils import timezone


def get_client_ip(request: HttpRequest) -> str:
    """
    Extract client IP address from request, handling X-Forwarded-For headers.
    Returns the IP as a string.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "127.0.0.1")
    return ip


def hash_ip_address(ip_address: str) -> str:
    """
    Hash IP address for GDPR compliance using SHA-256.
    Returns a hexadecimal string representation.
    """
    # Use SECRET_KEY as salt for additional security
    salt = getattr(settings, "SECRET_KEY", "").encode("utf-8")
    ip_bytes = ip_address.encode("utf-8")

    # Create hash with salt
    hash_obj = hashlib.sha256(salt + ip_bytes)
    return hash_obj.hexdigest()


def load_blacklist_terms() -> Dict[str, Any]:
    """
    Load prohibited keyword terms from JSON fixture file.
    Returns dictionary with terms and their metadata.
    """
    # Try to load from fixtures directory
    fixture_path = os.path.join(
        settings.BASE_DIR, "apps", "wiki", "fixtures", "keyword_blacklist.json"
    )

    try:
        with open(fixture_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Convert list of terms to dictionary for quick lookup
            term_dict = {}
            for field in data.get("fields", []):
                term_dict[field["term"].lower()] = {
                    "category": field.get("category", "self_harm"),
                    "severity": field.get("severity", "medium"),
                }
            return term_dict
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # Return default hardcoded list as fallback
        default_terms = {
            "cut": {"category": "self_harm", "severity": "high"},
            "needle": {"category": "self_harm", "severity": "high"},
            "knife": {"category": "self_harm", "severity": "high"},
            "bleed": {"category": "self_harm", "severity": "high"},
            "overdose": {"category": "self_harm", "severity": "high"},
            "suicide": {"category": "self_harm", "severity": "high"},
            "kill myself": {"category": "self_harm", "severity": "high"},
            "self harm": {"category": "self_harm", "severity": "high"},
        }
        return default_terms


def check_forbidden_keywords(text: str, blacklist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check text for prohibited keywords.
    Returns dictionary with violation status and matched terms.
    """
    text_lower = text.lower()
    matched_terms = []

    for term, metadata in blacklist.items():
        if term in text_lower:
            matched_terms.append(
                {
                    "term": term,
                    "category": metadata["category"],
                    "severity": metadata["severity"],
                }
            )

    return {
        "has_violation": len(matched_terms) > 0,
        "matched_terms": matched_terms,
        "severity": "high"
        if any(t["severity"] == "high" for t in matched_terms)
        else "medium",
    }


def cleanup_old_ip_hashes() -> int:
    """
    Remove IP hashes older than 7 days from cache.
    Returns count of removed entries.
    """
    removed_count = 0
    cache_key_prefix = "ip_hash_timestamp_"

    # In production, this should use a proper cache backend with iteration support
    # For now, this is a placeholder for cleanup logic
    # Actual implementation depends on cache backend (Redis, Memcached, etc.)

    return removed_count


class ContentModerationMiddleware:
    """
    Middleware for content moderation including:
    - Keyword blacklist filtering
    - IP address hashing for GDPR compliance
    - Rate limiting enforcement
    - Automatic flagging of policy violations
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist = load_blacklist_terms()
        self.ip_retention_days = getattr(settings, "IP_HASH_RETENTION_DAYS", 7)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process incoming request for content moderation.
        """
        # Extract and hash IP address
        client_ip = get_client_ip(request)
        hashed_ip = hash_ip_address(client_ip)

        # Store hashed IP in request for later use
        request.hashed_ip = hashed_ip
        request.client_ip = client_ip  # Keep original for rate limiting

        # Log IP hash with timestamp for retention tracking
        self._log_ip_hash(hashed_ip)

        # Process request through middleware chain
        response = self.get_response(request)

        return response

    def _log_ip_hash(self, hashed_ip: str) -> None:
        """
        Log IP hash with timestamp for GDPR retention tracking.
        """
        cache_key = f"ip_hash_timestamp_{hashed_ip}"
        cache.set(cache_key, timezone.now().isoformat(), self.ip_retention_days * 86400)

    @classmethod
    def moderate_content(cls, text: str) -> Dict[str, Any]:
        """
        Moderate content using keyword blacklist.
        Returns moderation result with violation details.
        """
        blacklist = load_blacklist_terms()
        return check_forbidden_keywords(text, blacklist)

    @classmethod
    def get_user_ip_hash(cls, request: HttpRequest) -> str:
        """
        Get hashed IP address for request.
        """
        if hasattr(request, "hashed_ip"):
            return request.hashed_ip

        return hash_ip_address(get_client_ip(request))

    @classmethod
    def check_rate_limit(
        cls, request: HttpRequest, action: str, limit: int, period: str
    ) -> bool:
        """
        Check if user has exceeded rate limit for specific action.
        Returns True if allowed, False if limit exceeded.
        """
        hashed_ip = cls.get_user_ip_hash(request)
        cache_key = f"ratelimit_{action}_{hashed_ip}"

        current_count = cache.get(cache_key, 0)

        if current_count >= limit:
            return False

        # Increment counter
        new_count = (
            cache.incr(cache_key)
            if cache.get(cache_key) is not None
            else cache.set(cache_key, 1, cls._get_period_seconds(period))
        )
        return new_count <= limit

    @staticmethod
    def _get_period_seconds(period: str) -> int:
        """
        Convert period string to seconds.
        """
        period_map = {
            "hour": 3600,
            "day": 86400,
            "week": 604800,
        }
        return period_map.get(period, 3600)


# Export utility functions for use in views and serializers
__all__ = [
    "ContentModerationMiddleware",
    "get_client_ip",
    "hash_ip_address",
    "load_blacklist_terms",
    "check_forbidden_keywords",
    "cleanup_old_ip_hashes",
]
