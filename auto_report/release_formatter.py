"""Formats releases to text"""


def format_releases_to_text(releases: dict) -> str:
    """Formats releases dictionary to text"""
    output = ""
    result_order = ["installed", "error", "cancelled"]
    for release, release_stats in releases.items():
        total = release_stats.pop("total")
        for result in result_order:
            if result in release_stats:
                value = release_stats[result]
                absolute = str(value)
                percent = 100 * (value / total)
                output += release.ljust(12, " ") +\
                    result.ljust(12, " ") +\
                    absolute.ljust(6, " ") +\
                    f"({percent:.2f}%)" + "\n"
        output += "---\n"
    return output.rstrip("---\n")
