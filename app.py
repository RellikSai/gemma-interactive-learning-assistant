import streamlit as st
from google import genai
from google.genai import types
import os
from pypdf import PdfReader
from dotenv import load_dotenv
import re

load_dotenv()
client = genai.Client(api_key=os.environ["GEMMA_API_KEY"])

def get_gemma_response(prompt, system_instruction=None):
    config = None
    if system_instruction:
        config = types.GenerateContentConfig(system_instruction=system_instruction)
    response = client.models.generate_content(model="gemma-4-31b-it", contents=prompt,  config=config)
    return response.text

st.set_page_config(
    page_title="Gemma-4 Powered: AI Tutor",
    layout="wide"
)

st.title("Gemma-4 Powered: Interactive Learning & Practice Assistant")

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Study-Material Learning",
    "📝 Quiz",
    "🎭 Customizable AI Tutor",
    "✨ Ask Doubts"
])


with tab1:
    st.header("Study-Material Learning: Summary and Road-Map")

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

                if st.button("Summarize & Generate RoadMap"):
                    with st.spinner("Analyzing PDF with Gemma..."):
                        analysis_prompt = f"""
                        Analyze the following document and:
                        1. Summarize the core thesis in 3 or 4 paragraph each with 6 or 7 clear sentences.
                        2. Based on this document, recommend: 3 prerequisite topics, 3 related concepts, 3 advanced topics, that the student should search next for deeper understanding and knowledge of the topic shared
                           and bullet point it as  first 3 topics as topics that should be known previously to understand the pdf shared and rest 3 related and and 3 advanced as u think it might fit it.
                        DOCUMENT TEXT:
                        {extracted_text}
                        """

                        result = get_gemma_response(analysis_prompt)
                        st.markdown("### 📌 Analysis Result")
                        st.markdown(result)

        except Exception as e:
            st.error(f"Failed to read PDF: {e}")


with tab2:

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    st.header("Practice & Test Your Understanding")
    st.subheader("Upload the Study-Material or Write the Topic Name")

    quiz_source = st.radio(
        "",
        ["Upload a PDF", "Write or Describe the Topic"],
        horizontal=True
    )

    quiz_content = ""

    if quiz_source == "Upload a PDF":

        uploaded_quiz_pdf = st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            key="quiz_pdf"
        )

        if uploaded_quiz_pdf:

            try:
                reader = PdfReader(uploaded_quiz_pdf)

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        quiz_content += page_text + "\n"

                if quiz_content.strip():
                    st.success("✅ PDF uploaded successfully.")
                else:
                    st.error("No readable text found in the PDF.")

            except Exception as e:
                st.error(f"Failed to read PDF: {e}")

    else:

        quiz_content = st.text_area(
            "Write or describe the topic",
            placeholder="Example: Artificial Intelligence, Thermodynamics, Indian Constitution, Data Structures...",
            height=120
        )


    st.divider()


    st.subheader("Select the Type of Questions You Want")

    question_style = st.radio(
        "",
        [
            "1-2 Word Answers",
            "2-3 Line Answers",
            "Long Descriptive Answers (4+ Lines)"
        ]
    )


    if st.button("Generate Quiz"):

        if not quiz_content.strip():

            st.warning("Please upload a PDF or enter a topic first.")

        else:

            if question_style == "1-2 Word Answers":

                answer_instruction = (
                    "Generate exactly 10 short-answer questions. "
                    "Each question should require a 1-2 word answer."
                )


            elif question_style == "2-3 Line Answers":

                answer_instruction = (
                    "Generate exactly 10 questions where answers should "
                    "require approximately 2-3 lines."
                )


            else:

                answer_instruction = (
                    "Generate exactly 10 deep descriptive questions where "
                    "answers should require at least 4 lines."
                )


            prompt = f"""

            Create a quiz based on the following material.

            Source Material:
            {quiz_content}


            Instructions:

            - {answer_instruction}
            - Number questions from 1 to 10.
            - Do not provide answers.
            - Questions should increase in difficulty.
            - Return only the questions.
            - Put each question on a separate line.

            """


            with st.spinner("Generating Quiz..."):

                quiz = get_gemma_response(prompt)

            questions = []

            for line in quiz.split("\n"):

                clean_line = line.strip()

                if clean_line:
                    questions.append(clean_line)


            st.session_state.quiz_questions = questions[:10]


    if st.session_state.quiz_questions:

        st.divider()

        st.markdown("## 📝 Answer the Quiz")


        user_answers = []


        for index, question in enumerate(st.session_state.quiz_questions):

            st.markdown(f"### {question}")


            answer = st.text_area(
                "Your Answer:",
                key=f"quiz_answer_{index}",
                height=100
            )


            user_answers.append(answer)

        st.divider()

        if st.button("Submit Quiz"):

            evaluation_data = ""

            for i, question in enumerate(st.session_state.quiz_questions):

                evaluation_data += f"""

                Question:
                {question}

                Student Answer:
                {user_answers[i]}

                """


            evaluation_prompt = f"""

            Evaluate this student's quiz.

            Rules:

            - There are 10 questions.
            - Give 1 mark for a completely correct answer.
            - Give 0 marks for wrong or unanswered questions.
            - Total score must be out of 10.
            - After scoring, provide the correct answer for every question.


            Student Responses:

            {evaluation_data}


            Format:

            SCORE:
            X/10


            CORRECT ANSWERS:

            1.
            2.
            3.
            4.
            5.
            6.
            7.
            8.
            9.
            10.

            """


            with st.spinner("AI is evaluating your answers..."):

                evaluation_result = get_gemma_response(
                    evaluation_prompt
                )

            st.divider()

            st.markdown("## 🎯 Quiz Result")

            score_match = re.search(r"SCORE:\s*(\d+\/10)", evaluation_result)

            if score_match:

                score = score_match.group(1)

                st.markdown(
                    f"""
                    <div style="
                        background-color:#FFC72C;
                        color:#1C1C1C;
                        padding:20px;
                        border-radius:12px;
                        font-size:32px;
                        font-weight:bold;
                        text-align:center;
                        box-shadow:0 0 20px rgba(255,199,44,0.9);
                        margin-bottom:20px;
                    ">
                        🏆 Your Score: {score} 🏆
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.warning("Score could not be extracted.")

            st.markdown("### ✅ Correct Answers & Evaluation")
            st.markdown(evaluation_result)


with tab3:
    st.header("Learn With Your Favorite AI Tutor")

    custom_persona_definition = st.text_area(
        "Name or Describe who do you want to Teach you:",
        placeholder="E.g. 'Act as Gojo Satoru' or 'Act as a Class Nerd who uses a lot of Analogies'....",
        height=100
    )

    user_request = st.text_area(
        "Which topic do you want to study today?",
        placeholder="E.g. Explain the cause and consequences of World War 2"
    )

    if st.button("Teach Me"):
        if not user_request.strip():
            st.warning("Please enter a request.")
        elif not custom_persona_definition.strip():
            st.warning("Please define the persona first.")
        else:
            with st.spinner("Generating content with Gemma..."):
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

                output = get_gemma_response(
                    content_prompt,
                    system_instruction=system_msg
                )

                st.divider()
                st.markdown(f"### ✨ Output based on Custom Role")
                st.write(output)


with tab4:
    st.header("AI Chatbox: Ready To Answer any Doubt you have")

    user_query = st.text_area(
        "What query or doubt do you have?",
        placeholder="Enter your query here...",
        height=100
    )

    if st.button("Answer my Query"):
        if not user_query.strip():
            st.warning("Please Enter your query to resolve it...")
        else:
            with st.spinner("Generating content with Gemma..."):
                system_msg = (
                    f"You are a Query solver just like a Customer Care. "
                    "Provide professional, detailed, high-quality answer to resolve the query. "
                    "Avoid fluff."
                )

                content_prompt = f"""
                User Request:
                {user_query}

                Generate the final output now.
                """

                output = get_gemma_response(
                    content_prompt,
                    system_instruction=system_msg
                )

                st.divider()
                st.markdown(f"### ✨ Here is Your Solution")
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
