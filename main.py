import streamlit as st
import os
import random
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from elevenlabs.client import ElevenLabs
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

# Load API keys from Streamlit secrets
google_api_keys = list(st.secrets["GOOGLE_API_KEY"].values())
google_api_key = google_api_keys[0]
os.environ["GOOGLE_API_KEY"] = google_api_key

elevenlabs_api_keys = list(st.secrets["ELEVENLABS_API_KEY"].values())
if not elevenlabs_api_keys:
    st.error("No ElevenLabs API keys found. Please check Streamlit secrets.")
    st.stop()
selected_elevenlabs_api_key = random.choice(elevenlabs_api_keys)

# Google Drive Video ID
drive_video_id = "1ncTcikpiBRvM1vVrBKY3vYpyQDqhlhkW"
video_url = f"https://drive.google.com/uc?export=download&id={drive_video_id}"
video_path = "input_video.mp4"


# Set custom page title and icon
st.set_page_config(
    page_title="BRAINROT AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        .css-1rs6os {visibility: hidden;}
        .css-17ziqus {visibility: hidden;}
        .css-14xtw13 e8zbici0 {visibility: hidden;}
        section[data-testid="stSidebar"] {display: none;}
        div[data-testid="stToolbar"] {display: none;}
        div[data-testid="stDecoration"] {display: none;}
        div[data-testid="stStatusWidget"] {display: none;}
        #root > div:nth-child(1) > div > div > div > div > section.css-1lcbmhc.e1fqkh3o0 > div.css-1adrfps.e1fqkh3o3 {display: none;}
    </style>
""", unsafe_allow_html=True)

# Main content container
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5em; margin-bottom: 0.5rem;'>🧠 BRAINROT AI</h1>
        <h3 style='font-size: 1.5em; color: #ff6b6b; margin-bottom: 2rem;'>Transform boring PDFs into viral-worthy video content! 🔥</h3>
        <div style='max-width: 800px; margin: 0 auto; padding: 2rem; background: rgba(255, 255, 255, 0.05); border-radius: 15px;'>
            <blockquote style='border-left: 4px solid #ff6b6b; padding-left: 1rem; margin: 1rem 0;'>
                <p style='font-style: italic; font-size: 1.2em;'>"Where AI meets chaos, and boring PDFs become internet gold!" 🚀</p>
            </blockquote>
        </div>
    </div>
""", unsafe_allow_html=True)

# Define Model A
model_a = "models/gemini-1.5-pro-latest"

def get_model_a():
    return model_a

llm_a = ChatGoogleGenerativeAI(model=get_model_a(), temperature=0.7)

prompt = ChatPromptTemplate.from_template(
    """
    🚀 **Brainrot Mode Activated!** 🤯🔥  
    Your mission: **Take this document and rewrite it in the most chaotic, meme-fueled, internet-infused way possible.**  
    No boring explanations. No robotic summaries. **Just straight-up high-energy, fun, and slightly unhinged storytelling.**  

    ## 🛑 RULES:  
    - **NO academic or formal tone.** If it sounds like a textbook, delete it. 🚮  
    - **Use slang, emojis, and meme references** but don’t overdo it. We want **fun, not gibberish.**  
    - **Be concise and punchy.** Get the point across FAST and with maximum impact.  
    - **Inject humor and hype.** Imagine you're explaining this to a friend who has the attention span of a goldfish. 🐠✨  
    - **Stay true to the document** but **you can add a *tiny* sprinkle of extra context if it makes things smoother or funnier.**  
    - **DO NOT introduce new concepts.** You can rephrase creatively, but **stick to what’s in the text.**  
    - **NO HEADINGS.** The output should be a **single, continuous paragraph**—no sections, no titles, no formatting.    

    ## 🏆 EXAMPLES:  
    **Original:** "The Transformer model replaces recurrent neural networks with self-attention mechanisms, leading to increased parallelization and improved training efficiency."  
    **Brainrot:** "BRO, RNNs are old news. Transformers just **stare at everything all at once** and go **big-brain mode.** 🧠💥 No waiting, no stress—just **pure speed and efficiency.** 🚀"  

    **Original:** "Experiments show the model performs significantly better in machine translation tasks compared to prior architectures."  
    **Brainrot:** "This thing didn’t just **win**—it **wrecked the competition.** 💀💥 BLEU scores went **through the roof**, and old models are now **collecting dust.** 🚀📈"  

    Now, **go forth and unleash brainrot magic.**  
    Keep it wild, but **use your brain a little—very little.**  

    Context:  
    {context}  
    """
)

def process_uploaded_pdf(uploaded_file):
    if uploaded_file is None:
        st.error("⚠️ Please upload a PDF file")
        return

    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader("temp_uploaded.pdf")
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)

    context = " ".join([doc.page_content for doc in final_documents])
    document_chain = create_stuff_documents_chain(llm_a, prompt)
    retriever = FAISS.from_documents(final_documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001")).as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({'input': "all", 'context': context})
    return response['answer']

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.05); padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;'>
            <h4 style='margin-bottom: 1rem; color: #ff6b6b;'>📂 Upload Your PDF</h4>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner('🤖 Analyzing your PDF with maximum chaos...'):
            brainrot_text = process_uploaded_pdf(uploaded_file)
        
        st.markdown("""
            <div style='text-align: center; margin: 2rem 0;'>
                <p style='color: #ff6b6b; font-size: 1.2em;'>🎉 PDF processed! Ready to create your viral video?</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎥 Generate Video with Audio", key="generate_video"):
            try:
                # Create a big bold header for the process
                st.markdown("""
                    <div style='padding: 2rem; background: linear-gradient(45deg, rgba(255, 107, 107, 0.2), rgba(255, 142, 83, 0.2)); 
                              border-radius: 15px; margin: 2rem 0; text-align: center; 
                              border: 2px solid rgba(255, 107, 107, 0.3);'>
                        <h2 style='margin: 0; background: linear-gradient(45deg, #ff6b6b, #ff8e53); 
                                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                                   font-size: 2em;'>🎥 Creating Your Viral Video</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                # Create containers for progress
                progress_container = st.container()
                with progress_container:
                    st.markdown("""
                        <style>
                            .stProgress > div > div {
                                height: 20px !important;
                                background: linear-gradient(45deg, #ff6b6b, #ff8e53) !important;
                            }
                            .stProgress > div {
                                background-color: rgba(255, 255, 255, 0.1) !important;
                            }
                        </style>
                    """, unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    status = st.empty()
                
                # Download the video if needed
                if not os.path.exists(video_path):
                    status.markdown("""
                        <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                                  border-radius: 10px; border-left: 4px solid #ff6b6b;'>
                            <p style='margin: 0; color: #ff6b6b; font-size: 1.1em;'>💾 Downloading background video...</p>
                        </div>
                    """, unsafe_allow_html=True)
                    progress_bar.progress(10)
                    try:
                        response = requests.get(video_url, stream=True)
                        if response.status_code == 200:
                            with open(video_path, "wb") as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    f.write(chunk)
                            progress_bar.progress(30)
                        else:
                            st.error("Failed to download video from Google Drive.")
                            st.stop()
                    except Exception as e:
                        st.error(f"Error downloading video: {e}")
                        st.stop()
                
                # Generate audio
                status.markdown("""
                    <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                              border-radius: 10px; border-left: 4px solid #ff6b6b;'>
                        <p style='margin: 0; color: #ff6b6b; font-size: 1.1em;'>🎙️ Converting text to speech...</p>
                    </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(40)
                
                # Initialize ElevenLabs Client
                client = ElevenLabs(api_key=selected_elevenlabs_api_key)
                
                # Convert brainrot text to speech
                audio_generator = client.text_to_speech.convert(
                    text=brainrot_text,
                    voice_id="pNInz6obpgDQGcFmaJgB",
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                
                # Save the audio file
                audio_path = "output_audio.mp3"
                with open(audio_path, "wb") as f:
                    f.write(b"".join(audio_generator))
                
                progress_bar.progress(60)

                # Process video
                status.markdown("""
                    <div style='padding: 1rem; background: rgba(255, 255, 255, 0.05); 
                              border-radius: 10px; border-left: 4px solid #ff6b6b;'>
                        <p style='margin: 0; color: #ff6b6b; font-size: 1.1em;'>🎥 Mixing video and audio...</p>
                    </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(70)
                
                # Load video and audio
                video_clip = VideoFileClip(video_path)
                audio_clip = AudioFileClip(audio_path)

                # Trim the video to match the audio duration
                trimmed_video = video_clip.subclipped(0, min(video_clip.duration, audio_clip.duration))
                
                # Set the trimmed video's audio
                final_audio = CompositeAudioClip([audio_clip])
                final_video = trimmed_video.with_audio(final_audio)
                
                # Save the final video
                final_video_path = "final_video.mp4"
                final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")
                
                # Show completion
                progress_bar.progress(100)
                status.markdown("""
                    <div style='padding: 1rem; background: rgba(39, 174, 96, 0.1); 
                              border-radius: 10px; border-left: 4px solid #27ae60;'>
                        <p style='margin: 0; color: #27ae60; font-size: 1.2em; font-weight: bold;'>🎉 Video created successfully!</p>
                    </div>
                """, unsafe_allow_html=True)

                # Add CSS to make video smaller
                st.markdown("""
                    <style>
                        video {
                            width: 50% !important;  /* Adjust width */
                            height: auto !important;
                        }
                    </style>
                """, unsafe_allow_html=True)

                st.video(final_video_path)

                with open(final_video_path, "rb") as f:
                    st.download_button("Download Final Video", f, file_name="final_video.mp4")
            except Exception as e:
                st.error(f"Error: {e}")




st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #ff8e53) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 1rem 3rem !important;
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        font-size: 1.1em !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin: 1rem 0 !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        border: 2px dashed rgba(255, 107, 107, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .uploadedFile:hover {
        border-color: #ff6b6b !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Progress and spinner styling */
    .stProgress > div > div {
        background-color: #ff6b6b !important;
    }
    
    .stSpinner > div {
        border-top-color: #ff6b6b !important;
    }
    
    /* Text styling */
    .stMarkdown p {
        color: #f8f9fa !important;
        line-height: 1.6 !important;
    }
    
    .stMarkdown blockquote {
        border-left: 4px solid #ff6b6b !important;
        background: rgba(255, 107, 107, 0.1) !important;
        padding: 1.5rem !important;
        border-radius: 10px !important;
        margin: 2rem 0 !important;
    }
    
    /* Video player styling */
    video {
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Download button styling */
    .stDownloadButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049) !important;
    }
</style>
""", unsafe_allow_html=True)
