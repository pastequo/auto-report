"""Get release statistics from OpenSearch"""

import collections
from distutils.version import LooseVersion
from opensearchpy import OpenSearch


class ReleaseStats:  # pylint: disable=too-few-public-methods
    """
    Provides release stats from OpenSearch data.
    """
    def __init__(self, opensearch_client: OpenSearch, index: str, logger):
        """Constructor, accepts opensearch client"""
        self._os_client = opensearch_client
        self._index = index
        self._logger = logger

    def get(self, from_date: str, to_date: str, top_n: int = None) -> dict:
        """
        Returns stats. Format:
        {
          "<release_tag>": {
            "<install_result>": {
              "value": "<absolute>", "percent": "<percent>
            }
          }
        }
        """
        query = _get_query(from_date, to_date)
        self._logger.debug("OpenSearch query: %s", query)
        response = self._os_client.search(index=self._index, body=query)
        self._logger.debug("OpenSearch response: %s", response)
        stats = parse_response(response)

        if not top_n:
            return stats

        return _get_top_by_version(stats, top_n)


def _get_top_by_version(stats: dict, top_n: int) -> dict:
    """
    Returns top N releases, ordered by version
    from latest to oldest
    """

    top_versions = sorted(stats, key=LooseVersion, reverse=True)[0:top_n]
    releases = collections.OrderedDict()
    for version in top_versions:
        releases[version] = stats[version]

    return releases


def _get_query(from_date: str, to_date: str) -> str:
    """
    Return query to select releases
    """
    return {
        "aggs": {
            "releases": {
                "terms": {
                    "field": "release_tag",
                    "order": {
                        "_key": "asc"
                    },
                    "size": 100
                },
                "aggs": {
                    "install_result": {
                        "terms": {
                            "field": "event.props.result"
                        },
                        "aggs": {
                            "unique_count": {
                                "cardinality": {
                                    "field": "cluster.id"
                                }
                            }
                        }
                    }
                }
            }
        },
        "size": 0,
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "match_all": {}
                    },
                    {
                        "bool": {
                            "should": [
                                {
                                    "match_phrase": {
                                        "message.keyword": "cluster.installation.results"
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    },
                    {
                        "range": {
                            "event_time": {
                                "gte": from_date,
                                "lte": to_date,
                            }
                        }
                    }
                ],
                "should": [],
                "must_not": [
                    {
                        "bool": {
                            "minimum_should_match": 1,
                            "should": [
                                {
                                    "match_phrase": {
                                        "cluster.email_domain": "redhat.com"
                                    }
                                },
                                {
                                    "match_phrase": {
                                        "cluster.email_domain": "ibm.com"
                                    }
                                },
                                {
                                    "match_phrase": {
                                        "cluster.email_domain": "fr.ibm.com"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "bool": {
                            "minimum_should_match": 1,
                            "should": [
                                {
                                    "match_phrase": {
                                        "cluster.email_domain": "juniper.net"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "match_phrase": {
                            "event.props.result": "Done"
                        }
                    },
                    {
                        "match_phrase": {
                            "event.props.result": "installing-pending-user-action"
                        }
                    }
                ]
            }
        }
    }


def parse_response(response):
    """Parses OpenSearch response into releases"""

    releases = {}
    for release in response["aggregations"]["releases"]["buckets"]:
        releases[release["key"]] = parse_results(release["install_result"]["buckets"])
    return releases


def parse_results(results_buckets):
    """Extracts results from partial opensearch response"""
    results = {}
    total = 0
    for result in results_buckets:
        results[result["key"]] = result["unique_count"]["value"]
        total += result["unique_count"]["value"]
    results["total"] = total
    return results
