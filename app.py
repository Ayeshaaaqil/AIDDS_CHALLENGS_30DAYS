import streamlit as st
import io
from modules import extractor, summarizer, quiz_mcq, quiz_mixed
import json # For displaying JSON outputs nicely

# --- Page Configuration ---
st.set_page_config(
    page_title="Study Notes Summarizer & Quiz Generator",
    page_icon="📚",
    layout="wide"
)
st.title("📚 Study Notes Summarizer & Quiz Generator")
st.markdown("Upload a PDF to get structured study notes and generate quizzes!")

# --- Session State Initialization ---
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = "uploaded_document"
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'mcq_quiz' not in st.session_state:
    st.session_state.mcq_quiz = None
if 'mixed_quiz' not in st.session_state:
    st.session_state.mixed_quiz = None

# --- PDF Upload Section ---
st.header("1. Upload Your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.session_state.pdf_name = uploaded_file.name
    st.write(f"File uploaded: {st.session_state.pdf_name}")

    # Read PDF as bytes
    pdf_bytes = uploaded_file.getvalue()

    # Extract text (only if not already extracted or a new file is uploaded)
    if st.session_state.extracted_text is None or st.session_state.pdf_name != uploaded_file.name:
        with st.spinner("Extracting text from PDF..."):
            st.session_state.extracted_text = extractor.extract_text_from_pdf(pdf_bytes)
        st.success("Text extraction complete!")
        # Clear previous results if a new PDF is uploaded
        st.session_state.summary = None
        st.session_state.mcq_quiz = None
        st.session_state.mixed_quiz = None

    st.subheader("Extracted Text (first 5000 characters):")
    st.text(st.session_state.extracted_text[:5000] + "..." if st.session_state.extracted_text else "No text extracted.")

# --- Action Buttons (Summarize & Quiz) ---
if st.session_state.extracted_text:
    st.header("2. Generate Study Materials")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Summarization")
        if st.button("Generate Summary", key="generate_summary_btn"):
            with st.spinner("Generating summary... This may take a moment."):
                summarizer_instance = summarizer.Summarizer()
                file_info = summarizer.FileInfo(
                    file_name=st.session_state.pdf_name,
                    file_type=summarizer.DataType.PDF,
                    content=st.session_state.extracted_text
                )
                st.session_state.summary = summarizer_instance.generate_summary(file_info)
            st.success("Summary generated!")

    with col2:
        st.subheader("Quiz Generation")
        quiz_type = st.radio("Select Quiz Type:", ("MCQ Only", "Mixed Format"), key="quiz_type_radio")
        num_questions = st.slider("Number of MCQs (or total for mixed):", min_value=1, max_value=10, value=5)

        if quiz_type == "MCQ Only":
            if st.button("Generate MCQ Quiz", key="generate_mcq_btn"):
                with st.spinner(f"Generating {num_questions} MCQs..."):
                    mcq_generator = quiz_mcq.QuizGeneratorMCQ()
                    st.session_state.mcq_quiz = mcq_generator.generate_mcq_quiz(
                        document_content=st.session_state.extracted_text,
                        num_questions=num_questions
                    )
                st.success("MCQ Quiz generated!")
        else: # Mixed Format
            if st.button("Generate Mixed Quiz", key="generate_mixed_btn"):
                with st.spinner("Generating Mixed Quiz (MCQ, True/False, Short Answer)..."):
                    mixed_generator = quiz_mixed.QuizGeneratorMixed()
                    # Distribute num_questions to different types, e.g., 50% MCQ, 30% TF, 20% SA
                    num_mcq_mixed = int(num_questions * 0.5)
                    num_tf_mixed = int(num_questions * 0.3)
                    num_sa_mixed = num_questions - num_mcq_mixed - num_tf_mixed
                    
                    st.session_state.mixed_quiz = mixed_generator.generate_mixed_quiz(
                        document_content=st.session_state.extracted_text,
                        num_mcq=num_mcq_mixed,
                        num_tf=num_tf_mixed,
                        num_sa=num_sa_mixed
                    )
                st.success("Mixed Quiz generated!")

# --- Display Results ---
st.header("3. Your Results")

if st.session_state.summary:
    st.subheader("📄 Generated Summary")
    summary = st.session_state.summary
    st.markdown(f"### {summary.get('title', 'No Title')}")
    st.write(summary.get('main_summary', 'No main summary available.'))

    if summary.get('study_notes'):
        st.markdown("#### Point-wise Study Notes:")
        for note in summary['study_notes']:
            st.markdown(f"- {note}")
    
    if summary.get('important_concepts'):
        st.markdown("#### Important Concepts:")
        for concept, definition in summary['important_concepts'].items():
            st.markdown(f"**{concept}**: {definition}")

    if summary.get('key_ideas'):
        st.markdown("#### Key Ideas:")
        for idea in summary['key_ideas']:
            st.markdown(f"- {idea}")
    
    st.download_button(
        label="Download Summary as JSON",
        data=json.dumps(summary, indent=2),
        file_name=f"{st.session_state.pdf_name}_summary.json",
        mime="application/json"
    )

if st.session_state.mcq_quiz:
    st.subheader("❓ MCQ Quiz")
    for i, q in enumerate(st.session_state.mcq_quiz):
        st.markdown(f"**Q{i+1}:** {q['question']}")
        options = q['options']
        for opt_key, opt_value in options.items():
            st.write(f"**{opt_key}.** {opt_value}")
        st.write(f"**Correct Answer:** {q['correct_answer']}")
        st.markdown("---")
    
    st.download_button(
        label="Download MCQ Quiz as JSON",
        data=json.dumps(st.session_state.mcq_quiz, indent=2),
        file_name=f"{st.session_state.pdf_name}_mcq_quiz.json",
        mime="application/json"
    )

if st.session_state.mixed_quiz:
    st.subheader("⁉️ Mixed Format Quiz")
    mixed_quiz = st.session_state.mixed_quiz

    if mixed_quiz.get("mcqs"):
        st.markdown("#### Multiple Choice Questions:")
        for i, q in enumerate(mixed_quiz["mcqs"]):
            st.markdown(f"**Q{i+1}:** {q['question']}")
            options = q['options']
            for opt_key, opt_value in options.items():
                st.write(f"**{opt_key}.** {opt_value}")
            st.write(f"**Correct Answer:** {q['correct_answer']}")
            st.markdown("---")

    if mixed_quiz.get("true_false"):
        st.markdown("#### True/False Questions:")
        for i, q in enumerate(mixed_quiz["true_false"]):
            st.markdown(f"**Q{i+1}:** {q['question']}")
            st.write(f"**Answer:** {q['answer']}")
            st.markdown("---")
    
    if mixed_quiz.get("short_answers"):
        st.markdown("#### Short Answer Questions:")
        for i, q in enumerate(mixed_quiz["short_answers"]):
            st.markdown(f"**Q{i+1}:** {q['question']}")
            st.write(f"**Required Keywords:** {', '.join(q['required_keywords'])}")
            st.markdown("---")
    
    st.download_button(
        label="Download Mixed Quiz as JSON",
        data=json.dumps(mixed_quiz, indent=2),
        file_name=f"{st.session_state.pdf_name}_mixed_quiz.json",
        mime="application/json"
    )
