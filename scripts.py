#!/usr/bin/env python3
"""Analyze the two text files for the Docker assignment."""

from __future__ import annotations

import os
import re
import socket
from collections import Counter
from pathlib import Path


DATA_DIR = Path(os.environ.get("DATA_DIR", "/home/data"))
INPUT_FILES = ("IF.txt", "AlwaysRememberUsThisWay.txt")
WORD_PATTERN = re.compile(r"[A-Za-z0-9]+")


def read_words(path: Path) -> list[str]:
    """Read a UTF-8 file and return lowercase words.

    Apostrophes are separators. Thus, a contraction such as "can't" becomes
    the two words "can" and "t" as the assignment requires.
    """

    text = path.read_text(encoding="utf-8")
    return WORD_PATTERN.findall(text.lower())


def top_three(words: list[str]) -> list[tuple[str, int]]:
    """Return three word counts with a stable order for equal counts."""

    counts = Counter(words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:3]


def get_ip_address() -> str:
    """Return the first non-loopback IPv4 address for this container."""

    try:
        addresses = socket.getaddrinfo(
            socket.gethostname(), None, family=socket.AF_INET
        )
        for address in addresses:
            ip_address = address[4][0]
            if not ip_address.startswith("127."):
                return ip_address
    except socket.gaierror:
        pass

    return "127.0.0.1"


def format_top_three(items: list[tuple[str, int]]) -> list[str]:
    """Format ranked word counts for the report."""

    return [f"  {rank}. {word}: {count}" for rank, (word, count) in enumerate(items, 1)]


def create_report(data_dir: Path = DATA_DIR) -> str:
    """Create the complete assignment report."""

    words_by_file = {
        name: read_words(data_dir / name)
        for name in INPUT_FILES
    }
    grand_total = sum(len(words) for words in words_by_file.values())

    lines = [
        "Docker Text Analysis Results",
        "============================",
        f"IF.txt word count: {len(words_by_file['IF.txt'])}",
        (
            "AlwaysRememberUsThisWay.txt word count: "
            f"{len(words_by_file['AlwaysRememberUsThisWay.txt'])}"
        ),
        f"Grand total word count: {grand_total}",
        "",
        "Top 3 words in IF.txt:",
        *format_top_three(top_three(words_by_file["IF.txt"])),
        "",
        "Top 3 words in AlwaysRememberUsThisWay.txt:",
        *format_top_three(
            top_three(words_by_file["AlwaysRememberUsThisWay.txt"])
        ),
        "",
        f"Container IP address: {get_ip_address()}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Write the report and print the same report to standard output."""

    output_path = DATA_DIR / "output" / "result.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = create_report()
    output_path.write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()
