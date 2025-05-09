# Dataset-Bit

A lightweight, production-ready FastAPI web application for high-quality Q&A dataset processing.  
Supports document upload, intelligent text chunking, Q&A generation, and export.  
Includes built-in SQLite database and file management. Ready to run out-of-the-box.

---

## Features

- 📄 **Document Upload**: Supports TXT, DOCX, PDF, and Markdown files.
- ✂️ **Intelligent Text Chunking**: Multiple chunking strategies (by paragraph, heading, table, or auto).
- 🤖 **Q&A Generation**: Generate question-answer pairs using LLMs (OpenAI API compatible).
- 📦 **Export**: Export datasets in various formats (JSON, CSV, Markdown).
- 🗂 **Built-in Database**: Ships with a pre-initialized SQLite database.
- 🗃 **File Management**: Uploaded files and exports are managed inside the container.
- 🌍 **Production Ready**: No code mounting or local dependencies required.

---

## Quick Start

### 1. Pull the image

```bash
docker pull yorko/dataset-bit:latest
```

### 2. Run the container

```bash
docker run -d -p 8000:8000 yorko/dataset-bit:latest
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Advanced Usage (with Docker Compose)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    image: yorko/dataset-bit:latest
    ports:
      - "8000:8000"
    environment:
      - APP_HOST=0.0.0.0
      - APP_PORT=8000
    restart: unless-stopped
```

Start with:

```bash
docker-compose up -d
```

---

## Notes

- The image includes a pre-initialized `dataset_bit.db` and all files in the `uploads` directory at build time.
- For persistent data, consider mounting volumes for `/app/uploads` and `/app/exports`.
- For development, see the `docker-compose.dev.yml` example in the repository.

---

## License

MIT 