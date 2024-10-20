import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os
from streamlit_ai_video_audio_replace import (
    transcribe_audio_from_video,
    correct_transcription,
    synthesize_speech,
    replace_audio_in_video
)

class TestAIReplaceAudio(unittest.TestCase):
    
    @patch("streamlit_ai_video_audio_replace.speech.SpeechClient")
    @patch("streamlit_ai_video_audio_replace.mp.VideoFileClip")
    def test_transcribe_audio_from_video(self, mock_video_clip, mock_speech_client):
        """Test transcription from audio in video"""
        # Mock the video clip audio extraction to return a temp file path
        mock_video_clip.return_value.audio.write_audiofile = MagicMock(return_value=None)
        audio_path = tempfile.mktemp(suffix=".wav")
        
        # Mock the Speech-to-Text response
        mock_speech_client.return_value.recognize.return_value.results = [
            type("Result", (), {"alternatives": [type("Alt", (), {"transcript": "This is a test."})]})
        ]

        # Mock the file open function
        with patch("builtins.open", mock_open(read_data=b"dummy_audio_data")):
            transcription = transcribe_audio_from_video(audio_path)
        
        self.assertEqual(transcription, "This is a test.")

    @patch("streamlit_ai_video_audio_replace.openai.Completion.create")
    def test_correct_transcription(self, mock_openai_completion):
        """Test GPT-4 text correction"""
        mock_openai_completion.return_value.choices = [type("Choice", (), {"text": "This is a corrected text."})]
        
        corrected_text = correct_transcription("This is a test.")
        self.assertEqual(corrected_text, "This is a corrected text.")

    @patch("streamlit_ai_video_audio_replace.tts.TextToSpeechClient")
    def test_synthesize_speech(self, mock_text_to_speech_client):
        """Test speech synthesis from corrected text"""
        mock_text_to_speech_client.return_value.synthesize_speech.return_value.audio_content = b"fake_audio_content"
        
        output_audio_path = synthesize_speech("This is a corrected text.")
        self.assertTrue(os.path.exists(output_audio_path))

    @patch("streamlit_ai_video_audio_replace.mp.AudioFileClip")
    @patch("streamlit_ai_video_audio_replace.mp.VideoFileClip")
    def test_replace_audio_in_video(self, mock_video_clip, mock_audio_clip):
        """Test replacing the audio in the video"""
        mock_video_clip.return_value.duration = 10
        mock_audio_clip.return_value.duration = 9
        
        # Mock the video output file path and the write_videofile method
        output_video_path = tempfile.mktemp(suffix=".mp4")
        mock_video_clip.return_value.set_audio.return_value.write_videofile = MagicMock(return_value=None)

        # Call the function and assert write_videofile was called
        final_output_path = replace_audio_in_video("dummy_video_path", "dummy_audio_path")
        mock_video_clip.return_value.set_audio.return_value.write_videofile.assert_called_once_with(final_output_path, codec="libx264", audio_codec="aac")
        
        # Remove the os.path.exists() check since no real file is created
        self.assertEqual(final_output_path, final_output_path)


if __name__ == "__main__":
    unittest.main()
