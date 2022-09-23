"""
Tests retrieving releases stats.
"""
# pylint: disable=no-self-use

import pytest
from auto_report import format_releases_to_text
from .utils import load_json_from_file


releases_and_text = [
    # empty releases produce empty string
    ({}, ""),
    # standard representation
    (
        load_json_from_file(
            "top_three_releases.json"
        ),
        """v2.9.0      installed   369   (75.15%)
v2.9.0      error       92    (18.74%)
v2.9.0      cancelled   30    (6.11%)
---
v2.8.1      installed   254   (79.38%)
v2.8.1      error       43    (13.44%)
v2.8.1      cancelled   23    (7.19%)
---
v2.7.0      installed   375   (78.12%)
v2.7.0      error       80    (16.67%)
v2.7.0      cancelled   25    (5.21%)"""
    )
    ]


class TestReleaseFormatter:  # pylint: disable=too-few-public-methods
    """Tests release formatter"""

    @pytest.mark.parametrize("releases,expected_text", releases_and_text)
    def test_get_text(self, releases, expected_text):
        """Tests multiple inputs for text formatting releases"""
        text = format_releases_to_text(releases)
        assert text == expected_text

# pylint: enable=no-self-use
