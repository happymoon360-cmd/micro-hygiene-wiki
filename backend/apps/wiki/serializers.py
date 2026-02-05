from rest_framework import serializers
from .models import (
    Category,
    Tip,
    Vote,
    AffiliateProduct,
    BlacklistTerm,
    ModerationFlag,
    ModerationLog,
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model with tips count"""

    tips_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "tips_count"]
        read_only_fields = ["id"]

    def get_tips_count(self, obj):
        """Return count of published tips in this category"""
        return obj.tips.count()


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for Vote model"""

    class Meta:
        model = Vote
        fields = ["id", "effectiveness", "difficulty", "ip_hash", "created_at"]
        read_only_fields = ["id", "ip_hash", "created_at"]


class AffiliateProductSerializer(serializers.ModelSerializer):
    """Serializer for Affiliate Product model"""

    class Meta:
        model = AffiliateProduct
        fields = ["id", "name", "affiliate_url", "network", "keywords", "is_active"]


class TipListSerializer(serializers.ModelSerializer):
    """Optimized list serializer for tips - minimal data"""

    category_name = serializers.CharField(source="category.name", read_only=True)
    vote_score = serializers.SerializerMethodField()

    class Meta:
        model = Tip
        fields = [
            "id",
            "title",
            "slug",
            "category_name",
            "effectiveness_avg",
            "difficulty_avg",
            "success_rate",
            "created_at",
        ]

    def get_vote_score(self, obj):
        """Calculate vote score: avg_effectiveness * votes"""
        vote_count = obj.votes.count()
        return round(obj.effectiveness_avg * vote_count, 1) if vote_count > 0 else 0


class TipDetailSerializer(serializers.ModelSerializer):
    """Detail serializer for tip with full nested relationships"""

    category = CategorySerializer(read_only=True)
    votes = VoteSerializer(many=True, read_only=True)
    vote_count = serializers.SerializerMethodField()
    vote_score = serializers.SerializerMethodField()

    class Meta:
        model = Tip
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "category",
            "votes",
            "vote_count",
            "vote_score",
            "effectiveness_avg",
            "difficulty_avg",
            "success_rate",
            "created_at",
        ]
        read_only_fields = ["id", "vote_count", "created_at", "votes"]

    def get_vote_count(self, obj):
        return obj.votes.count()

    def get_vote_score(self, obj):
        vote_count = obj.votes.count()
        return round(obj.effectiveness_avg * vote_count, 1) if vote_count > 0 else 0


class CreateTipSerializer(serializers.Serializer):
    """Custom serializer for tip creation"""

    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    category_id = serializers.IntegerField(required=True)
    turnstile_token = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ["title", "description", "category_id", "turnstile_token"]

    def validate_title(self, value):
        """Validate title is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        """Validate description is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value


class VoteTipSerializer(serializers.Serializer):
    """Custom serializer for voting on a tip"""

    effectiveness = serializers.IntegerField(min_value=1, max_value=5, required=True)
    difficulty = serializers.IntegerField(min_value=1, max_value=5, required=True)

    class Meta:
        fields = ["effectiveness", "difficulty"]


class FlagTipSerializer(serializers.Serializer):
    """Custom serializer for flagging a tip"""

    tip_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=True)

    class Meta:
        fields = ["tip_id", "reason"]
