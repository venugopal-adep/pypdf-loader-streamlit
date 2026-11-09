import io
import json
import os
import re
import tempfile
import pandas as pd
import pypdf
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Page Config
st.set_page_config(
    page_title="PyPDFLoader Studio 📄✨",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

/* Aurora Hero Banner */
.aurora-hero {
    background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 30%, #6366f1 65%, #a855f7 100%);
    border-radius: 18px;
    padding: 26px 32px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 14px 34px -8px rgba(59, 130, 246, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.25);
}

.aurora-title {
    font-size: 32px;
    font-weight: 800;
    margin: 0 0 6px 0;
    letter-spacing: -0.6px;
    display: flex;
    align-items: center;
    gap: 12px;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.aurora-sub {
    font-size: 15px;
    opacity: 0.96;
    max-width: 860px;
    line-height: 1.5;
    font-weight: 500;
}

.hero-pill-bar {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
}

.hero-pill {
    background: rgba(255, 255, 255, 0.22);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.35);
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* Metric Cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(59, 130, 246, 0.15);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}

.card-pages::before { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.card-chars::before { background: linear-gradient(90deg, #8b5cf6, #ec4899); }
.card-words::before { background: linear-gradient(90deg, #10b981, #22c55e); }
.card-size::before { background: linear-gradient(90deg, #f59e0b, #f97316); }
.card-ver::before { background: linear-gradient(90deg, #6366f1, #8b5cf6); }

.m-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    color: #64748b;
    margin-bottom: 4px;
}

.m-val {
    font-size: 24px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: #0f172a;
    line-height: 1.2;
}

.m-sub {
    font-size: 10.5px;
    color: #94a3b8;
    margin-top: 3px;
    font-weight: 500;
}

/* Metadata badges */
.meta-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
}

.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
}

.meta-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
}

.meta-key {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 3px;
}

.meta-val {
    font-weight: 600;
    color: #0f172a;
    font-family: 'JetBrains Mono', monospace;
    word-break: break-all;
}

/* Chunk Cards */
.chunk-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.chunk-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 12.5px;
    font-weight: 700;
    color: #4f46e5;
}
</style>
""", unsafe_allow_html=True)

# Banner
st.markdown("""
<div class="aurora-hero">
    <div class="aurora-title">PyPDFLoader Studio 📄✨</div>
    <div class="aurora-sub">
        Extract text, inspect document metadata, and explore advanced LangChain PyPDFLoader features like Layout Preservation, Page vs Single Mode, and RAG Text Chunking.
    </div>
    <div class="hero-pill-bar">
        <span class="hero-pill">⚡ PyPDFLoader</span>
        <span class="hero-pill">📐 Layout vs Plain Mode</span>
        <span class="hero-pill">📊 PDF Metadata Extraction</span>
        <span class="hero-pill">🔒 Password Decryption</span>
        <span class="hero-pill">🧩 LangChain RAG Chunking</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: PyPDFLoader Options Explorer
st.sidebar.markdown("### ⚙️ PyPDFLoader Configuration")
st.sidebar.caption("Explore all configurable features of LangChain's `PyPDFLoader`:")

extraction_mode = st.sidebar.radio(
    "1. Extraction Mode (`extraction_mode`)",
    options=["layout", "plain"],
    index=0,
    help="`layout` preserves spatial indentation, tabular columns, and margins. `plain` performs standard linear extraction."
)

doc_mode = st.sidebar.radio(
    "2. Loading Mode (`mode`)",
    options=["page", "single"],
    index=0,
    help="`page` returns one Document per PDF page (ideal for page navigation & citations). `single` merges all pages into one continuous Document."
)

delimiter = "\n\x0c"
if doc_mode == "single":
    delimiter = st.sidebar.text_input(
        "Page Delimiter (`pages_delimiter`)",
        value="\\n\\n--- PAGE BREAK ---\\n\\n",
        help="Custom separator string placed between pages when mode='single'"
    ).encode().decode("unicode_escape")

password_input = st.sidebar.text_input(
    "3. Password (`password`)",
    type="password",
    value="",
    help="Leave empty if PDF is not encrypted."
)
password = password_input.strip() if password_input.strip() else None

handle_rotations = st.sidebar.checkbox(
    "4. Handle Rotated Text (`orientations=(0,90,180,270)`)",
    value=True,
    help="Extracts text across all 4 standard orientations for rotated scans or slides."
)

st.sidebar.divider()
st.sidebar.markdown("### 🧩 RAG Chunking Explorer")
enable_chunking = st.sidebar.checkbox("Preview LangChain Text Chunking (`load_and_split`)", value=True)
chunk_size = st.sidebar.slider("Chunk Size (characters)", min_value=100, max_value=2000, value=500, step=50)
chunk_overlap = st.sidebar.slider("Chunk Overlap (characters)", min_value=0, max_value=400, value=50, step=10)

# File Uploader
uploaded_file = st.file_uploader(
    "Upload a PDF file to extract text & inspect metadata:",
    type=["pdf"],
    help="Upload any valid PDF document"
)

# Built-in sample PDF button
sample_pdf_path = "sample.pdf"
use_sample = False
if not uploaded_file and os.path.exists(sample_pdf_path):
    if st.button("📄 Or Load Built-in Sample PDF"):
        use_sample = True

pdf_bytes = None
filename = "document.pdf"

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    filename = uploaded_file.name
elif use_sample and os.path.exists(sample_pdf_path):
    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    filename = sample_pdf_path

if pdf_bytes is not None:
    # Save to temp file for PyPDFLoader
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    file_size_kb = len(pdf_bytes) / 1024.0
    size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.2f} MB"

    # Extract Reader Metadata using pypdf directly for deep inspection
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes), password=password)
        is_encrypted = reader.is_encrypted
        pdf_version = getattr(reader, "pdf_header", "Unknown")
        total_reader_pages = len(reader.pages)
        raw_meta = dict(reader.metadata) if reader.metadata else {}
    except Exception as e:
        is_encrypted = "Error reading"
        pdf_version = "Unknown"
        total_reader_pages = 0
        raw_meta = {}

    # Load with LangChain's PyPDFLoader
    extraction_kwargs = {}
    if handle_rotations:
        extraction_kwargs["orientations"] = (0, 90, 180, 270)

    try:
        loader = PyPDFLoader(
            file_path=tmp_path,
            password=password,
            mode=doc_mode,
            pages_delimiter=delimiter,
            extraction_mode=extraction_mode,
            extraction_kwargs=extraction_kwargs if extraction_kwargs else None,
        )
        docs = loader.load()
    except Exception as e:
        st.error(f"❌ PyPDFLoader failed to load PDF: {e}")
        docs = []
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    if docs:
        # Calculate overall statistics
        total_pages = total_reader_pages if total_reader_pages > 0 else len(docs)
        total_characters = sum(len(d.page_content) for d in docs)
        total_words = sum(len(d.page_content.split()) for d in docs)
        reading_time_min = max(1, round(total_words / 200))

        # Top Metrics Grid
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card card-pages">
                <div class="m-label">Total Pages</div>
                <div class="m-val">{total_pages:,}</div>
                <div class="m-sub">{len(docs)} Document objects</div>
            </div>
            <div class="metric-card card-chars">
                <div class="m-label">Characters</div>
                <div class="m-val">{total_characters:,}</div>
                <div class="m-sub">Extracted text length</div>
            </div>
            <div class="metric-card card-words">
                <div class="m-label">Words</div>
                <div class="m-val">{total_words:,}</div>
                <div class="m-sub">~{reading_time_min} min read</div>
            </div>
            <div class="metric-card card-size">
                <div class="m-label">File Size</div>
                <div class="m-val">{size_str}</div>
                <div class="m-sub">{filename}</div>
            </div>
            <div class="metric-card card-ver">
                <div class="m-label">PDF Version</div>
                <div class="m-val">{pdf_version}</div>
                <div class="m-sub">Encrypted: {is_encrypted}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Document Metadata Section
        st.markdown("### 📋 PDF Document Metadata")
        clean_title = raw_meta.get("/Title") or docs[0].metadata.get("title") or "Untitled Document"
        clean_author = raw_meta.get("/Author") or docs[0].metadata.get("author") or "Not Specified"
        clean_creator = raw_meta.get("/Creator") or docs[0].metadata.get("creator") or "Unknown"
        clean_producer = raw_meta.get("/Producer") or docs[0].metadata.get("producer") or "Unknown"
        clean_cdate = raw_meta.get("/CreationDate") or docs[0].metadata.get("creationdate") or "Unknown"
        clean_mdate = raw_meta.get("/ModDate") or docs[0].metadata.get("moddate") or "Unknown"

        st.markdown(f"""
        <div class="meta-box">
            <div class="meta-grid">
                <div class="meta-item">
                    <div class="meta-key">Title</div>
                    <div class="meta-val">{html.escape(str(clean_title))}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Author</div>
                    <div class="meta-val">{html.escape(str(clean_author))}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Creator Software</div>
                    <div class="meta-val">{html.escape(str(clean_creator))}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">PDF Producer</div>
                    <div class="meta-val">{html.escape(str(clean_producer))}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Creation Date</div>
                    <div class="meta-val">{html.escape(str(clean_cdate))}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-key">Modification Date</div>
                    <div class="meta-val">{html.escape(str(clean_mdate))}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tabs for Extracted Content Exploration
        tab_pages, tab_full, tab_rag, tab_meta = st.tabs([
            "📖 Page-by-Page View",
            "📜 Full Document Text",
            "🧩 LangChain RAG Chunking",
            "🛠️ Raw Metadata Inspector",
        ])

        # TAB 1: Page-by-Page View
        with tab_pages:
            if doc_mode == "page":
                col_sel, col_stats = st.columns([2, 3])
                with col_sel:
                    page_idx = st.number_input(
                        "Select Page Number:",
                        min_value=1,
                        max_value=len(docs),
                        value=1,
                        step=1,
                    ) - 1
                
                selected_doc = docs[page_idx]
                p_text = selected_doc.page_content
                p_chars = len(p_text)
                p_words = len(p_text.split())
                p_lines = len(p_text.splitlines())

                with col_stats:
                    st.markdown(f"**Page {page_idx + 1} of {len(docs)}** &bull; `{p_chars:,}` characters &bull; `{p_words:,}` words &bull; `{p_lines}` lines")

                st.text_area(
                    label=f"Text Content - Page {page_idx + 1}:",
                    value=p_text if p_text.strip() else "[No extractable text on this page - may be a scanned image or blank]",
                    height=450,
                )
            else:
                st.info("The PDF was loaded in `mode='single'` (all pages combined into 1 document). Go to the 'Full Document Text' tab to inspect.")

        # TAB 2: Full Document Text
        with tab_full:
            full_text = "\n\n".join(d.page_content for d in docs)
            
            # Keyword Search
            search_query = st.text_input("🔍 Search keyword in extracted text:", placeholder="Type a word or phrase...")
            if search_query.strip():
                matches = list(re.finditer(re.escape(search_query), full_text, re.IGNORECASE))
                st.success(f"Found **{len(matches)}** occurrence(s) of '{search_query}'.")

            st.text_area("Complete Extracted Text:", value=full_text, height=450)

            # Download Options
            d1, d2, d3 = st.columns(3)
            with d1:
                st.download_button(
                    label="💾 Download Text (.txt)",
                    data=full_text,
                    file_name=f"{filename.rsplit('.', 1)[0]}_extracted.txt",
                    mime="text/plain",
                )
            with d2:
                # Page-by-page JSON
                json_data = json.dumps([
                    {
                        "page": d.metadata.get("page", idx) + 1 if "page" in d.metadata else idx + 1,
                        "metadata": d.metadata,
                        "text": d.page_content,
                    }
                    for idx, d in enumerate(docs)
                ], indent=2)
                st.download_button(
                    label="💾 Download JSON (.json)",
                    data=json_data,
                    file_name=f"{filename.rsplit('.', 1)[0]}_pages.json",
                    mime="application/json",
                )
            with d3:
                # Markdown formatted
                md_text = f"# Extracted Document: {clean_title}\n\n"
                for idx, d in enumerate(docs):
                    p_num = d.metadata.get("page", idx) + 1 if "page" in d.metadata else idx + 1
                    md_text += f"## Page {p_num}\n\n{d.page_content}\n\n---\n\n"
                st.download_button(
                    label="💾 Download Markdown (.md)",
                    data=md_text,
                    file_name=f"{filename.rsplit('.', 1)[0]}.md",
                    mime="text/markdown",
                )

        # TAB 3: LangChain RAG Chunking
        with tab_rag:
            st.markdown("### 🧩 LangChain Text Chunking Demonstration")
            st.markdown("In Retrieval-Augmented Generation (RAG) pipelines, documents loaded with `PyPDFLoader` are split into chunks using text splitters (like `RecursiveCharacterTextSplitter`).")
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False,
            )
            chunks = splitter.split_documents(docs)
            st.info(f"Split **{len(docs)}** page document(s) into **{len(chunks)}** RAG chunks (Chunk size: {chunk_size}, Overlap: {chunk_overlap}).")

            if chunks:
                chunk_preview_limit = min(10, len(chunks))
                st.markdown(f"**Previewing first {chunk_preview_limit} chunks:**")
                for i in range(chunk_preview_limit):
                    chk = chunks[i]
                    p_orig = chk.metadata.get("page", 0) + 1 if "page" in chk.metadata else "N/A"
                    with st.container():
                        st.markdown(f"""
                        <div class="chunk-card">
                            <div class="chunk-header">
                                <span>Chunk #{i + 1}</span>
                                <span>Page {p_orig} &bull; {len(chk.page_content)} characters</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(chk.page_content, language="text")

        # TAB 4: Raw Metadata Inspector
        with tab_meta:
            st.markdown("### 🛠️ Raw Metadata Inspector")
            c_meta1, c_meta2 = st.columns(2)
            with c_meta1:
                st.markdown("**PDF Level Metadata (`pypdf.PdfReader.metadata`):**")
                st.json(raw_meta)
            with c_meta2:
                st.markdown("**LangChain Document Metadata (First Page):**")
                st.json(docs[0].metadata)

            # Metadata Table per Page
            if doc_mode == "page":
                st.markdown("**Page-by-Page Metadata Breakdown:**")
                table_rows = []
                for idx, d in enumerate(docs):
                    p_num = d.metadata.get("page", idx) + 1 if "page" in d.metadata else idx + 1
                    table_rows.append({
                        "Page #": p_num,
                        "Characters": len(d.page_content),
                        "Words": len(d.page_content.split()),
                        "Source File": d.metadata.get("source", filename),
                        "Page Label": d.metadata.get("page_label", str(p_num)),
                    })
                st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
else:
    st.info("👆 Please upload a PDF file using the file uploader above to extract text and explore metadata.")
