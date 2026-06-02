import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.chunker import create_chunks
from utils.vector_store import create_vector_store
from utils.summarizer import generate_summary


st.set_page_config(
    page_title="AI PDF Assistant",
    layout="wide"
)

st.title(
    "AI PDF Assistant"
)

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 3:

    st.error(
        "Maximum 3 PDFs allowed."
    )

    st.stop()

process_button = st.button(
    "Process Documents"
)

if process_button and uploaded_files:

    combined_text = ""

    with st.spinner("Processing Documents..."):

        for pdf in uploaded_files:

            text = extract_text_from_pdf(pdf)

            combined_text += text + "\n\n"

        chunks = create_chunks(
            combined_text
        )

        total_chunks = create_vector_store(
            chunks
        )

        summary = generate_summary(
            combined_text
        )

    st.success(
        "Knowledge Base Created Successfully"
    )

    # -------------------------
    # SUMMARY
    # -------------------------

    st.markdown("## Document Summary")

    st.info(summary)

    # -------------------------
    # STATS
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Documents",
            len(uploaded_files)
        )

    with col2:

        st.metric(
            "Words",
            len(
                combined_text.split()
            )
        )

    with col3:

        st.metric(
            "Characters",
            len(
                combined_text
            )
        )

    with col4:

        st.metric(
            "Chunks",
            total_chunks
        )

    # -------------------------
    # PREVIEW
    # -------------------------

    tab1, tab2 = st.tabs(
        [
            "Extracted Content",
            "Semantic Segments"
        ]
    )

    with tab1:

        st.text_area(
            "Document Content",
            combined_text[:5000],
            height=400
        )

    with tab2:

        for i, chunk in enumerate(chunks[:5]):

            st.markdown(
                f"### Segment {i+1}"
            )

            st.write(
                chunk[:500]
            )

            st.divider()