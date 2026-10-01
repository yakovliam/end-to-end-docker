import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts


class TextAnalysisTests(unittest.TestCase):
    def test_contractions_split_into_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("I'm sure I can't. Don't stop.", encoding="utf-8")

            self.assertEqual(
                scripts.read_words(path),
                ["i", "m", "sure", "i", "can", "t", "don", "t", "stop"],
            )

    def test_top_three_uses_count_then_alphabetical_order(self) -> None:
        words = ["pear", "apple", "pear", "banana", "apple", "zebra"]

        self.assertEqual(
            scripts.top_three(words),
            [("apple", 2), ("pear", 2), ("banana", 1)],
        )

    @patch("scripts.get_ip_address", return_value="172.17.0.2")
    def test_report_contains_all_required_results(self, _mock_ip) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_dir = Path(directory)
            (data_dir / "IF.txt").write_text("If if then", encoding="utf-8")
            (data_dir / "AlwaysRememberUsThisWay.txt").write_text(
                "I'm here", encoding="utf-8"
            )

            report = scripts.create_report(data_dir)

            self.assertIn("IF.txt word count: 3", report)
            self.assertIn("AlwaysRememberUsThisWay.txt word count: 3", report)
            self.assertIn("Grand total word count: 6", report)
            self.assertIn("1. if: 2", report)
            self.assertIn("Container IP address: 172.17.0.2", report)


if __name__ == "__main__":
    unittest.main()
