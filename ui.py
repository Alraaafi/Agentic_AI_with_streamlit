import streamlit as st
from youtube_analyzer import build_youtube_agent

st.set_page_config(
    page_title="Youtube Video Analyzer",
    layout="centered"
)

st.title("🎥 AI Youtube Video Analyzer")

@st.cache_resource
def get_agent():
    return build_youtube_agent()


try:
    agent = get_agent()
except RuntimeError as error:
    st.error(str(error))
    st.info("Create a Gemini API key at https://aistudio.google.com/app/apikey and put it in .env as GOOGLE_API_KEY=...")
    st.stop()

# input box
video_url = st.text_input("Enter Youtube Video Link") # str
button = st.button("Analyze Video") # True/False

if video_url and button:
    try:
        with st.spinner("Analyzing video...."):
            response = agent.run(
                f"Analyze this video: {video_url}"
            )
    except Exception as error:
        if "401" in str(error) or "UNAUTHENTICATED" in str(error):
            st.error("Gemini authentication failed.")
            st.info("Replace GOOGLE_API_KEY in .env with a Google AI Studio API key, then restart Streamlit.")
        else:
            st.error(f"Analysis failed: {error}")
    else:
        st.markdown("Analysis Report of Video:")
        st.markdown(response.content)