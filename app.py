import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AuraNexus: Ultimate Destination", layout="wide")

# You will need to get a FREE API Key from https://aistudio.google.com/
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 2. THE AI ENGINE ---
def generate_content(level, board, goal, chapter, pdf_text=None):
    context = pdf_text if pdf_text else "Use your internal high-quality academic database."
    
    prompt = f"""
    Act as a strict Senior Examiner for {board} and a top-tier {goal} Coach.
    Target Level: {level}.
    Chapter: {chapter}.
    
    Context Data: {context[:10000]} # Processing first chunk of data
    
    Generate the ULTIMATE STUDY PACKET:
    1. SMART NOTES: 
       - 'Deep Dive': Technical, detailed notes with specific terminology for {board}.
       - 'Flash Notes': 10 bullet points for 2-minute revision.
    2. VISUALS: Create a text-based Mindmap using levels/hierarchy.
    3. THE SURESHOT 100+:
       - 36 Reasoning Questions (Give reasons/Conceptual) for {board}.
       - 36 Numerical Questions (Board Level) with step-marking.
       - 36 Competitive MCQs ({goal} Level) with shortcuts/tricks.
    4. CHEAT SHEET: All formulas, constants, and 'Teacher's Secret' tips.
    
    Tone: Professional, high-efficiency, and strict.
    """
    response = model.generate_content(prompt)
    return response.text

# --- 3. THE USER INTERFACE (Frontend) ---
st.title("🌌 AuraNexus: The Ultimate Academic Destination")
st.markdown("---")

# Sidebar for Identity Selection
with st.sidebar:
    st.header("👤 User Persona")
    era = st.selectbox("Select Your Era", ["10th", "11th-12th (School/Boards)", "University", "PhD"])
    
    if era == "11th-12th (School/Boards)":
        board = st.radio("Board", ["ISC", "CBSE"])
        goal = st.radio("Primary Goal", ["Boards", "JEE", "NEET", "CUET"])
    else:
        board = "N/A"
        goal = "Academic Research"

    st.divider()
    strict_mode = st.toggle("Strict Examiner Mode", value=True)

# Main Dashboard
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📁 Input Source")
    input_type = st.radio("How to load chapter?", ["Chapter Name Only", "Upload PDF (Max 200 pgs)"])
    
    pdf_content = ""
    chapter_name = st.text_input("Enter Chapter Name", placeholder="e.g. Work Power Energy")
    
    if input_type == "Upload PDF (Max 200 pgs)":
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            with st.spinner("Analyzing PDF..."):
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in doc:
                    pdf_content += page.get_text()
                st.success(f"Processed {len(doc)} pages successfully!")

    if st.button("🚀 GENERATE ULTIMATE NOTES"):
        if chapter_name:
            with st.spinner("AI Agents are crafting your Sureshot Packet..."):
                result = generate_content(era, board, goal, chapter_name, pdf_content)
                st.session_state['output'] = result
        else:
            st.error("Please enter a chapter name.")

with col2:
    st.subheader("📖 Your Study Destination")
    if 'output' in st.session_state:
        st.markdown(st.session_state['output'])
    else:
        st.info("Your smart notes and Sureshot 36 questions will appear here.")

# --- 4. DOUBT BUSTER CHAT ---
st.divider()
st.subheader("💬 24/7 Doubt Buster")
user_doubt = st.text_input("Ask a doubt from this chapter...")
if user_doubt:
    response = model.generate_content(f"Context: {chapter_name}. Doubt: {user_doubt}. Answer briefly and strictly.")
    st.write(response.text)
