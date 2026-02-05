"""
Test suite for wiki API endpoints.
Tests all REST API views including tips, categories, voting, and search.
"""

import json
import pytest
from django.urls import reverse
from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User
from apps.wiki.models import Category, Tip, Vote, ModerationFlag, BlacklistTerm


@pytest.mark.django_db
class TestTipListView:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the TipListView API endpoint."""

    def test_list_tips_empty(self, client):
        """Test listing tips when database is empty."""
        response = client.get('/api/tips/')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 0
        assert data['results'] == []
        assert data['total_pages'] == 0
        assert data['current_page'] == 1

    def test_list_tips_with_data(self, client):
        """Test listing tips with data in database."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        Tip.objects.create(
            title='Test Tip',
            description='Test description',
            category=category
        )
        
        response = client.get('/api/tips/')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 1
        assert len(data['results']) == 1
        assert data['results'][0]['title'] == 'Test Tip'

    def test_list_tips_pagination(self, client):
        """Test pagination works correctly."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        
        # Create 25 tips (more than page size of 20)
        for i in range(25):
            Tip.objects.create(
                title=f'Test Tip {i}',
                description=f'Description {i}',
                category=category
            )
        
        response = client.get('/api/tips/')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 25
        assert data['total_pages'] == 2
        assert data['current_page'] == 1
        assert len(data['results']) == 20
        assert data['next'] == 2
        assert data['previous'] is None

    def test_list_tips_second_page(self, client):
        """Test retrieving second page of results."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        
        for i in range(25):
            Tip.objects.create(
                title=f'Test Tip {i}',
                description=f'Description {i}',
                category=category
            )
        
        response = client.get('/api/tips/?page=2')
        assert response.status_code == 200
        data = response.json()
        assert data['current_page'] == 2
        assert len(data['results']) == 5
        assert data['next'] is None
        assert data['previous'] == 1

    def test_list_tips_ordering(self, client):
        """Test tips are ordered by created_at descending."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        
        tip1 = Tip.objects.create(title='First Tip', description='First', category=category)
        tip2 = Tip.objects.create(title='Second Tip', description='Second', category=category)
        
        response = client.get('/api/tips/')
        data = response.json()
        
        # Second tip should appear first (newest first)
        assert data['results'][0]['title'] == 'Second Tip'
        assert data['results'][1]['title'] == 'First Tip'


@pytest.mark.django_db
class TestTipDetailView:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the TipDetailView API endpoint."""

    def test_get_tip_detail_success(self, client):
        """Test retrieving a specific tip by ID."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        tip = Tip.objects.create(
            title='Test Tip',
            description='Test description',
            category=category,
            effectiveness_avg=4.5,
            difficulty_avg=2.0,
            success_rate=150.0
        )
        
        response = client.get(f'/api/tips/{tip.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'Test Tip'
        assert data['description'] == 'Test description'
        assert data['effectiveness_avg'] == 4.5
        assert data['difficulty_avg'] == 2.0
        assert data['success_rate'] == 150.0
        assert 'category' in data
        assert data['category']['name'] == 'Test Category'

    def test_get_tip_detail_not_found(self, client):
        """Test retrieving a non-existent tip returns 404."""
        response = client.get('/api/tips/99999/')
        assert response.status_code == 404

    def test_get_tip_detail_with_votes(self, client):
        """Test tip detail includes vote information."""
        category = Category.objects.create(name='Test Category', slug='test-category')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        Vote.objects.create(tip=tip, effectiveness=5, difficulty=1, ip_hash='hash1')
        Vote.objects.create(tip=tip, effectiveness=4, difficulty=2, ip_hash='hash2')
        
        response = client.get(f'/api/tips/{tip.id}/')
        assert response.status_code == 200
        data = response.json()
        assert 'votes' in data
        assert len(data['votes']) == 2
        assert data['vote_count'] == 2


@pytest.mark.django_db
class TestCategoryListView:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the CategoryListView API endpoint."""

    def test_list_categories_empty(self, client):
        """Test listing categories when database is empty."""
        response = client.get('/api/categories/')
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_categories_with_data(self, client):
        """Test listing categories with data."""
        Category.objects.create(name='Kitchen', slug='kitchen', description='Kitchen tips')
        Category.objects.create(name='Bathroom', slug='bathroom', description='Bathroom tips')
        
        response = client.get('/api/categories/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == 'Bathroom'  # Alphabetically sorted
        assert data[1]['name'] == 'Kitchen'

    def test_list_categories_includes_tips_count(self, client):
        """Test categories include tips_count field."""
        category = Category.objects.create(name='Test', slug='test')
        Tip.objects.create(title='Tip 1', description='Desc 1', category=category)
        Tip.objects.create(title='Tip 2', description='Desc 2', category=category)
        
        response = client.get('/api/categories/')
        data = response.json()
        assert data[0]['tips_count'] == 2


@pytest.mark.django_db
class TestCategoryDetailView:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the CategoryDetailView API endpoint."""

    def test_get_category_detail_success(self, client):
        """Test retrieving category details with tips."""
        category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test description'
        )
        Tip.objects.create(title='Tip 1', description='Desc 1', category=category)
        Tip.objects.create(title='Tip 2', description='Desc 2', category=category)
        
        response = client.get('/api/categories/test-category/')
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Test Category'
        assert data['slug'] == 'test-category'
        assert 'tips' in data
        assert len(data['tips']) == 2

    def test_get_category_detail_not_found(self, client):
        """Test retrieving non-existent category returns 404."""
        response = client.get('/api/categories/non-existent/')
        assert response.status_code == 404




@pytest.mark.django_db
class TestSearchTips:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the search_tips API endpoint."""

    def test_search_with_query(self, client):
        """Test searching tips with a query parameter."""
        category = Category.objects.create(name='Test', slug='test')
        Tip.objects.create(title='Kitchen Cleaning', description='How to clean', category=category)
        Tip.objects.create(title='Bathroom Tips', description='Shower cleaning', category=category)
        
        response = client.get('/api/tips/search/?q=Kitchen')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['title'] == 'Kitchen Cleaning'

    def test_search_no_query(self, client):
        """Test searching without query parameter returns error."""
        response = client.get('/api/tips/search/')
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data

    def test_search_case_insensitive(self, client):
        """Test search is case insensitive."""
        category = Category.objects.create(name='Test', slug='test')
        Tip.objects.create(title='KITCHEN Tips', description='Description', category=category)
        
        response = client.get('/api/tips/search/?q=kitchen')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_search_limit_20_results(self, client):
        """Test search returns maximum 20 results."""
        category = Category.objects.create(name='Test', slug='test')
        
        for i in range(25):
            Tip.objects.create(title=f'Test Tip {i}', description='Test', category=category)
        
        response = client.get('/api/tips/search/?q=Test')
        data = response.json()
        assert len(data) == 20


@pytest.mark.django_db
class TestTipVote:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the tip_vote API endpoint."""

    def test_vote_success(self, client):
        """Test successful voting on a tip."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        data = {
            'effectiveness': 5,
            'difficulty': 2
        }
        
        response = client.post(
            f'/api/tips/{tip.id}/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result['success'] is True
        assert result['effectiveness_avg'] == 5.0
        assert result['difficulty_avg'] == 2.0
        
        # Verify vote was created
        assert Vote.objects.filter(tip=tip).count() == 1

    def test_vote_duplicate_not_allowed(self, client):
        """Test that duplicate votes from same IP are not allowed."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        data = {'effectiveness': 5, 'difficulty': 2}
        
        # First vote
        client.post(
            f'/api/tips/{tip.id}/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Second vote from same IP (client maintains same IP in test)
        response = client.post(
            f'/api/tips/{tip.id}/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'already voted' in response.json()['error'].lower()

    def test_vote_invalid_effectiveness(self, client):
        """Test voting with invalid effectiveness value."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        data = {'effectiveness': 11, 'difficulty': 2}  # Invalid: > 10
        
        response = client.post(
            f'/api/tips/{tip.id}/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'effectiveness' in response.json()['error'].lower()

    def test_vote_invalid_difficulty(self, client):
        """Test voting with invalid difficulty value."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        data = {'effectiveness': 5, 'difficulty': 0}  # Invalid: < 1
        
        response = client.post(
            f'/api/tips/{tip.id}/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'difficulty' in response.json()['error'].lower()

    def test_vote_tip_not_found(self, client):
        """Test voting on non-existent tip returns 404."""
        data = {'effectiveness': 5, 'difficulty': 2}
        
        response = client.post(
            '/api/tips/99999/vote/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 404


@pytest.mark.django_db
class TestCreateTip:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False
        settings.DEBUG = True

    """Tests for the create_tip API endpoint."""

    def test_create_tip_success(self, client):
        """Test successfully creating a new tip."""
        category = Category.objects.create(name='Test', slug='test')
        
        data = {
            'title': 'New Tip',
            'description': 'This is a new tip description',
            'category_id': category.id
        }
        
        response = client.post(
            '/api/tips/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['success'] is True
        assert result['title'] == 'New Tip'
        assert 'tip_id' in result
        
        # Verify tip was created
        assert Tip.objects.filter(title='New Tip').exists()

    def test_create_tip_missing_fields(self, client):
        """Test creating tip with missing required fields."""
        data = {'title': 'New Tip'}  # Missing description and category_id
        
        response = client.post(
            '/api/tips/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'missing' in response.json()['error'].lower()

    def test_create_tip_empty_fields(self, client):
        """Test creating tip with empty fields."""
        category = Category.objects.create(name='Test', slug='test')
        
        data = {
            'title': '   ',  # Empty after strip
            'description': 'Description',
            'category_id': category.id
        }
        
        response = client.post(
            '/api/tips/create/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400

    def test_create_tip_invalid_json(self, client):
        """Test creating tip with invalid JSON."""
        response = client.post(
            '/api/tips/create/',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'invalid json' in response.json()['error'].lower()


@pytest.mark.django_db
class TestFlagContent:
    @pytest.fixture(autouse=True)
    def setup_settings(self, settings):
        settings.SECURE_SSL_REDIRECT = False

    """Tests for the flag_content API endpoint."""

    def test_flag_content_success(self, client):
        """Test successfully flagging content."""
        category = Category.objects.create(name='Test', slug='test')
        tip = Tip.objects.create(title='Test Tip', description='Test', category=category)
        
        data = {
            'tip_id': tip.id,
            'reason': 'Inappropriate content'
        }
        
        response = client.post(
            '/api/tips/flag/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result['success'] is True
        
        # Verify flag was created
        assert ModerationFlag.objects.filter(tip=tip).exists()

    def test_flag_content_missing_fields(self, client):
        """Test flagging with missing required fields."""
        data = {'tip_id': 1}  # Missing reason
        
        response = client.post(
            '/api/tips/flag/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'missing' in response.json()['error'].lower()

    def test_flag_content_tip_not_found(self, client):
        """Test flagging non-existent tip returns 404."""
        data = {
            'tip_id': 99999,
            'reason': 'Inappropriate content'
        }
        
        response = client.post(
            '/api/tips/flag/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
