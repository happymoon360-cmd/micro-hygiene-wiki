"""
Test suite for wiki utility functions.
Tests affiliate link generation, content moderation, and middleware utilities.
"""

import json
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, RequestFactory
from django.conf import settings

from apps.wiki.utils import (
    AffiliateLinkGenerator,
    get_affiliate_generator,
    generate_affiliate_link,
    convert_text_with_affiliate_links,
    moderate_content,
    get_moderation_summary,
    AIModerator,
)
from apps.wiki.middleware import (
    get_client_ip,
    hash_ip_address,
    load_blacklist_terms,
    check_forbidden_keywords,
    ContentModerationMiddleware,
)


class TestGetClientIP:
    """Tests for get_client_ip function."""

    def test_get_client_ip_from_x_forwarded_for(self):
        """Test extracting IP from X-Forwarded-For header."""
        request = Mock()
        request.META = {'HTTP_X_FORWARDED_FOR': '203.0.113.195, 70.41.3.18, 150.172.238.178'}
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.195'

    def test_get_client_ip_from_remote_addr(self):
        """Test extracting IP from REMOTE_ADDR when no X-Forwarded-For."""
        request = Mock()
        request.META = {'REMOTE_ADDR': '192.168.1.1'}
        
        ip = get_client_ip(request)
        assert ip == '192.168.1.1'

    def test_get_client_ip_strips_whitespace(self):
        """Test that IP is stripped of whitespace."""
        request = Mock()
        request.META = {'HTTP_X_FORWARDED_FOR': '  203.0.113.195  '}
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.195'


class TestHashIPAddress:
    """Tests for hash_ip_address function."""

    def test_hash_ip_address_consistency(self):
        """Test that same IP produces same hash."""
        ip = '192.168.1.1'
        hash1 = hash_ip_address(ip)
        hash2 = hash_ip_address(ip)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex length

    def test_hash_ip_address_different_ips(self):
        """Test that different IPs produce different hashes."""
        hash1 = hash_ip_address('192.168.1.1')
        hash2 = hash_ip_address('192.168.1.2')
        
        assert hash1 != hash2

    def test_hash_ip_address_uses_salt(self):
        """Test that hash uses SECRET_KEY as salt."""
        with patch.object(settings, 'SECRET_KEY', 'test-secret-key'):
            hash1 = hash_ip_address('192.168.1.1')
            
        with patch.object(settings, 'SECRET_KEY', 'different-secret'):
            hash2 = hash_ip_address('192.168.1.1')
        
        assert hash1 != hash2


class TestLoadBlacklistTerms:
    """Tests for load_blacklist_terms function."""

    def test_load_blacklist_returns_dict(self):
        """Test that blacklist is returned as dictionary."""
        blacklist = load_blacklist_terms()
        assert isinstance(blacklist, dict)

    def test_load_blacklist_has_default_terms(self):
        """Test that default terms exist as fallback."""
        # Mock file not found to trigger fallback
        with patch('builtins.open', side_effect=FileNotFoundError):
            blacklist = load_blacklist_terms()
        
        assert 'suicide' in blacklist
        assert 'self harm' in blacklist
        assert blacklist['suicide']['category'] == 'self_harm'

    def test_load_blacklist_from_file(self, tmp_path):
        """Test loading blacklist from JSON file."""
        fixture_data = {
            "fields": [
                {"term": "test_term", "category": "test_cat", "severity": "high"}
            ]
        }
        
        fixtures_dir = tmp_path / "apps" / "wiki" / "fixtures"
        fixtures_dir.mkdir(parents=True)
        fixture_file = fixtures_dir / "keyword_blacklist.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        with patch.object(settings, 'BASE_DIR', tmp_path):
            blacklist = load_blacklist_terms()
        
        assert 'test_term' in blacklist
        assert blacklist['test_term']['category'] == 'test_cat'


class TestCheckForbiddenKeywords:
    """Tests for check_forbidden_keywords function."""

    def test_no_violation_clean_text(self):
        """Test clean text has no violations."""
        blacklist = {'badword': {'category': 'inappropriate', 'severity': 'medium'}}
        text = "This is a clean text with no bad words"
        
        result = check_forbidden_keywords(text, blacklist)
        
        assert result['has_violation'] is False
        assert result['matched_terms'] == []

    def test_violation_found(self):
        """Test detecting forbidden keyword."""
        blacklist = {'badword': {'category': 'inappropriate', 'severity': 'high'}}
        text = "This text contains badword in it"
        
        result = check_forbidden_keywords(text, blacklist)
        
        assert result['has_violation'] is True
        assert len(result['matched_terms']) == 1
        assert result['matched_terms'][0]['term'] == 'badword'
        assert result['severity'] == 'high'

    def test_case_insensitive_matching(self):
        """Test matching is case insensitive."""
        blacklist = {'badword': {'category': 'test', 'severity': 'medium'}}
        text = "This contains BADWORD in uppercase"
        
        result = check_forbidden_keywords(text, blacklist)
        
        assert result['has_violation'] is True

    def test_multiple_violations(self):
        """Test detecting multiple forbidden keywords."""
        blacklist = {
            'word1': {'category': 'cat1', 'severity': 'medium'},
            'word2': {'category': 'cat2', 'severity': 'high'}
        }
        text = "This has word1 and word2 both"
        
        result = check_forbidden_keywords(text, blacklist)
        
        assert result['has_violation'] is True
        assert len(result['matched_terms']) == 2
        assert result['severity'] == 'high'  # Highest severity


class TestAffiliateLinkGenerator:
    """Tests for AffiliateLinkGenerator class."""

    def test_load_mappings_file_not_found(self, tmp_path):
        """Test error raised when fixture file not found."""
        non_existent_path = tmp_path / "non_existent.json"
        
        with pytest.raises(FileNotFoundError):
            AffiliateLinkGenerator(str(non_existent_path))

    def test_load_mappings_invalid_json(self, tmp_path):
        """Test error raised with invalid JSON."""
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text("invalid json")
        
        with pytest.raises(json.JSONDecodeError):
            AffiliateLinkGenerator(str(fixture_file))

    def test_generate_affiliate_link_found(self, tmp_path):
        """Test generating link for existing keyword."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Test Product",
                        "url": "https://amazon.com/dp/123",
                        "keyword": ["testproduct"],
                        "asin": "B123"
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        link = generator.generate_affiliate_link("testproduct")
        
        assert 'amazon.com' in link
        assert 'nofollow sponsored' in link
        assert '_blank' in link
        assert 'Test Product' in link

    def test_generate_affiliate_link_not_found(self, tmp_path):
        """Test generating link for non-existent keyword returns keyword."""
        fixture_data = {"affiliate_mappings": {}}
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        result = generator.generate_affiliate_link("nonexistent")
        
        assert result == "nonexistent"

    def test_generate_affiliate_link_custom_text(self, tmp_path):
        """Test generating link with custom link text."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Test Product",
                        "url": "https://amazon.com/dp/123",
                        "keyword": ["testproduct"]
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        link = generator.generate_affiliate_link("testproduct", link_text="Click Here")
        
        assert 'Click Here' in link

    def test_convert_text_with_affiliate_links(self, tmp_path):
        """Test converting text with multiple keywords."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Product 1",
                        "url": "https://amazon.com/dp/1",
                        "keyword": ["product1"]
                    },
                    "product2": {
                        "name": "Product 2",
                        "url": "https://amazon.com/dp/2",
                        "keyword": ["product2"]
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        text = "Buy product1 and product2 today!"
        result = generator.convert_text_with_affiliate_links(text)
        
        assert 'amazon.com/dp/1' in result
        assert 'amazon.com/dp/2' in result
        assert 'product1' not in result or '<a' in result  # Either replaced or in link

    def test_convert_text_respects_max_links(self, tmp_path):
        """Test max_links_per_text limit is respected."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    f"product{i}": {
                        "name": f"Product {i}",
                        "url": f"https://amazon.com/dp/{i}",
                        "keyword": [f"product{i}"]
                    }
                    for i in range(10)
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        text = " ".join([f"product{i}" for i in range(10)])
        result = generator.convert_text_with_affiliate_links(text, max_links_per_text=3)
        
        # Count number of links (count <a tags)
        link_count = result.count('<a ')
        assert link_count == 3

    def test_get_product_by_keyword(self, tmp_path):
        """Test retrieving product info by keyword."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Test Product",
                        "url": "https://amazon.com/dp/123",
                        "keyword": ["testproduct"],
                        "asin": "B123"
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        product = generator.get_product_by_keyword("testproduct")
        
        assert product is not None
        assert product['name'] == "Test Product"
        assert product['platform'] == "amazon"

    def test_get_all_keywords(self, tmp_path):
        """Test getting all available keywords."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Product 1",
                        "url": "https://amazon.com/dp/1",
                        "keyword": ["keyword1", "keyword2"]
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        keywords = generator.get_all_keywords()
        
        assert len(keywords) == 2
        assert "keyword1" in keywords
        assert "keyword2" in keywords

    def test_get_platform_products(self, tmp_path):
        """Test getting products for specific platform."""
        fixture_data = {
            "affiliate_mappings": {
                "amazon": {
                    "product1": {
                        "name": "Amazon Product",
                        "url": "https://amazon.com/dp/1",
                        "keyword": ["keyword1"]
                    }
                },
                "iherb": {
                    "product2": {
                        "name": "iHerb Product",
                        "url": "https://iherb.com/p/1",
                        "keyword": ["keyword2"]
                    }
                }
            }
        }
        
        fixture_file = tmp_path / "affiliate_products.json"
        fixture_file.write_text(json.dumps(fixture_data))
        
        generator = AffiliateLinkGenerator(str(fixture_file))
        amazon_products = generator.get_platform_products("amazon")
        
        assert len(amazon_products) == 1
        assert amazon_products[0]['name'] == "Amazon Product"


class TestGlobalAffiliateFunctions:
    """Tests for global affiliate convenience functions."""

    def test_get_affiliate_generator_singleton(self):
        """Test that get_affiliate_generator returns singleton."""
        gen1 = get_affiliate_generator()
        gen2 = get_affiliate_generator()
        
        assert gen1 is gen2


class TestModerateContent:
    """Tests for moderate_content function."""

    def test_moderate_content_empty_text(self):
        """Test moderating empty text."""
        result = moderate_content("", use_ai=False)
        
        assert result['is_flagged'] is False
        assert 'empty' in result['reason'].lower() or 'no violation' in result['reason'].lower()

    def test_moderate_content_clean_text(self):
        """Test moderating clean text."""
        result = moderate_content("This is a clean text about hygiene tips", use_ai=False)
        
        assert result['is_flagged'] is False

    def test_moderate_content_with_violation(self):
        """Test moderating text with violations."""
        # Use a term from default blacklist
        result = moderate_content("This contains suicide reference", use_ai=False)
        
        assert result['is_flagged'] is True
        assert result['category'] == 'self_harm'
        assert result['confidence'] == 1.0

    def test_moderate_content_method_keyword(self):
        """Test that keyword method is indicated."""
        result = moderate_content("test", use_ai=False)
        
        assert result['method'] == 'keyword'


class TestGetModerationSummary:
    """Tests for get_moderation_summary function."""

    def test_empty_results(self):
        """Test summary with no results."""
        summary = get_moderation_summary([])
        
        assert summary['total_reviewed'] == 0
        assert summary['total_flagged'] == 0
        assert summary['flag_rate'] == 0

    def test_all_clean(self):
        """Test summary with all clean content."""
        results = [
            {'is_flagged': False, 'category': None},
            {'is_flagged': False, 'category': None},
        ]
        summary = get_moderation_summary(results)
        
        assert summary['total_reviewed'] == 2
        assert summary['total_flagged'] == 0
        assert summary['flag_rate'] == 0
        assert summary['flagged_percent'] == 0

    def test_mixed_results(self):
        """Test summary with mixed flagged and clean content."""
        results = [
            {'is_flagged': True, 'category': 'spam'},
            {'is_flagged': False, 'category': None},
            {'is_flagged': True, 'category': 'inappropriate'},
            {'is_flagged': False, 'category': None},
        ]
        summary = get_moderation_summary(results)
        
        assert summary['total_reviewed'] == 4
        assert summary['total_flagged'] == 2
        assert summary['flag_rate'] == 0.5
        assert summary['flagged_percent'] == 50.0
        assert summary['flagged_categories']['spam'] == 1
        assert summary['flagged_categories']['inappropriate'] == 1


class TestContentModerationMiddleware:
    """Tests for ContentModerationMiddleware."""

    def test_middleware_initialization(self):
        """Test middleware initializes correctly."""
        get_response = Mock()
        middleware = ContentModerationMiddleware(get_response)
        
        assert middleware.get_response == get_response
        assert hasattr(middleware, 'blacklist')
        assert hasattr(middleware, 'ip_retention_days')

    def test_middleware_call_adds_hashed_ip(self):
        """Test middleware adds hashed_ip to request."""
        get_response = Mock(return_value=Mock())
        middleware = ContentModerationMiddleware(get_response)
        
        request = Mock()
        request.META = {'REMOTE_ADDR': '192.168.1.1'}
        
        with patch('apps.wiki.middleware.cache'):
            middleware(request)
        
        assert hasattr(request, 'hashed_ip')
        assert hasattr(request, 'client_ip')
        assert request.client_ip == '192.168.1.1'

    def test_moderate_content_classmethod(self):
        """Test classmethod for content moderation."""
        result = ContentModerationMiddleware.moderate_content("clean text")
        
        assert 'has_violation' in result

    def test_get_user_ip_hash_from_request(self):
        """Test getting IP hash from request attribute."""
        request = Mock()
        request.hashed_ip = 'test_hash_123'
        
        result = ContentModerationMiddleware.get_user_ip_hash(request)
        assert result == 'test_hash_123'

    def test_get_user_ip_hash_calculates_if_missing(self):
        """Test calculating IP hash if not in request."""
        request = Mock()
        request.META = {'REMOTE_ADDR': '192.168.1.1'}
        del request.hashed_ip  # Ensure attribute doesn't exist
        
        result = ContentModerationMiddleware.get_user_ip_hash(request)
        assert len(result) == 64  # SHA-256 hex length

    def test_get_period_seconds(self):
        """Test period conversion to seconds."""
        assert ContentModerationMiddleware._get_period_seconds('hour') == 3600
        assert ContentModerationMiddleware._get_period_seconds('day') == 86400
        assert ContentModerationMiddleware._get_period_seconds('week') == 604800
        assert ContentModerationMiddleware._get_period_seconds('invalid') == 3600  # Default
