# BrainrotAI 🧠

> Transform boring PDFs into viral-worthy video content!

BrainrotAI is a cutting-edge Streamlit application that transforms boring PDF documents into engaging, meme-worthy video content by combining AI-powered text transformation, text-to-speech generation, and video processing. The app uses multiple AI services including Groq, Google's Generative AI, and ElevenLabs to create an entertaining and dynamic presentation of document content.

## 🚀 Features

- PDF document upload and processing
- AI-powered text transformation to casual, engaging content
- Text-to-speech conversion using ElevenLabs
- Automatic video generation with synchronized audio
- Download capability for the final video
- Responsive web interface

## 📋 Prerequisites

Before running this application, you'll need:

- Python 3.7 or higher
- Streamlit
- Required API keys:
  - Groq API key
  - Google API key
  - ElevenLabs API key

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required dependencies:
```bash
pip install streamlit langchain-groq langchain google-generative-ai elevenlabs moviepy faiss-cpu
```

3. Create a `config.json` file in the root directory with your API keys:
```json
{
    "GROQ_API_KEY": {
        "key1": "your-groq-api-key"
    },
    "GOOGLE_API_KEY": "your-google-api-key",
    "ELEVENLABS_API_KEY": {
        "key1": "your-elevenlabs-api-key"
    }
}
```

## 🎮 Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload a PDF document using the file uploader

4. Click "Generate Video with Audio" to process the document and create the video

5. Download the final video using the download button

## 🔧 Configuration

### Model Configuration
- Default LLM: Gemma 2 9B IT
- Text Splitter: RecursiveCharacterTextSplitter with:
  - Chunk size: 1000
  - Chunk overlap: 200

### ElevenLabs Configuration
- Voice ID: pNInz6obpgDQGcFmaJgB
- Model: eleven_multilingual_v2
- Output format: mp3_44100_128

## 📦 Dependencies

- streamlit
- langchain-groq
- langchain
- google-generative-ai
- elevenlabs
- moviepy
- faiss-cpu
- requests

## ⚠️ Important Notes

1. The application requires a stable internet connection for API calls and video processing
2. Large PDF files may take longer to process
3. Video generation time depends on the length of the text and system resources
4. Make sure you have sufficient disk space for temporary video and audio files

## 🔐 Security

- API keys are loaded from a separate config.json file
- Keys are randomly selected from available keys to distribute usage
- The application includes basic error handling for API failures

## 💡 Customization

You can customize the following aspects:

1. Prompt Template: Modify the ChatPromptTemplate in the code to change the style of text transformation
2. Video Source: Update the Google Drive video ID to use a different background video
3. Voice Settings: Change the ElevenLabs voice ID or model for different voice characteristics
4. Text Splitting: Adjust chunk_size and chunk_overlap parameters for different text processing lengths

## 🐛 Troubleshooting

Common issues and solutions:

1. **API Key Errors**: Ensure all API keys in config.json are valid and properly formatted
2. **Video Download Fails**: Check internet connection and Google Drive link accessibility
3. **Memory Issues**: Reduce chunk_size if processing large PDFs
4. **Audio Sync Issues**: Verify that both video and audio files are generated correctly

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 🙏 Acknowledgments

- Groq for LLM API
- Google for Generative AI
- ElevenLabs for text-to-speech
- Streamlit for the web framework
