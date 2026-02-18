import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.getcwd()))
from services.deepgram import DeepgramClient

class TestDeepgramClient(unittest.TestCase):
    def setUp(self):
        self.client = DeepgramClient()
        self.client.api_key = "fake-key"

    @patch('services.deepgram.requests.post')
    def test_transcribe_bytes(self, mock_post):
        # Mock successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "results": {
                "channels": [{
                    "alternatives": [{
                        "transcript": "Hello world.",
                        "words": [
                            {"word": "Hello", "punctuated_word": "Hello", "speaker": 0},
                            {"word": "world", "punctuated_word": "world.", "speaker": 0}
                        ]
                    }]
                }]
            }
        }

        result = self.client.transcribe_bytes(b"fake-audio")
        
        self.assertIn("transcript", result)
        self.assertIn("formatted_transcript", result)
        self.assertEqual(result["transcript"], "Hello world.")
        self.assertEqual(result["formatted_transcript"], "Speaker 0: Hello world.")

    @patch('services.deepgram.requests.post')
    def test_transcribe_file(self, mock_post):
        # Mock successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
             "results": {
                "channels": [{
                    "alternatives": [{
                        "transcript": "Test file.",
                        "words": []
                    }]
                }]
            }
        }
        
        # We need to mock open() too, but honestly easier to just create a dummy file
        dummy_file = "test_audio_stub.mp3"
        with open(dummy_file, "wb") as f:
            f.write(b"data")
            
        try:
            result = self.client.transcribe_file(dummy_file)
            self.assertEqual(result["transcript"], "Test file.")
        finally:
            if os.path.exists(dummy_file):
                os.remove(dummy_file)

if __name__ == '__main__':
    unittest.main()
