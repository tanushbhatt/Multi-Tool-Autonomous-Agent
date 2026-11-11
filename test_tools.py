import unittest
from unittest.mock import patch
from pathlib import Path
from tools import TOOLS, calculator, read_local_file, web_search


class TestAgentTools(unittest.TestCase):

    def setUp(self):
        # Create a temporary sample file for testing
        self.sample_file = (
            Path(__file__).resolve().parent / "tool_test_sample.txt"
        )

        self.sample_content = "Hello Tanush! This is a tool test."

        self.sample_file.write_text(
            self.sample_content,
            encoding="utf-8"
        )

    def tearDown(self):
        # Delete the temporary sample file
        if self.sample_file.exists():
            self.sample_file.unlink()

    # Test 1: Check all three tools are registered
    def test_tool_registration(self):
        tool_names = {item.name for item in TOOLS}

        self.assertEqual(
            tool_names,
            {"web_search", "calculator", "read_local_file"}
        )

    # Test 2: Test calculator
    def test_calculator(self):
        result = calculator.invoke({
            "expression": "25 * 4 + 100"
        })

        self.assertEqual(result, "Result: 200")

    # Test 3: Test division by zero
    def test_calculator_division_by_zero(self):
        result = calculator.invoke({
            "expression": "100 / 0"
        })

        self.assertIn("Cannot divide by zero", result)

    # Test 4: Reject unsafe Python code
    def test_calculator_rejects_unsafe_code(self):
        result = calculator.invoke({
            "expression": "__import__('os').system('whoami')"
        })

        self.assertIn("Calculation failed", result)

    # Test 5: Test local file reader
    def test_file_reader(self):
        result = read_local_file.invoke({
            "file_path": "tool_test_sample.txt"
        })

        self.assertEqual(result, self.sample_content)

    # Test 6: Test missing file
    def test_file_reader_missing_file(self):
        result = read_local_file.invoke({
            "file_path": "missing_file.txt"
        })

        self.assertIn("File not found", result)

    # Test 7: Prevent access outside project directory
    def test_file_reader_blocks_external_access(self):
        result = read_local_file.invoke({
            "file_path": "../README.md"
        })

        self.assertIn("Access outside", result)


    
    # Test 8: Web search returns formatted results
    @patch("tools.DDGS")
    def test_web_search_returns_results(self, mock_ddgs):

        mock_client = mock_ddgs.return_value

        mock_client.text.return_value = [
            {
                "title": "Python Official Website",
                "href": "https://www.python.org/",
                "body": "Python is a programming language."
            }
        ]

        result = web_search.invoke({
            "query": "Python programming",
            "max_results": 2
        })

        self.assertIn("Python Official Website", result)
        self.assertIn("https://www.python.org/", result)
        self.assertIn("programming language", result)

    # Test 9: Handle empty search results
    @patch("tools.DDGS")
    def test_web_search_no_results(self, mock_ddgs):

        mock_client = mock_ddgs.return_value
        mock_client.text.return_value = []

        result = web_search.invoke({
            "query": "Unknown topic",
            "max_results": 3
        })

        self.assertEqual(result, "No search results found.")

    # Test 10: Reject empty search queries
    def test_web_search_empty_query(self):

        result = web_search.invoke({
            "query": "   ",
            "max_results": 3
        })

        self.assertIn("cannot be empty", result)


if __name__ == "__main__":
    unittest.main()
