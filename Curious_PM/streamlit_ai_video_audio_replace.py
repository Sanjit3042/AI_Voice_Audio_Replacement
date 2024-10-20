# File: streamlit_ai_video_audio_replace.py

import streamlit as st
import tempfile
import moviepy.editor as mp
import openai
import google.cloud.texttospeech as tts
from google.cloud import speech_v1p1beta1 as speech
import os

# Setup Google Cloud credentials for Text-to-Speech and Speech-to-Text
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_google_credentials.json"

# Setup Azure OpenAI GPT-4o credentials
openai.api_key = "your_azure_openai_gpt_4o_key"

def transcribe_audio_from_video(video_path):
    """Extracts audio from the video and transcribes it using Google Speech-to-Text."""
    clip = mp.VideoFileClip(video_path)
    audio_path = tempfile.mktemp(suffix=".wav")
    clip.audio.write_audiofile(audio_path)

    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription

def correct_transcription(transcription):
    """Uses GPT-4o to correct grammatical errors and filler words from transcription."""
    prompt = f"Please correct the following transcription by removing any grammatical errors, 'umms', 'hmms', and making it fluent:\n\n{transcription}"

    response = openai.Completion.create(
        model="gpt-4o",  # Assuming GPT-4o in Azure
        prompt=prompt,
        max_tokens=1000
    )

    corrected_text = response.choices[0].text.strip()
    return corrected_text

def synthesize_speech(text):
    """Uses Google's Text-to-Speech API to convert corrected text to speech."""
    client = tts.TextToSpeechClient()
    input_text = tts.SynthesisInput(text=text)
    
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-JennyNeural",  # Change to the 'Journey' voice if available
        ssml_gender=tts.SsmlVoiceGender.FEMALE
    )

    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    output_audio_path = tempfile.mktemp(suffix=".wav")
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)

    return output_audio_path

def replace_audio_in_video(video_path, new_audio_path):
    """Replaces the audio in the original video with the generated audio."""
    clip = mp.VideoFileClip(video_path)
    new_audio = mp.AudioFileClip(new_audio_path)
    
    # Adjust audio duration if necessary
    new_audio = new_audio.subclip(0, min(clip.duration, new_audio.duration))
    final_clip = clip.set_audio(new_audio)
    
    output_video_path = tempfile.mktemp(suffix=".mp4")
    final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path

# Streamlit UI
st.title("AI Video Audio Replacement")

uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    with st.spinner("Processing your video..."):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_video:
            temp_video.write(uploaded_video.read())
            temp_video_path = temp_video.name
        
        # Step 1: Transcribe the video audio
        transcription = transcribe_audio_from_video(temp_video_path)
        st.write("Original Transcription:", transcription)

        # Step 2: Correct the transcription
        corrected_text = correct_transcription(transcription)
        st.write("Corrected Transcription:", corrected_text)

        # Step 3: Synthesize the corrected text into speech
        new_audio_path = synthesize_speech(corrected_text)

        # Step 4: Replace the original video audio with the new audio
        final_video_path = replace_audio_in_video(temp_video_path, new_audio_path)

        # Step 5: Provide the user with a downloadable video
        st.video(final_video_path)
        with open(final_video_path, "rb") as video_file:
            btn = st.download_button(
                label="Download Corrected Video",
                data=video_file,
                file_name="corrected_video.mp4",
                mime="video/mp4"
            )
