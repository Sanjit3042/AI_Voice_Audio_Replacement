
# AI Video Audio Replacement PoC

This project is a Proof of Concept (PoC) that processes a video file by transcribing its audio, correcting any grammatical mistakes using GPT-4, generating a new AI-generated voice, and replacing the original audio in the video. The app is built using **Streamlit** and integrates with **Google Cloud** and **Azure OpenAI**.

## Features
1. **Transcription**: Extracts audio from the uploaded video and transcribes it using Google's Speech-to-Text API.
2. **Text Correction**: Corrects grammatical mistakes, removes filler words (e.g., "umms", "hmms"), and improves fluency using GPT-4 via Azure OpenAI.
3. **Text-to-Speech**: Converts the corrected transcription to speech using Google's Text-to-Speech API with the "Journey" voice model.
4. **Audio Replacement**: Replaces the original video’s audio with the newly generated AI voice while maintaining sync between video and audio.
5. **Streamlit UI**: Provides an interface to upload the video, process it, and download the output.

## Prerequisites

Before running the application, you will need the following:
1. **Google Cloud** credentials:
    - Enable **Google Speech-to-Text** and **Google Text-to-Speech** APIs.
    - Download the **Service Account Key** in JSON format.
    - Set the environment variable for the credentials:
      ```bash
      export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_google_credentials.json"
      ```

2. **Azure OpenAI API Key**:
    - Access to the GPT-4 model via **Azure OpenAI**.
    - Set the API key in your code:
      ```python
      openai.api_key = "your_azure_openai_gpt_4o_key"
      ```

## Setup Instructions

### 1. Clone the Repository
Clone the project repository or download the source code.

```bash
git clone https://github.com/your-username/ai-video-audio-replace-poc.git
cd ai-video-audio-replace-poc
```

### 2. Install Dependencies
Install the required Python packages using `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Run the Application
Run the Streamlit app locally:

```bash
streamlit run streamlit_ai_video_audio_replace.py
```

This will open the app in your default web browser. If it doesn’t open automatically, you can manually visit `http://localhost:8501/`.

## How to Use the App

1. **Upload a Video**: 
   - Use the UI to upload a video file (formats like `.mp4`, `.mov`, `.avi`).
   
2. **Processing**:
   - The app will extract the audio, transcribe it, and use GPT-4 to correct the transcription.
   - It will then generate a new AI voice and replace the original video’s audio with it.
   
3. **Download the Result**:
   - Once processing is complete, the app will provide a link to download the video with the replaced audio.

## Example Workflow
1. **Upload a video** (e.g., a speech with grammatical mistakes or filler words like "umms").
2. **Transcription**: The app transcribes the audio.
3. **Text Correction**: The transcribed text is corrected using GPT-4 to remove errors and filler words.
4. **Text-to-Speech**: The corrected text is synthesized using Google Text-to-Speech (Journey model).
5. **Download**: The final video, with the new AI-generated voice, is available for download.

## File Structure

```
├── streamlit_ai_video_audio_replace.py    # Main Streamlit app
├── test_streamlit_ai_video_audio_replace.py # Unit tests
├── requirements.txt                      # Required dependencies
└── README.md                             # Project documentation
```

## Testing

Unit tests are provided to ensure each function (transcription, correction, synthesis, and audio replacement) works as expected. You can run the tests using:

```bash
python -m unittest test_streamlit_ai_video_audio_replace.py
```

## Key Libraries Used
- **Streamlit**: For the web interface.
- **MoviePy**: For video and audio manipulation.
- **Google Cloud Speech-to-Text**: For transcribing audio from the video.
- **Google Cloud Text-to-Speech**: For generating the corrected AI voice.
- **OpenAI GPT-4**: For text correction and grammar improvements.

## Future Improvements
- **Improved Sync**: More advanced handling of sync between video and generated audio.
- **Custom Voices**: Support for additional Text-to-Speech models.
- **Error Handling**: More comprehensive handling of edge cases like long pauses or interruptions in the audio.

## Contact Information
If you have any questions or issues with the project, feel free to reach out.

- **Email**: your.email@example.com

## License
This project is for educational and non-commercial use only.
