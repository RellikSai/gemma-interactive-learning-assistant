import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_gemini_response(prompt, system_instruction=None):
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )
    response = model.generate_content(prompt)
    return response.text


st.set_page_config(
    page_title="Gemini PDF Reasoning Tool",
    layout="wide"
)

st.title("🧠 Gemini PDF Reasoning & Personalization Hub")

tab1, tab2 = st.tabs([
    "📄 PDF Learning Summary",
    "🎭 Persona Content Generator"
])

# -----------------------------
# Tab 1: PDF Learning Summary
# -----------------------------
with tab1:
    st.header("1. PDF Learning Summary")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    if uploaded_file:
        try:
            reader = PdfReader(uploaded_file)
            extracted_text = ""

            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"

            if not extracted_text.strip():
                st.error("❌ No readable text found in this PDF.")
            else:
                st.success("✅ PDF text extracted successfully")

                if st.button("Analyze & Generate Challenges"):
                    with st.spinner("Analyzing PDF with Gemini..."):
                        analysis_prompt = f"""
                        Analyze the following document and:
                        1. Summarize the core thesis in 2 paragraph each with 4 or 5 clear sentences.
                        2. Generate 5 complex, deep-reasoning questions based on the document.

                        DOCUMENT TEXT:
                        {extracted_text}
                        """

                        result = get_gemini_response(analysis_prompt)
                        st.markdown("### 📌 Analysis Result")
                        st.markdown(result)

        except Exception as e:
            st.error(f"Failed to read PDF: {e}")

# -----------------------------
# Tab 2: Persona-Driven Generator
# -----------------------------
with tab2:
    st.header("2. Persona-Driven Generator")

    custom_persona_definition = st.text_area(
        "Define the AI's Persona/Role:",
        placeholder="E.g. 'Act as a Mechanical Engineer' or 'Act as a Researcher'....",
        height=100
    )

    user_request = st.text_area(
        "What do you need created?",
        placeholder="E.g. Summarize this research paper for executives...."
    )

    if st.button("Generate Content"):
        if not user_request.strip():
            st.warning("Please enter a request.")
        elif not custom_persona_definition.strip():
            st.warning("Please define the persona first.")
        else:
            with st.spinner("Generating content with Gemini..."):
                system_msg = (
                    f"You are a {custom_persona_definition}. "
                    "Provide professional, detailed, high-quality output. "
                    "Avoid fluff."
                )

                content_prompt = f"""
                User Request:
                {user_request}

                Generate the final output now.
                """

                output = get_gemini_response(
                    content_prompt,
                    system_instruction=system_msg
                )

                st.divider()
                st.markdown(f"### ✨ Output based on Custom Role")
                st.write(output)


def set_mixed_color_background_green_pro():
    PRIMARY_DARK = "#1C1C1C"
    ACCENT_SHINY_GREEN = "#39FF14"
    ACCENT_GOLD = "#FFC72C"
    LIGHT_TEXT = "#E0E0E0"

    depth_gradient = (
        "linear-gradient(150deg, "
        "rgba(28,28,28,1) 0%, "
        "rgba(20,20,20,1) 100%)"
    )

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {PRIMARY_DARK};
            background-image: {depth_gradient}; 
            background-size: cover;
            background-attachment: fixed;
            color: {LIGHT_TEXT}; 
        }}

        .stFileUploaderDropzone {{
            border: 2px dashed {ACCENT_SHINY_GREEN}; /* This creates the green outline */
            border-radius: 6px;
            box-shadow: 0 0 8px rgba(57, 255, 20, 0.3);
            background-color: rgba(57, 255, 20, 0.05);
            padding: 20px;
        }}

        .st-emotion-cache-1jmh399 {{ 
            background-color: rgba(35, 35, 35, 0.9); 
            border: 1px solid {ACCENT_SHINY_GREEN}; 
            border-radius: 6px;
            padding: 25px;
            box-shadow: 0 0 12px rgba(57, 255, 20, 0.4); 
        }}

        h1, h2, h3 {{
            color: {ACCENT_SHINY_GREEN}; 
            text-shadow: 
                0 0 4px {ACCENT_SHINY_GREEN}, 
                0 0 8px {ACCENT_SHINY_GREEN}; 
            border-bottom: 2px solid rgba(255, 199, 44, 0.3); 
            padding-bottom: 5px;
            margin-bottom: 10px;
        }}

        .stButton>button, .stSelectbox {{
            border-color: {ACCENT_GOLD}; 
            background-color: {PRIMARY_DARK};
            color: {ACCENT_GOLD}; 
            box-shadow: 0 0 5px rgba(255, 199, 44, 0.4);
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: rgba(57, 255, 20, 0.1); 
            color: #FFFFFF;
        }}

        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            background-color: rgba(255, 255, 255, 0.05); 
            border: 1px solid {ACCENT_SHINY_GREEN};
            color: {LIGHT_TEXT};
        }}

        .stFileUploader {{
            border: none;
            box-shadow: none;
            padding: 0;
        }}

        .stFileUploaderDropzone {{
            border: 2px dashed {ACCENT_SHINY_GREEN}; 
            border-radius: 6px;
            box-shadow: 0 0 8px rgba(57, 255, 20, 0.3);
            background-color: rgba(57, 255, 20, 0.05);
            padding: 20px;
        }}

        .stFileUploader button {{
            border-color: {ACCENT_GOLD};
            color: {ACCENT_GOLD};
            background-color: {PRIMARY_DARK};
            box-shadow: 0 0 5px rgba(255, 199, 44, 0.4);
        }}
        .stFileUploader button:hover {{
            background-color: rgba(255, 199, 44, 0.1); 
            color: #FFFFFF;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )
set_mixed_color_background_green_pro()