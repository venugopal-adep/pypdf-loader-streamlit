# PyPDFLoader Studio 📄✨

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=venugopal-adep/pypdf-loader-streamlit&branch=main&main_module=app.py)

An interactive PDF text extraction, metadata inspection, and RAG chunking explorer built with **Streamlit** and **LangChain's PyPDFLoader**.

## 🚀 One-Click Deploy to Streamlit Community Cloud

Click the button above or use this link:
👉 **[Deploy to Streamlit Cloud](https://share.streamlit.io/deploy?repository=venugopal-adep/pypdf-loader-streamlit&branch=main&main_module=app.py)**

---

## 🌟 Key Features

1. **📄 Drag-and-Drop PDF Upload**:
   - Easily upload any PDF document or test immediately using the built-in sample document.

2. **⚙️ PyPDFLoader Features as Configurable Options**:
   - **`extraction_mode`**: Toggle between `layout` (preserves spatial margins, indentation, and tables) and `plain` (linear text extraction).
   - **`mode`**: Choose between `page` (one LangChain `Document` per PDF page) and `single` (all pages combined into one document).
   - **`pages_delimiter`**: Customize the separator string used between pages when in `single` mode.
   - **`password`**: Decrypt password-protected or encrypted PDFs.
   - **`orientations`**: Detect and extract rotated text across 0°, 90°, 180°, and 270°.

3. **📋 Comprehensive Metadata Inspector**:
   - **Document Level**: Title, Author, Subject, Creator, Producer, Creation Date, Modification Date, PDF Version, Encryption status.
   - **Page Level**: Page number, character count, word count, line count, and source file metadata.

4. **🔍 Interactive Content Exploration**:
   - **Page-by-Page Viewer**: Jump to any page with real-time statistics.
   - **Full Document Search**: Instant keyword search showing match count across all extracted text.
   - **RAG Chunking Preview**: Test LangChain's `RecursiveCharacterTextSplitter` / `load_and_split` with adjustable chunk size and overlap sliders.

5. **💾 Multi-Format Export**:
   - Download extracted text as `.txt`.
   - Download page-by-page metadata & text as `.json`.
   - Download formatted Markdown document as `.md`.

---

## 💻 Local Execution

```bash
git clone https://github.com/venugopal-adep/pypdf-loader-streamlit.git
cd pypdf-loader-streamlit
pip install -r requirements.txt
streamlit run app.py
```

