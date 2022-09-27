"""
Auto-report generates reports automatically.
"""

from .release_stats import ReleaseStats
from .release_formatter import format_releases_to_text

__all__ = [
    "ReleaseStats",
    "format_releases_to_text",
]
