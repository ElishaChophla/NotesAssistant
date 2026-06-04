import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.chunker import create_chunks
from utils.vector_store import create_vector_store
from utils.summarizer import generate_summary

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Document Intelligence Platform",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: linear-gradient(
        135deg,
        #0F172A 0%,
        #111827 50%,
        #1E1B4B 100%
    );
}

/* HERO */

.hero{
    text-align:center;
    padding:40px 0px;
}

.hero-title{
    font-size:4rem;
    font-weight:800;
    color:white;
    margin-bottom:10px;
}

.hero-subtitle{
    color:#CBD5E1;
    font-size:1.2rem;
    max-width:900px;
    margin:auto;
    line-height:1.8;
}

/* SECTION TITLES */

.section-title{
    color:white;
    font-size:1.8rem;
    font-weight:700;
    margin-top:20px;
    margin-bottom:15px;
}

/* GLASS CARDS */

.glass-card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(14px);
    border:1px solid rgba(255,255,255,0.15);
    border-radius:20px;
    padding:20px;
    color:white;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);
    border:2px dashed #8B5CF6;
    border-radius:20px;
    padding:20px;
}

/* BUTTON */

.stButton > button{
    width:100%;
    height:60px;
    border:none;
    border-radius:15px;

    background:linear-gradient(
        135deg,
        #7C3AED,
        #2563EB
    );

    color:white;
    font-size:18px;
    font-weight:700;
}

/* METRICS */

[data-testid="metric-container"]{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.15);
    border-radius:18px;
    padding:18px;
}

[data-testid="metric-container"] *{
    color:white !important;
}

/* TABS */

.stTabs [data-baseweb="tab"]{
    color:white;
    font-weight:600;
}

/* EXPANDERS */

.streamlit-expanderHeader{
    color:white;
}

/* TEXT */

h1,h2,h3,h4,p,label,span{
    color:white !important;
}

/* TEXT AREA */

textarea{
    background:#0F172A !important;
    color:white !important;
}

/* SUCCESS MESSAGE */

[data-testid="stAlert"]{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO
# ==================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
Document Intelligence Platform
</div>

<div class="hero-subtitle">
Transform PDF documents into searchable knowledge.
Generate summaries, build semantic embeddings,
and prepare your content for intelligent AI-powered conversations.
</div>

</div>
""", unsafe_allow_html=True)

# ==================================================
# FEATURES
# ==================================================

st.markdown(
    '<div class="section-title">Platform Features</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="glass-card">
    <h4>Document Analysis</h4>
    Extract and organize information from uploaded PDFs.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card">
    <h4>Semantic Retrieval</h4>
    Generate vector embeddings for intelligent search.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card">
    <h4>Knowledge Base</h4>
    Store document intelligence using FAISS.
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="glass-card">
    <h4>AI Ready</h4>
    Prepare documents for future chatbot interaction.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# UPLOAD SECTION
# ==================================================

st.markdown(
    '<div class="section-title">Upload Documents</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload up to 3 PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 3:

    st.error(
        "Maximum 3 PDF files are allowed."
    )

    st.stop()

# ==================================================
# FILE LIST
# ==================================================

if uploaded_files:

    st.markdown(
        '<div class="section-title">Document Library</div>',
        unsafe_allow_html=True
    )

    for file in uploaded_files:

        st.markdown(
            f"""
            <div class="glass-card">
            📄 {file.name}
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# PROCESS BUTTON
# ==================================================

process_button = st.button(
    "Build Knowledge Base"
)

# ==================================================
# PROCESSING
# ==================================================

if process_button and uploaded_files:

    combined_text = ""

    with st.spinner(
        "Processing Documents..."
    ):

        for pdf in uploaded_files:

            text = extract_text_from_pdf(
                pdf
            )

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
        "Knowledge Base Ready • Documents Successfully Processed"
    )

    # ==================================================
    # SUMMARY
    # ==================================================

    st.markdown(
        '<div class="section-title">Document Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="glass-card">
        {summary}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # METRICS
    # ==================================================

    st.markdown(
        '<div class="section-title">Knowledge Base Metrics</div>',
        unsafe_allow_html=True
    )

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
            "Segments",
            total_chunks
        )

    # ==================================================
    # TABS
    # ==================================================

    tab1, tab2 = st.tabs(
        [
            "Document Content",
            "Knowledge Segments"
        ]
    )

    with tab1:

        st.text_area(
            "Extracted Document Content",
            combined_text[:5000],
            height=450
        )

    with tab2:

        for i, chunk in enumerate(
            chunks[:5]
        ):

            with st.expander(
                f"Semantic Segment {i+1}"
            ):

                st.write(
                    chunk
                )

# ==================================================
# FOOTER
# ==================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "Built with Streamlit • FAISS • Sentence Transformers • Generative AI"
)