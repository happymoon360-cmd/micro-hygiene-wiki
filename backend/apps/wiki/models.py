from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AffiliateProduct(models.Model):
    name = models.CharField(max_length=255)
    affiliate_url = models.URLField()
    network = models.CharField(max_length=100)
    keywords = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Affiliate Product"
        verbose_name_plural = "Affiliate Products"

    def __str__(self):
        return self.name


class Tip(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tips"
    )
    effectiveness_avg = models.FloatField(default=0.0)
    difficulty_avg = models.FloatField(default=0.0)
    success_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tip"
        verbose_name_plural = "Tips"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) if not self.slug else self.slug
        super().save(*args, **kwargs)

    def calculate_success_rate(self):
        """Calculate success rate: avg_effectiveness / (avg_difficulty + 1) * 100"""
        return (self.effectiveness_avg / (self.difficulty_avg + 1)) * 100


class Vote(models.Model):
    tip = models.ForeignKey("Tip", on_delete=models.CASCADE, related_name="votes")
    effectiveness = models.IntegerField()
    difficulty = models.IntegerField()
    ip_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"Vote for Tip {self.tip_id} - IP: {self.ip_hash}"


class BlacklistTerm(models.Model):
    term = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=50)
    severity = models.CharField(
        max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Blacklist Term"
        verbose_name_plural = "Blacklist Terms"
        ordering = ["-severity", "term"]

    def __str__(self):
        return f"{self.term} ({self.severity})"


class ModerationFlag(models.Model):
    FLAG_TYPES = [
        ("keyword", "Keyword Match"),
        ("ai", "AI Detection"),
        ("manual", "Manual Review"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("escalated", "Escalated"),
    ]

    tip = models.ForeignKey(
        Tip,
        on_delete=models.CASCADE,
        related_name="moderation_flags",
        null=True,
        blank=True,
    )
    flag_type = models.CharField(max_length=20, choices=FLAG_TYPES)
    category = models.CharField(max_length=50)
    confidence = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    matched_terms = models.JSONField(default=list)
    reason = models.TextField(blank=True)
    ip_hash = models.CharField(max_length=255)
    reviewed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_flags",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Moderation Flag"
        verbose_name_plural = "Moderation Flags"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["flag_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Flag #{self.id} - {self.flag_type} - {self.status}"


class ModerationLog(models.Model):
    ACTION_TYPES = [
        ("flag_created", "Flag Created"),
        ("flag_approved", "Flag Approved"),
        ("flag_rejected", "Flag Rejected"),
        ("tip_rejected", "Tip Rejected"),
        ("user_warned", "User Warned"),
        ("user_suspended", "User Suspended"),
    ]

    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    flag = models.ForeignKey(
        ModerationFlag,
        on_delete=models.CASCADE,
        related_name="logs",
        null=True,
        blank=True,
    )
    tip = models.ForeignKey(
        Tip,
        on_delete=models.CASCADE,
        related_name="moderation_logs",
        null=True,
        blank=True,
    )
    ip_hash = models.CharField(max_length=255)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Moderation Log"
        verbose_name_plural = "Moderation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["ip_hash"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
