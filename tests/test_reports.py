import subprocess
import sys
from pathlib import Path

import pytest

from reports import median_coffee, REPORTS

MATH_CSV = Path(__file__).parent.parent / "math.csv"


class TestMedianCoffee:
    def test_median_is_correct(self):
        rows = [
            {"student": "Иван", "coffee_spent": "400"},
            {"student": "Иван", "coffee_spent": "600"},
            {"student": "Иван", "coffee_spent": "500"},
        ]
        result = median_coffee(rows)
        assert result[0]["student"] == "Иван"
        assert result[0]["median_coffee"] == 500.0

    def test_sorted_descending(self):
        rows = [
            {"student": "Аня", "coffee_spent": "100"},
            {"student": "Боб", "coffee_spent": "300"},
            {"student": "Вася", "coffee_spent": "200"},
        ]
        result = median_coffee(rows)
        medians = [r["median_coffee"] for r in result]
        assert medians == sorted(medians, reverse=True)

    def test_multiple_rows_per_student(self):
        rows = [
            {"student": "Аня", "coffee_spent": "100"},
            {"student": "Аня", "coffee_spent": "300"},
            {"student": "Боб", "coffee_spent": "200"},
            {"student": "Боб", "coffee_spent": "400"},
            {"student": "Боб", "coffee_spent": "600"},
        ]
        result = median_coffee(rows)
        aня = next(r for r in result if r["student"] == "Аня")
        bob = next(r for r in result if r["student"] == "Боб")
        assert aня["median_coffee"] == 200.0
        assert bob["median_coffee"] == 400.0

    def test_empty_input(self):
        assert median_coffee([]) == []

    def test_registered_in_reports(self):
        assert "median-coffee" in REPORTS


@pytest.mark.skipif(not MATH_CSV.exists(), reason="math.csv not found")
class TestCLI:
    def run(self, *args):
        return subprocess.run(
            [sys.executable, "main.py", *args],
            capture_output=True,
            text=True,
        )

    def test_output_has_headers(self):
        result = self.run("--files", str(MATH_CSV), "--report", "median-coffee")
        assert result.returncode == 0
        assert "student" in result.stdout
        assert "median_coffee" in result.stdout

    def test_output_sorted_descending(self):
        result = self.run("--files", str(MATH_CSV), "--report", "median-coffee")
        assert result.returncode == 0
        values = []
        for line in result.stdout.splitlines():
            if line.strip().startswith("|") and "student" not in line:
                parts = [p.strip() for p in line.strip("|").split("|")]
                try:
                    values.append(float(parts[1]))
                except (ValueError, IndexError):
                    pass
        assert values == sorted(values, reverse=True)

    def test_missing_file(self):
        result = self.run("--files", "nonexistent.csv", "--report", "median-coffee")
        assert result.returncode != 0
        assert "Error" in result.stderr

    def test_unknown_report(self):
        result = self.run("--files", str(MATH_CSV), "--report", "wrong-report")
        assert result.returncode != 0
