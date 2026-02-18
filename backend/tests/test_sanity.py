import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.getcwd()))
from services.sanity import SanityClient

class TestSanityClient(unittest.TestCase):
    def setUp(self):
        self.client = SanityClient()
        self.client.token = "fake-token" # Ensure methods run

    @patch('services.sanity.requests.post')
    def test_create_document(self, mock_post):
        # Mock successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"results": [{"id": "123"}]}

        data = {
            "title": "Test Doc",
            "summary": "Summary",
            "action_items": []
        }
        
        response = self.client.create_document("meeting_notes", "Test Doc", data, "/tmp/test.pdf")
        
        self.assertIsNotNone(response)
        mock_post.assert_called_once()
        # Verify mutation structure
        args, kwargs = mock_post.call_args
        self.assertIn("mutations", kwargs['json'])
        self.assertEqual(kwargs['json']['mutations'][0]['create']['title'], "Test Doc")

    @patch('services.sanity.requests.get')
    def test_get_documents(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": [{"title": "Doc 1"}, {"title": "Doc 2"}]
        }

        docs = self.client.get_documents()
        self.assertEqual(len(docs), 2)
        mock_get.assert_called_once()
        
        # Verify GROQ query
        args, kwargs = mock_get.call_args
        self.assertIn("generatedDocument", kwargs['params']['query'])

    @patch('services.sanity.requests.get')
    def test_get_open_tasks(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": [{"title": "Doc 1", "tasks": [{"task": "Do X"}]}]
        }

        tasks = self.client.get_open_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0]['tasks']), 1)

if __name__ == '__main__':
    unittest.main()
