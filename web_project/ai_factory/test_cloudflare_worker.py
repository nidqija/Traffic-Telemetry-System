import unittest
from unittest.mock import patch, MagicMock
import requests
from ai_factory.cloudflare_worker_factory import CloudflareWorkerFactory

class TestCloudflareWorkerFactory(unittest.TestCase):

    @patch.dict("os.environ", {"CLOUDFLARE_ACCOUNT_ID": "mock_id", "CLOUDFLARE_API_TOKEN": "mock_token"})
    def setUp(self):
        """Sets up the factory instance before each test with mocked environment variables."""
        # We mock get_schema_context and clean_sql since they belong to the base class
        self.factory = CloudflareWorkerFactory()
        self.factory.get_schema_context = MagicMock(return_value="CREATE TABLE traffic_data (id INT);")
        self.factory.clean_sql = MagicMock(side_effect=lambda x: x)  # Returns string as-is

    @patch("os.environ", {})
    def test_init_missing_credentials(self):
        """Test that ValueError is raised if environment variables are missing."""
        with self.assertRaises(ValueError):
            CloudflareWorkerFactory()

    @patch("sqlite3.connect")
    @patch("requests.post")
    def test_ask_questions_success(self, mock_post, mock_sql_connect):
        """Test a fully successful API response and database execution sequence."""
        # 1. Mock the Cloudflare API response wrapper
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "response": "SELECT * FROM traffic_data;"
            }
        }
        mock_post.return_value = mock_response

        # 2. Mock SQLite connection, cursor, and description rows
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchall.return_value = [(1,), (2,)]
        mock_cursor.description = [("id", None, None, None, None, None, None)]
        mock_conn.cursor.return_value = mock_cursor
        mock_sql_connect.return_value = mock_conn

        # Execute
        results, columns = self.factory.ask_questions("Show all traffic data")

        # Assertions
        self.assertEqual(results, [(1,), (2,)])
        self.assertEqual(columns, ["id"])
        mock_post.assert_called_once()
        mock_cursor.execute.assert_called_with("SELECT * FROM traffic_data;")

    @patch("requests.post")
    def test_ask_questions_api_failure(self, mock_post):
        """Test that HTTP errors from Cloudflare are caught gracefully."""
        # Setup mock to raise an HTTP connection error
        mock_post.side_effect = requests.exceptions.RequestException("Connection timed out")

        result = self.factory.ask_questions("Show all traffic")

        

        self.assertIn("Error processing query", result)

    @patch("requests.post")
    def test_ask_questions_invalid_json_structure(self, mock_post):
        """Test that invalid structural schemas returned by the API are caught safely."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {}} # Missing 'response' key
        mock_post.return_value = mock_response

        result = self.factory.ask_questions("Show all traffic")

        # ASSERTION FIX: Match the string wrapper returned when the exception is safely caught
        self.assertIn("Error processing query", result)


if __name__ == "__main__":
    unittest.main()