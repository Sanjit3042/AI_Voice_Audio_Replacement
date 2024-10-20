import streamlit as st
import moviepy.editor as mp
import requests
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import tempfile

# 1. Streamlit UI for Video Upload
st.title('AI-Powered Video Audio Replacement')
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save video temporarily
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_video.write(uploaded_file.read())

    # 2. Extract Audio from Video
    video = mp.VideoFileClip(temp_video.name)
    audio = video.audio
    temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    audio.write_audiofile(temp_audio_path)
    
    # 3. Transcribe using Google Speech-to-Text
    client = speech.SpeechClient()
    
    with open(temp_audio_path, "rb") as audio_file:
        content = audio_file.read()
    
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    
    audio = speech.RecognitionAudio(content=content)
    response = client.recognize(config=audio_config, audio=audio)

    # Extract the transcription
    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    # 4. Send transcription to GPT-4o for correction
    api_key = '22ec84421ec24230a3638d1b51e3a7dc'  # Your Azure OpenAI API key
    url = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    
    prompt = f"Please correct this transcription for grammar: {transcription}"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    response = requests.post(url, json=data, headers=headers)
    corrected_text = response.json()["choices"][0]["message"]["content"]

    # 5. Convert corrected text to speech using Google TTS (Journey model)
    tts_client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=corrected_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Journey"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the generated audio to a file
    temp_speech_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    with open(temp_speech_audio.name, "wb") as out:
        out.write(response.audio_content)

    # 6. Merge new audio with the original video
    new_audio = mp.AudioFileClip(temp_speech_audio.name)
    video_with_new_audio = video.set_audio(new_audio)
    
    # Save the final video
    output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_with_new_audio.write_videofile(output_video_path.name)

    # 7. Download option for the user
    st.video(output_video_path.name)
    st.download_button("Download the processed video", data=open(output_video_path.name, "rb"), file_name="processed_video.mp4")

