import os
import requests
import json
from core.config import DEEPGRAM_API_KEY

DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"

class DeepgramClient:
    def __init__(self):
        self.api_key = DEEPGRAM_API_KEY
        if not self.api_key:
            print("⚠️ Deepgram API Key missing. Transcription will fail.")

    def _get_headers(self, content_type="audio/*"):
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": content_type
        }

    def _get_params(self):
        return {
            "model": "nova-2",
            "smart_format": "true",
            "punctuate": "true",
            "diarize": "true",       # Enable speaker labeling
            "utterances": "true",    # Split by speaker/pause
            "sentiment": "true",     # Detect sentiment
            "language": "en",
        }

    def transcribe_bytes(self, audio_data: bytes, filename: str = "upload.mp3") -> dict:
        """
        Transcribes audio bytes and returns a structured response.
        """
        print(f"🎧 Transcribing audio ({len(audio_data)} bytes) with Deepgram...")
        
        try:
            response = requests.post(
                DEEPGRAM_URL,
                params=self._get_params(),
                headers=self._get_headers(),
                data=audio_data,
                timeout=60
            )
            response.raise_for_status()
            return self._process_response(response.json())
        except Exception as e:
            print(f"❌ Deepgram Transcription Failed: {e}")
            return {"transcript": "", "error": str(e)}

    def transcribe_file(self, file_path: str) -> dict:
        """
        Transcribes a local audio file.
        """
        if not os.path.exists(file_path):
            return {"transcript": "", "error": "File not found"}

        try:
            with open(file_path, "rb") as audio:
                response = requests.post(
                    DEEPGRAM_URL,
                    params=self._get_params(),
                    headers=self._get_headers(),
                    data=audio,
                    timeout=60
                )
            response.raise_for_status()
            return self._process_response(response.json())
        except Exception as e:
            print(f"❌ Deepgram Transcription Failed: {e}")
            return {"transcript": "", "error": str(e)}

    def _process_response(self, data: dict) -> dict:
        """
        Extracts transcript, speaker-labeled text, and sentiment.
        """
        try:
            result = data["results"]
            channels = result.get("channels", [{}])[0]
            alternatives = channels.get("alternatives", [{}])[0]
            
            # 1. Plain Text
            raw_transcript = alternatives.get("transcript", "")
            
            # 2. Speaker-Labeled Transcript (Diarized)
            # Iterate through words/utterances to reconstruct "Speaker X: ..."
            diarized_transcript = ""
            current_speaker = None
            
            words = alternatives.get("words", [])
            if words:
                for word in words:
                    speaker = word.get("speaker", 0)
                    text = word.get("word", "")
                    punctuated = word.get("punctuated_word", text)
                    
                    if speaker != current_speaker:
                        if current_speaker is not None:
                            diarized_transcript += "\n\n"
                        diarized_transcript += f"Speaker {speaker}: "
                        current_speaker = speaker
                    
                    diarized_transcript += f"{punctuated} "
            else:
                # Fallback if no word-level info
                diarized_transcript = raw_transcript

            return {
                "transcript": raw_transcript,
                "formatted_transcript": diarized_transcript.strip(),
                "confidence": alternatives.get("confidence", 0),
                "words": words
            }

        except Exception as e:
            print(f"❌ Error processing Deepgram response: {e}")
            return {"transcript": "", "error": str(e)}

# Singleton
deepgram_client = DeepgramClient()
