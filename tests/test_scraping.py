import unittest
from unittest.mock import patch, MagicMock
from scraping import find_script
import requests
from typing import Dict, Optional, Any

class TestFindScript(unittest.TestCase):

    @patch('scraping.requests.get')
    def test_find_script_success(self, mock_get: MagicMock) -> None:
        # Mock the response content
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <script id="__NEXT_DATA__">
            {
                "props": {
                    "versions": [
                        {"name": "Test App", "vername": "1.0", "date": "2024-01-01"}
                    ],
                    "app": {
                        "media": {"description": "Test Description"},
                        "stats": {"pdownloads": 12345}
                    }
                }
            }
            </script>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        # Call the find_script function
        result: Optional[Dict[str, Any]] = find_script('http://test.com', '__NEXT_DATA__')

        # Assert the function returned the correct info
        self.assertEqual(result['name'], 'Test App')
        self.assertEqual(result['version'], '1.0')
        self.assertEqual(result['date'], '2024-01-01')
        self.assertEqual(result['downloads'], 12345)
        self.assertEqual(result['description'], 'Test Description')

    @patch('scraping.requests.get')
    def test_find_script_missing_script_tag(self, mock_get: MagicMock) -> None:
        # Mock the response content with no script tag
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <!-- No script tag here -->
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        # Call the find_script function
        result: Optional[Dict[str, Any]] = find_script('http://test.com', '__NEXT_DATA__')

        # Assert that the result is None because the script tag is missing
        self.assertIsNone(result)

    @patch('scraping.requests.get')
    def test_find_script_invalid_json(self, mock_get: MagicMock) -> None:
        # Mock the response content with invalid JSON in the script tag
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <script id="__NEXT_DATA__">
            {
                "props": {
                    "versions": [
                        {"name": "Test App", "vername": "1.0", "date": "2024-01-01"}
                    ],
                    "app": {
                        "media": {"description": "Test Description"},
                        "stats": {"pdownloads": "invalid-number"}
                    }
                }
            </script>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        # Call the find_script function and expect it to return None due to invalid JSON
        result: Optional[Dict[str, Any]] = find_script('http://test.com', '__NEXT_DATA__')

        # The test expects None because of invalid JSON content
        self.assertIsNone(result)

    @patch('scraping.requests.get')
    def test_find_script_http_error(self, mock_get: MagicMock) -> None:
        # Simulate an HTTP error by having requests.get raise an exception
        mock_get.side_effect = requests.exceptions.RequestException

        # Call the find_script function
        result: Optional[Dict[str, Any]] = find_script('http://test.com', '__NEXT_DATA__')

        # Assert that the result is None because of the exception
        self.assertIsNone(result)

    @patch('scraping.requests.get')
    def test_find_script_invalid_script_id(self, mock_get: MagicMock) -> None:
        # Mock the response content with a script tag that doesn't match the provided ID
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <script id="some_other_id">
            {
                "props": {
                    "versions": [
                        {"name": "Test App", "vername": "1.0", "date": "2024-01-01"}
                    ],
                    "app": {
                        "media": {"description": "Test Description"},
                        "stats": {"pdownloads": 12345}
                    }
                }
            }
            </script>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        # Call the find_script function with a mismatched script ID
        result: Optional[Dict[str, Any]] = find_script('http://test.com', '__NEXT_DATA__')

        # Assert that the result is None because the script ID does not match
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
