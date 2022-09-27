"""
Tests retrieving releases stats.
"""
# pylint: disable=no-self-use

from unittest import mock
import pytest
from auto_report import ReleaseStats
from .utils import load_json_from_file


response_release_stats = [
    # mock integration data: master only release, unlimited
    (
        load_json_from_file(
            "opensearch_response_only_one_release.json"
        ),
        {
            "master": {
                "total": 61,
                "installed": 35,
                "error": 7,
                "cancelled": 19,
            }
        },
        None
    ),
    # mock production data, unlimited
    (
        load_json_from_file(
            "opensearch_response_many_releases.json"
        ),
        {
            "v2.4.4": {
                "total": 11,
                "installed": 7,
                "error": 4,
            },
            "v2.5.0": {
                "total": 86,
                "installed": 59,
                "error": 14,
                "cancelled": 13,
            },
            "v2.5.1": {
                "total": 60,
                "installed": 40,
                "error": 13,
                "cancelled": 7,
            },
            "v2.5.2": {
                "total": 552,
                "installed": 410,
                "error": 99,
                "cancelled": 43,
            },
            "v2.6.0": {
                "total": 364,
                "installed": 270,
                "error": 66,
                "cancelled": 28,
            },
            "v2.7.0": {
                "total": 480,
                "installed": 375,
                "error": 80,
                "cancelled": 25,
            },
            "v2.8.1": {
                "total": 320,
                "installed": 254,
                "error": 43,
                "cancelled": 23,
            },
            "v2.9.0": {
                "total": 491,
                "installed": 369,
                "error": 92,
                "cancelled": 30,
            },
        },
        None
    ),
    # mock production data, top 3
    (
        load_json_from_file(
            "opensearch_response_many_releases.json"
        ),
        {
            "v2.7.0": {
                "total": 480,
                "installed": 375,
                "error": 80,
                "cancelled": 25,
            },
            "v2.8.1": {
                "total": 320,
                "installed": 254,
                "error": 43,
                "cancelled": 23,
            },
            "v2.9.0": {
                "total": 491,
                "installed": 369,
                "error": 92,
                "cancelled": 30,
            },
        },
        3
    ),
]


class TestReleaseStats:  # pylint: disable=too-few-public-methods
    """Test release stats"""

    @pytest.mark.parametrize("mock_response,expected_stats,top_n", response_release_stats)
    def test_release_stats(self, mock_response, expected_stats, top_n):
        """Tests release stats for multiple cases"""
        mock_opensearch_client = mock.Mock()
        mock_opensearch_client.search = mock.Mock(return_value=mock_response)
        mock_logger = mock.Mock()

        release_stats = ReleaseStats(mock_opensearch_client, "myindex", mock_logger)

        stats = release_stats.get(
            from_date="now-6w/d",
            to_date="now/d",
            top_n=top_n
        )
        assert mock_opensearch_client.search.call_count == 1
        assert expected_stats == stats

# pylint: enable=no-self-use
