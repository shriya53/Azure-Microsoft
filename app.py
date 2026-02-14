import streamlit as st
import whisper
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import re
import os

# PAGE CONFIG
st.set_page_config(
    page_title="AI Voice Notes Generator",
    page_icon="🎙️",
    layout="centered"
)

# CUSTOM CSS 
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.gradient-text {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #2563eb, #9333ea, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 30px;
}

.section-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

.stButton>button {
    background: linear-gradient(90deg, #2563eb, #9333ea);
    color: white;
    border-radius: 12px;
    padding: 10px 25px;
    font-weight: 600;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="gradient-text">🎙️ AI Voice to Smart Notes</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload audio/video and generate structured notes instantly</div>', unsafe_allow_html=True)

# LOAD WHISPER MODEL (Cached)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

# SMART BULLET FORMATTER 
def structure_notes(text):

    sections = {
        "🌍 Causes & Background": [],
        "⚔ Military Mobilization": [],
        "🚢 War Efforts": [],
        "🏆 Victory & Legacy": []
    }

    sentences = re.split(r'(?<=[.!?]) +', text)

    for s in sentences:
        s = s.strip()
        if len(s) < 25:
            continue

        lower = s.lower()

        if "germany" in lower or "declaration" in lower or "submarine" in lower:
            sections["🌍 Causes & Background"].append(s)

        elif "army" in lower or "million" in lower or "soldier" in lower:
            sections["⚔ Military Mobilization"].append(s)

        elif "transported" in lower or "organization" in lower:
            sections["🚢 War Efforts"].append(s)

        elif "victory" in lower or "conquered" in lower or "world war" in lower:
            sections["🏆 Victory & Legacy"].append(s)

    formatted = ""

    for heading, points in sections.items():
        if points:
            formatted += f"## {heading}\n\n"
            for p in points:
                formatted += f"- {p}\n"
            formatted += "\n"

    return formatted


# PDF GENERATION
def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AI Generated Structured Notes", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    for line in text.split("\n"):
        clean_line = line.replace("##", "").replace("-", "•")
        elements.append(Paragraph(clean_line, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload MP3, MP4, or OGG file",
    type=["mp3", "mp4", "ogg"]
)

# MAIN PROCESS
if uploaded_file:
    with st.spinner("Transcribing and generating notes... ⏳"):

        whisper_model = load_model()

        temp_file = "temp_audio"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.read())

        result = whisper_model.transcribe(temp_file)
        transcript = result["text"]

        structured_notes = structure_notes(transcript)

        os.remove(temp_file)

    # Transcription
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📄 Transcription")
    st.write(transcript)
    st.markdown('</div>', unsafe_allow_html=True)

    # Structured Notes
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📝 Structured Notes")
    st.markdown(structured_notes)
    st.markdown('</div>', unsafe_allow_html=True)

    # PDF Download
    pdf = generate_pdf(structured_notes)

    st.download_button(
        label="📥 Download Notes as PDF",
        data=pdf,
        file_name="AI_Structured_Notes.pdf",
        mime="application/pdf"
    )

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>Built with Whisper • Streamlit • ReportLab</div>",
    unsafe_allow_html=True
)
