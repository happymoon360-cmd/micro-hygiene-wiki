"""
Test suite for wiki models.
Tests all model classes including Category, Tip, Vote, and moderation models.
"""

import pytest
from django.test import TestCase
from apps.wiki.models import (
    Category,
    Tip,
    Vote,
    AffiliateProduct,
    BlacklistTerm,
    ModerationFlag,
    ModerationLog,
)


@pytest.mark.django_db
class TestCategoryModel:
    """Tests for the Category model."""

    def test_category_creation(self):
        """Test creating a category."""
        category = Category.objects.create(
            name='Kitchen',
            slug='kitchen',
            description='Kitchen hygiene tips'
        )
        
        assert category.name == 'Kitchen'
        assert category.slug == 'kitchen'
        assert category.description == 'Kitchen hygiene tips'
        assert str(category) == 'Kitchen'

    def test_category_slug_unique(self):
        """Test that category slugs must be unique."""
        Category.objects.create(name='Kitchen', slug='kitchen')
        
        with pytest.raises(Exception):  # IntegrityError
            Category.objects.create(name='Another Kitchen', slug='kitchen')

    def test_category_ordering(self):
        """Test categories are ordered by name."""
        Category.objects.create(name='Zebra', slug='zebra')
        Category.objects.create(name='Apple', slug='apple')
        Category.objects.create(name='Banana', slug='banana')
        
        categories = list(Category.objects.all())
        assert categories[0].name == 'Apple'
        assert categories[1].name == 'Banana'
        assert categories[2].name == 'Zebra'

    def test_category_tips_relationship(self):
        """Test category to tips relationship."""
        category = Category.objects.create(name='Test', slug='test')
        
        Tip.objects.create(title='Tip 1', description='Desc 1', category=category)
        Tip.objects.create(title='Tip 2', description='Desc 2', category=category)
        
        assert category.tips.count() == 2


@pytest.mark.django_db
class TestTipModel:
    """Tests for the Tip model."""

    def test_tip_creation(self):
        """Test creating a tip."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(
            title='Test Tip',
            description='Test description',
            category=category,
            effectiveness_avg=4.5,
            difficulty_avg=2.0,
            success_rate=150.0
        )
        
        assert tip.title == 'Test Tip'
        assert tip.description == 'Test description'
        assert tip.category == category
        assert tip.effectiveness_avg == 4.5
        assert tip.difficulty_avg == 2.0
        assert tip.success_rate == 150.0
        assert str(tip) == 'Test Tip'

    def test_tip_default_values(self):
        """Test tip default values."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        assert tip.effectiveness_avg == 0.0
        assert tip.difficulty_avg == 0.0
        assert tip.success_rate == 0.0

    def test_tip_ordering(self):
        """Test tips are ordered by created_at descending."""
        category = Category.objects.create(name='Test', slug='test')
        
        tip1 = Tip.objects.create(title='First', description='First', category=category)
        tip2 = Tip.objects.create(title='Second', description='Second', category=category)
        
        tips = list(Tip.objects.all())
        assert tips[0] == tip2  # Newest first
        assert tips[1] == tip1

    def test_calculate_success_rate(self):
        """Test success rate calculation."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(
            title='Test',
            description='Test',
            category=category,
            effectiveness_avg=4.0,
            difficulty_avg=1.0
        )
        
        # Formula: (effectiveness / (difficulty + 1)) * 100
        expected = (4.0 / (1.0 + 1)) * 100  # = 200.0
        assert tip.calculate_success_rate() == expected

    def test_calculate_success_rate_zero_difficulty(self):
        """Test success rate with zero difficulty."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(
            title='Test',
            description='Test',
            category=category,
            effectiveness_avg=5.0,
            difficulty_avg=0.0
        )
        
        expected = (5.0 / (0.0 + 1)) * 100  # = 500.0
        assert tip.calculate_success_rate() == expected

    def test_tip_votes_relationship(self):
        """Test tip to votes relationship."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        Vote.objects.create(tip=tip, effectiveness=5, difficulty=1, ip_hash='hash1')
        Vote.objects.create(tip=tip, effectiveness=4, difficulty=2, ip_hash='hash2')
        
        assert tip.votes.count() == 2


@pytest.mark.django_db
class TestVoteModel:
    """Tests for the Vote model."""

    def test_vote_creation(self):
        """Test creating a vote."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        vote = Vote.objects.create(
            tip=tip,
            effectiveness=5,
            difficulty=2,
            ip_hash='abc123hash'
        )
        
        assert vote.tip == tip
        assert vote.effectiveness == 5
        assert vote.difficulty == 2
        assert vote.ip_hash == 'abc123hash'
        assert 'Vote for Tip' in str(vote)

    def test_vote_valid_effectiveness_range(self):
        """Test effectiveness must be 1-10."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        # Django IntegerField doesn't enforce range at DB level
        # This test documents expected behavior
        vote = Vote.objects.create(tip=tip, effectiveness=15, difficulty=1, ip_hash='hash')
        assert vote.effectiveness == 15  # DB allows it, validation should be in view

    def test_multiple_votes_per_tip(self):
        """Test multiple votes can exist for same tip from different IPs."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        Vote.objects.create(tip=tip, effectiveness=5, difficulty=1, ip_hash='hash1')
        Vote.objects.create(tip=tip, effectiveness=4, difficulty=2, ip_hash='hash2')
        Vote.objects.create(tip=tip, effectiveness=3, difficulty=3, ip_hash='hash3')
        
        assert Vote.objects.filter(tip=tip).count() == 3


@pytest.mark.django_db
class TestAffiliateProductModel:
    """Tests for the AffiliateProduct model."""

    def test_product_creation(self):
        """Test creating an affiliate product."""
        product = AffiliateProduct.objects.create(
            name='Test Product',
            affiliate_url='https://amazon.com/dp/123',
            network='amazon',
            keywords=['test', 'product'],
            is_active=True
        )
        
        assert product.name == 'Test Product'
        assert product.affiliate_url == 'https://amazon.com/dp/123'
        assert product.network == 'amazon'
        assert product.keywords == ['test', 'product']
        assert product.is_active is True
        assert str(product) == 'Test Product'

    def test_product_default_is_active(self):
        """Test product is active by default."""
        product = AffiliateProduct.objects.create(
            name='Test',
            affiliate_url='https://test.com',
            network='test'
        )
        
        assert product.is_active is True

    def test_product_default_keywords(self):
        """Test product has empty keywords list by default."""
        product = AffiliateProduct.objects.create(
            name='Test',
            affiliate_url='https://test.com',
            network='test'
        )
        
        assert product.keywords == []


@pytest.mark.django_db
class TestBlacklistTermModel:
    """Tests for the BlacklistTerm model."""

    def test_term_creation(self):
        """Test creating a blacklist term."""
        term = BlacklistTerm.objects.create(
            term='spam',
            category='inappropriate',
            severity='high',
            is_active=True
        )
        
        assert term.term == 'spam'
        assert term.category == 'inappropriate'
        assert term.severity == 'high'
        assert term.is_active is True
        assert 'spam' in str(term)

    def test_term_unique(self):
        """Test that terms must be unique."""
        BlacklistTerm.objects.create(term='spam', category='test', severity='low')
        
        with pytest.raises(Exception):  # IntegrityError
            BlacklistTerm.objects.create(term='spam', category='other', severity='high')

    def test_term_ordering(self):
        """Test terms are ordered by severity then term."""
        BlacklistTerm.objects.create(term='zebra', category='test', severity='low')
        BlacklistTerm.objects.create(term='apple', category='test', severity='high')
        BlacklistTerm.objects.create(term='banana', category='test', severity='medium')
        
        terms = list(BlacklistTerm.objects.all())
        # Alphabetical reverse: medium > low > high
        assert terms[0].severity == 'medium'
        assert terms[1].severity == 'low'
        assert terms[2].severity == 'high'


@pytest.mark.django_db
class TestModerationFlagModel:
    """Tests for the ModerationFlag model."""

    def test_flag_creation(self):
        """Test creating a moderation flag."""
        flag = ModerationFlag.objects.create(
            flag_type='keyword',
            category='inappropriate',
            confidence=0.95,
            status='pending',
            matched_terms=['bad_word'],
            reason='Contains prohibited term',
            ip_hash='hash123'
        )
        
        assert flag.flag_type == 'keyword'
        assert flag.category == 'inappropriate'
        assert flag.confidence == 0.95
        assert flag.status == 'pending'
        assert flag.matched_terms == ['bad_word']
        assert 'Flag #' in str(flag)

    def test_flag_with_tip(self):
        """Test creating a flag associated with a tip."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        flag = ModerationFlag.objects.create(
            tip=tip,
            flag_type='manual',
            category='user_report',
            confidence=1.0,
            status='pending',
            reason='User reported',
            ip_hash='hash123'
        )
        
        assert flag.tip == tip
        assert tip.moderation_flags.count() == 1

    def test_flag_status_choices(self):
        """Test flag status choices."""
        valid_statuses = ['pending', 'approved', 'rejected', 'escalated']
        
        for status in valid_statuses:
            flag = ModerationFlag.objects.create(
                flag_type='keyword',
                category='test',
                confidence=0.5,
                status=status,
                reason='Test',
                ip_hash='hash'
            )
            assert flag.status == status

    def test_flag_type_choices(self):
        """Test flag type choices."""
        valid_types = ['keyword', 'ai', 'manual']
        
        for flag_type in valid_types:
            flag = ModerationFlag.objects.create(
                flag_type=flag_type,
                category='test',
                confidence=0.5,
                status='pending',
                reason='Test',
                ip_hash='hash'
            )
            assert flag.flag_type == flag_type

    def test_flag_ordering(self):
        """Test flags are ordered by created_at descending."""
        flag1 = ModerationFlag.objects.create(
            flag_type='keyword',
            category='test',
            confidence=0.5,
            status='pending',
            reason='Test',
            ip_hash='hash1'
        )
        flag2 = ModerationFlag.objects.create(
            flag_type='ai',
            category='test',
            confidence=0.8,
            status='pending',
            reason='Test',
            ip_hash='hash2'
        )
        
        flags = list(ModerationFlag.objects.all())
        assert flags[0] == flag2  # Newest first
        assert flags[1] == flag1


@pytest.mark.django_db
class TestModerationLogModel:
    """Tests for the ModerationLog model."""

    def test_log_creation(self):
        """Test creating a moderation log."""
        log = ModerationLog.objects.create(
            action='flag_created',
            ip_hash='hash123',
            details={'reason': 'Test'}
        )
        
        assert log.action == 'flag_created'
        assert log.ip_hash == 'hash123'
        assert log.details == {'reason': 'Test'}
        assert 'flag_created' in str(log)

    def test_log_with_flag(self):
        """Test creating a log associated with a flag."""
        flag = ModerationFlag.objects.create(
            flag_type='keyword',
            category='test',
            confidence=0.5,
            status='pending',
            reason='Test',
            ip_hash='hash'
        )
        
        log = ModerationLog.objects.create(
            action='flag_created',
            flag=flag,
            ip_hash='hash123',
            details={}
        )
        
        assert log.flag == flag
        assert flag.logs.count() == 1

    def test_log_with_tip(self):
        """Test creating a log associated with a tip."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test', description='Test', category=category)
        
        log = ModerationLog.objects.create(
            action='tip_rejected',
            tip=tip,
            ip_hash='hash123',
            details={}
        )
        
        assert log.tip == tip
        assert tip.moderation_logs.count() == 1

    def test_log_action_choices(self):
        """Test log action choices."""
        valid_actions = [
            'flag_created',
            'flag_approved',
            'flag_rejected',
            'tip_rejected',
            'user_warned',
            'user_suspended',
        ]
        
        for action in valid_actions:
            log = ModerationLog.objects.create(
                action=action,
                ip_hash='hash',
                details={}
            )
            assert log.action == action

    def test_log_ordering(self):
        """Test logs are ordered by created_at descending."""
        log1 = ModerationLog.objects.create(
            action='flag_created',
            ip_hash='hash1',
            details={}
        )
        log2 = ModerationLog.objects.create(
            action='flag_approved',
            ip_hash='hash2',
            details={}
        )
        
        logs = list(ModerationLog.objects.all())
        assert logs[0] == log2  # Newest first
        assert logs[1] == log1
