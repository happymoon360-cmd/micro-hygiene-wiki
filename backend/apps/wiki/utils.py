"""
Utility functions for affiliate link generation and management.

This module provides functionality to automatically convert keywords in text
into affiliate links with proper SEO attributes (rel="nofollow sponsored").
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class AffiliateLinkGenerator:
    """
    Generates affiliate links from keyword mappings.

    Uses a JSON fixture file containing product mappings for Amazon and iHerb.
    Keywords in text are automatically replaced with affiliate links containing
    rel="nofollow sponsored" attributes for SEO compliance.
    """

    def __init__(self, fixture_path: Optional[str] = None):
        """
        Initialize the affiliate link generator.

        Args:
            fixture_path: Optional path to the affiliate_products.json fixture file.
                         If not provided, uses the default path relative to this file.
        """
        if fixture_path is None:
            # Default path: fixtures/affiliate_products.json relative to this file
            base_dir = Path(__file__).parent
            fixture_path = base_dir / "fixtures" / "affiliate_products.json"

        self.fixture_path = Path(fixture_path)
        self._mappings: Dict = self._load_mappings()
        self._keyword_index: Dict[str, Dict] = self._build_keyword_index()

    def _load_mappings(self) -> Dict:
        """
        Load affiliate product mappings from JSON fixture file.

        Returns:
            Dictionary containing affiliate mappings organized by platform.

        Raises:
            FileNotFoundError: If the fixture file doesn't exist.
            json.JSONDecodeError: If the fixture file contains invalid JSON.
        """
        if not self.fixture_path.exists():
            raise FileNotFoundError(
                f"Affiliate fixture file not found: {self.fixture_path}"
            )

        with open(self.fixture_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_keyword_index(self) -> Dict[str, Dict]:
        """
        Build a keyword-to-product mapping index for efficient lookup.

        Returns:
            Dictionary mapping keywords to product information including URL and platform.
        """
        index = {}

        for platform, products in self._mappings.get("affiliate_mappings", {}).items():
            for product_key, product_data in products.items():
                for keyword in product_data.get("keyword", []):
                    normalized_keyword = keyword.lower().strip()
                    index[normalized_keyword] = {
                        "name": product_data.get("name", ""),
                        "url": product_data.get("url", ""),
                        "platform": platform,
                        "product_id": product_data.get("asin")
                        or product_data.get("product_id", ""),
                    }

        return index

    def generate_affiliate_link(
        self,
        keyword: str,
        link_text: Optional[str] = None,
        css_class: Optional[str] = None,
        target: str = "_blank",
    ) -> str:
        """
        Generate an affiliate link HTML tag for a given keyword.

        Args:
            keyword: The keyword to look up in the affiliate database.
            link_text: Optional custom text for the link. If not provided, uses the keyword.
            css_class: Optional CSS class name to add to the link.
            target: Link target attribute (default: "_blank" for new tab).

        Returns:
            HTML string with the affiliate link, or the original keyword if no match found.

        Example:
            >>> generator.generate_affiliate_link("omega3")
            '<a href="https://www.amazon.com/dp/..." rel="nofollow sponsored" target="_blank">omega3</a>'
        """
        normalized_keyword = keyword.lower().strip()
        product_info = self._keyword_index.get(normalized_keyword)

        if not product_info:
            # Return original keyword if no affiliate mapping found
            return keyword

        link_text = link_text or keyword
        css_class_attr = f' class="{css_class}"' if css_class else ""

        html = (
            f'<a href="{product_info["url"]}" '
            f'rel="nofollow sponsored" '
            f'target="{target}" '
            f'title="{product_info["name"]}" '
            f'data-affiliate-platform="{product_info["platform"]}"'
            f"{css_class_attr}>"
            f"{link_text}"
            f"</a>"
        )

        return html

    def convert_text_with_affiliate_links(
        self,
        text: str,
        skip_words: Optional[List[str]] = None,
        max_links_per_text: int = 5,
    ) -> str:
        """
        Convert keywords in text to affiliate links.

        Args:
            text: Input text to convert.
            skip_words: Optional list of words to skip (won't be converted to links).
            max_links_per_text: Maximum number of affiliate links to generate per text.

        Returns:
            Text with keywords replaced by affiliate links.

        Example:
            >>> text = "I recommend omega3 and vitamin_d3 supplements."
            >>> generator.convert_text_with_affiliate_links(text)
            'I recommend <a href="...">omega3</a> and <a href="...">vitamin_d3</a> supplements.'
        """
        if skip_words is None:
            skip_words = []

        words_to_skip = {word.lower().strip() for word in skip_words}
        result = text
        links_added = 0

        # Sort keywords by length (longest first) to avoid partial matches
        sorted_keywords = sorted(
            self._keyword_index.keys(), key=lambda x: len(x.split()), reverse=True
        )

        for keyword in sorted_keywords:
            if links_added >= max_links_per_text:
                break

            if keyword in words_to_skip:
                continue

            if keyword.lower() in result.lower():
                # Generate affiliate link for this keyword
                affiliate_link = self.generate_affiliate_link(keyword)

                # Replace only the first occurrence to avoid spam
                result = result.replace(keyword, affiliate_link, 1)
                links_added += 1

        return result

    def get_product_by_keyword(self, keyword: str) -> Optional[Dict]:
        """
        Get product information by keyword.

        Args:
            keyword: The keyword to look up.

        Returns:
            Product information dictionary, or None if not found.

        Example:
            >>> generator.get_product_by_keyword("probiotic")
            {
                'name': 'Garden of Life Dr. Formulated Probiotics',
                'url': 'https://www.amazon.com/dp/...',
                'platform': 'amazon',
                'product_id': 'B00J0Y8QG4'
            }
        """
        return self._keyword_index.get(keyword.lower().strip())

    def get_all_keywords(self) -> List[str]:
        """
        Get all available keywords in the affiliate database.

        Returns:
            List of all keywords that can be converted to affiliate links.
        """
        return list(self._keyword_index.keys())

    def get_platform_products(self, platform: str) -> List[Dict]:
        """
        Get all products for a specific platform.

        Args:
            platform: Platform name ('amazon' or 'iherb').

        Returns:
            List of product dictionaries for the specified platform.
        """
        products = self._mappings.get("affiliate_mappings", {}).get(platform, {})
        return [
            {
                "product_key": key,
                "name": data.get("name", ""),
                "url": data.get("url", ""),
                "keywords": data.get("keyword", []),
            }
            for key, data in products.items()
        ]


# Global instance for convenience
_affiliate_generator: Optional[AffiliateLinkGenerator] = None


def get_affiliate_generator() -> AffiliateLinkGenerator:
    """
    Get or create the global affiliate link generator instance.

    Returns:
        Shared AffiliateLinkGenerator instance.
    """
    global _affiliate_generator
    if _affiliate_generator is None:
        _affiliate_generator = AffiliateLinkGenerator()
    return _affiliate_generator


def generate_affiliate_link(
    keyword: str,
    link_text: Optional[str] = None,
    css_class: Optional[str] = None,
    target: str = "_blank",
) -> str:
    """
    Convenience function to generate an affiliate link for a keyword.

    Args:
        keyword: The keyword to look up in the affiliate database.
        link_text: Optional custom text for the link.
        css_class: Optional CSS class name.
        target: Link target attribute.

    Returns:
        HTML string with the affiliate link.
    """
    generator = get_affiliate_generator()
    return generator.generate_affiliate_link(keyword, link_text, css_class, target)


def convert_text_with_affiliate_links(
    text: str, skip_words: Optional[List[str]] = None, max_links_per_text: int = 5
) -> str:
    """
    Convenience function to convert text keywords to affiliate links.

    Args:
        text: Input text to convert.
        skip_words: Optional list of words to skip.
        max_links_per_text: Maximum number of affiliate links per text.

    Returns:
        Text with keywords replaced by affiliate links.
    """
    generator = get_affiliate_generator()
    return generator.convert_text_with_affiliate_links(
        text, skip_words, max_links_per_text
    )


import logging
from threading import Lock

logger = logging.getLogger(__name__)


class AIModerator:
    """
    AI-powered content moderator using Hugging Face zero-shot classification.
    """

    _classifier = None
    _lock = Lock()
    _is_initialized = False
    _initialization_error = None

    DEFAULT_CATEGORIES = [
        "self harm",
        "violence",
        "suicide",
        "substance abuse",
        "threat",
        "harassment",
        "safe content",
    ]

    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize AI moderator with optional custom model.

        Args:
            model_name: Hugging Face model identifier (e.g., "facebook/bart-large-mnli")
        """
        self.model_name = model_name or getattr(
            settings, "HUGGINGFACE_ZERO_SHOT_MODEL", "facebook/bart-large-mnli"
        )
        self.categories = getattr(
            settings, "MODERATION_CATEGORIES", self.DEFAULT_CATEGORIES
        )

    @classmethod
    def get_classifier(cls):
        """
        Get or initialize the zero-shot classifier (lazy loading).
        Uses singleton pattern to avoid loading model multiple times.
        """
        if cls._is_initialized or cls._initialization_error is not None:
            if cls._initialization_error:
                raise RuntimeError(
                    f"AI Classifier initialization failed: {cls._initialization_error}"
                )
            return cls._classifier

        with cls._lock:
            if cls._is_initialized:
                return cls._classifier

            try:
                from transformers import pipeline

                model_name = getattr(
                    settings, "HUGGINGFACE_ZERO_SHOT_MODEL", "facebook/bart-large-mnli"
                )

                logger.info(
                    f"Initializing Hugging Face zero-shot classifier: {model_name}"
                )
                cls._classifier = pipeline(
                    "zero-shot-classification", model=model_name, device=-1
                )
                cls._is_initialized = True
                logger.info(
                    "Hugging Face zero-shot classifier initialized successfully"
                )

                return cls._classifier

            except ImportError as e:
                error_msg = f"Failed to import transformers library: {e}"
                cls._initialization_error = error_msg
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            except Exception as e:
                error_msg = f"Failed to initialize Hugging Face classifier: {e}"
                cls._initialization_error = error_msg
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            except Exception as e:
                error_msg = f"Failed to initialize Hugging Face classifier: {e}"
                cls._initialization_error = error_msg
                logger.error(error_msg)
                raise RuntimeError(error_msg)

    def moderate_text(self, text: str, threshold: float = 0.5) -> Dict[str, any]:
        """
        Moderate text using zero-shot classification.

        Args:
            text: Text to moderate
            threshold: Confidence threshold for flagging (0.0 to 1.0)

        Returns:
            Dictionary with moderation results:
            {
                'is_flagged': bool,
                'reason': str,
                'confidence': float,
                'category': str,
                'all_scores': dict
            }
        """
        if not text or not text.strip():
            return {
                'is_flagged': False,
                'reason': 'Empty content',
                'confidence': 0.0,
                'category': None,
                'all_scores': {}
            }

        try:
            classifier = self.get_classifier()

            result = classifier(
                text,
                candidate_labels=self.categories,
                multi_label=False
            )

            flagged_categories = [cat for cat in self.categories if cat != 'safe content']

            top_result = result['labels'][0]
            top_score = result['scores'][0]

            is_flagged = (
                top_result in flagged_categories and
                top_score >= threshold
            )

            return {
                'is_flagged': is_flagged,
                'reason': f"Content flagged as: {top_result}",
                'confidence': top_score,
                'category': top_result if is_flagged else None,
                'all_scores': dict(zip(result['labels'], result['scores']))
            }

        except RuntimeError as e:
            logger.warning(f"AI classifier unavailable, falling back to keyword check: {e}")
            return self._fallback_keyword_check(text)

        except Exception as e:
            logger.error(f"Error during AI moderation: {e}")
            return {
                'is_flagged': False,
                'reason': 'Moderation error',
                'confidence': 0.0,
                'category': None,
                'all_scores': {}
            }
        if not text or not text.strip():
            return {
                "is_flagged": False,
                "reason": "Empty content",
                "confidence": 0.0,
                "category": None,
                "all_scores": {},
            }

        try:
            classifier = self.get_classifier()

            # Run zero-shot classification
            result = classifier(
                text, candidate_labels=self.categories, multi_label=False
            )

            # Find highest scoring category (excluding 'safe content')
            flagged_categories = [
                cat for cat in self.categories if cat != "safe content"
            ]

            top_result = result["labels"][0]
            top_score = result["scores"][0]

            # Check if content is flagged (not safe)
            is_flagged = top_result in flagged_categories and top_score >= threshold

            return {
                "is_flagged": is_flagged,
                "reason": f"Content flagged as: {top_result}",
                "confidence": top_score,
                "category": top_result if is_flagged else None,
                "all_scores": dict(zip(result["labels"], result["scores"])),
            }

        except RuntimeError as e:
            # Fall back to simple keyword check if AI classifier fails
            logger.warning(
                f"AI classifier unavailable, falling back to keyword check: {e}"
            )
            return self._fallback_keyword_check(text)

        except Exception as e:
            logger.error(f"Error during AI moderation: {e}")
            return {
                "is_flagged": False,
                "reason": "Moderation error",
                "confidence": 0.0,
                "category": None,
                "all_scores": {},
            }

    def _fallback_keyword_check(self, text: str) -> Dict[str, any]:
        """
        Fallback keyword-based moderation when AI classifier is unavailable.

        Args:
            text: Text to check

        Returns:
            Dictionary with moderation results
        """
        from .middleware import load_blacklist_terms, check_forbidden_keywords

        blacklist = load_blacklist_terms()
        result = check_forbidden_keywords(text, blacklist)

        if result["has_violation"]:
            return {
                "is_flagged": True,
                "reason": f"Flagged terms: {', '.join(t['term'] for t in result['matched_terms'])}",
                "confidence": 1.0,
                "category": result["matched_terms"][0]["category"],
                "all_scores": {"keyword_match": 1.0},
            }

        return {
            "is_flagged": False,
            "reason": "No prohibited keywords found",
            "confidence": 0.0,
            "category": None,
            "all_scores": {},
        }

    def batch_moderate(
        self, texts: List[str], threshold: float = 0.5
    ) -> List[Dict[str, any]]:
        """
        Moderate multiple texts in batch for efficiency.

        Args:
            texts: List of texts to moderate
            threshold: Confidence threshold for flagging

        Returns:
            List of moderation result dictionaries
        """
        return [self.moderate_text(text, threshold) for text in texts]


def moderate_content(
    text: str, threshold: float = 0.5, use_ai: bool = True
) -> Dict[str, any]:
    """
    Convenience function for content moderation.

    Args:
        text: Text to moderate
        threshold: Confidence threshold for flagging (0.0 to 1.0)
        use_ai: Whether to use AI moderation (falls back to keywords if unavailable)

    Returns:
        Dictionary with moderation results
    """
    if use_ai:
        moderator = AIModerator()
        return moderator.moderate_text(text, threshold)
    else:
        from .middleware import load_blacklist_terms, check_forbidden_keywords

        blacklist = load_blacklist_terms()
        result = check_forbidden_keywords(text, blacklist)

        if result["has_violation"]:
            return {
                "is_flagged": True,
                "reason": f"Flagged terms: {', '.join(t['term'] for t in result['matched_terms'])}",
                "confidence": 1.0,
                "category": result["matched_terms"][0]["category"],
                "all_scores": {"keyword_match": 1.0},
                "method": "keyword",
            }

        return {
            "is_flagged": False,
            "reason": "No violations found",
            "confidence": 0.0,
            "category": None,
            "all_scores": {},
            "method": "keyword",
        }


def get_moderation_summary(results: List[Dict[str, any]]) -> Dict[str, any]:
    """
    Get summary statistics from multiple moderation results.

    Args:
        results: List of moderation result dictionaries

    Returns:
        Summary dictionary with statistics
    """
    total = len(results)
    flagged = sum(1 for r in results if r.get("is_flagged", False))

    categories = {}
    for result in results:
        category = result.get("category")
        if category:
            categories[category] = categories.get(category, 0) + 1

    return {
        "total_reviewed": total,
        "total_flagged": flagged,
        "flag_rate": flagged / total if total > 0 else 0,
        "flagged_categories": categories,
        "flagged_percent": (flagged / total * 100) if total > 0 else 0,
    }
