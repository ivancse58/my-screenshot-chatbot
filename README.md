# 🖼️ Screenshot Chatbot

A privacy-focused, local chatbot that monitors a folder for new screenshots/images, extracts text using OCR, stores them in a vector database with embeddings, and answers natural language questions using a local LLM based on the image content.

---

## 🚀 Features

- 📂 **Live Folder Watching**: Automatically detects and processes new image files (`.png`, `.jpg`, `.jpeg`, `.heic`)
- 🧠 **OCR Text Extraction**: Uses Tesseract OCR to extract text from screenshots
- 🔍 **Semantic Search**: Uses SentenceTransformers and FAISS for similarity-based text retrieval
- 💬 **LLM-Powered Answers**: Combines search results with a local language model for intelligent responses
- 🔐 **Offline & Private**: No cloud dependencies; all data is stored and processed locally

---

## 🧱 Project Structure

- Please find the project structure in docs/file_structure.txt file.
---

## 🛠️ Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/screenshot-chatbot.git
cd screenshot-chatbot
2. Set Up Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Install Dependencies
Tesseract OCR
macOS (with Homebrew):
brew install tesseract
brew install tesseract-lang
```

⚙️ Usage
1. Start Watcher
```bash
    python watcher.py
```
- Monitors data/watch/ for new images
    
- Automatically extracts text, generates embeddings, updates the index

2. Add Screenshots 
   Place .png, .jpg, .jpeg, or .heic files into data/watch/.

3. Ask Questions
   ```bash
   python query_console.py
   ```
   Interact with the embedded knowledge base

   Natural language interface to search screenshot content

📌 Example

```bash
    $ python query_console.py
    
    Ask me: What error message did I see yesterday?
    Answer: The system reported "Connection timed out."
```
⚠️ Limitations & Future Work

- 🔤 Language Support

- ❌ Current OCR is optimized for English; multi-language OCR support is limited and may require manual Tesseract language packs.

- 🧪 LLMs may not respond accurately in languages other than English depending on the model.

- 📷 Image Processing

- 🚧 HEIC conversion may crop or distort high-res images; improved conversion pipeline is planned.

- 🎯 OCR results vary with font clarity, image quality, and orientation.

- 🤖 Chatbot Capabilities

  - 🧠 No memory or history-aware chat; each query is independent.

  - 🛠 Context truncation may happen if image content is long.

  - 🔄 Modular Extensibility

- ☑️ Watcher and Query systems are modular and can be extended to:

  - Watch multiple folders

- Send system notifications on process completion

- Add real-time web or desktop chat interface

- Use faster or multilingual models (e.g., Mistral, LLaMA 3)

🧑‍💻 Author
- Built by ChatGPT and customized by Riazul Karim Ivan.

📄 License
- MIT License — use freely, improve boldly.