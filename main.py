import streamlit as st
import os
import random
import requests
from langchain_groq import ChatGroq
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
groq_api_keys = list(st.secrets["GROQ_API_KEY"].values())
selected_groq_api_key = random.choice(groq_api_keys)

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

elevenlabs_api_keys = list(st.secrets["ELEVENLABS_API_KEY"].values())
if not elevenlabs_api_keys:
    st.error("No ElevenLabs API keys found. Please check Streamlit secrets.")
    st.stop()
selected_elevenlabs_api_key = random.choice(elevenlabs_api_keys)

# Google Drive Video ID
drive_video_id = "1ncTcikpiBRvM1vVrBKY3vYpyQDqhlhkW"
video_url = f"https://drive.google.com/uc?export=download&id={drive_video_id}"
video_path = "input_video.mp4"

# Download the video
try:
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(video_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        st.error("Failed to download video from Google Drive.")
        st.stop()
except Exception as e:
    st.error(f"Error downloading video: {e}")
    st.stop()


# Set custom page title and icon
st.set_page_config(page_title="BrainrotAI - Meme-Powered Summarization", page_icon="🧠")



st.title("🧠 BrainrotAI")

# Define Model A
model_a = "gemma2-9b-it"

def get_model_a():
    return model_a

llm_a = ChatGroq(groq_api_key=selected_groq_api_key, model_name=get_model_a())

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

uploaded_file = st.file_uploader("📂 Upload a PDF Document", type=["pdf"])

if uploaded_file is not None:
    brainrot_text = process_uploaded_pdf(uploaded_file)

    if st.button("Generate Video with Audio"):
        try:
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
            
            st.success("Video processed successfully!")

            # Add CSS to make video smaller
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





            st.video(final_video_path)

            with open(final_video_path, "rb") as f:
                st.download_button("Download Final Video", f, file_name="final_video.mp4")
        except Exception as e:
            st.error(f"Error: {e}")




footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Made with ❤️ by Daksh Arora</p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)
