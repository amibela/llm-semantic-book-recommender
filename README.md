# Semantic Book Recommender (projectized)

This repo is a cleaned-up project structure based on the freeCodeCamp Project.
The original tutorial files are kept under `notebooks/` and `README_upstream.md`.

## What it does
- Builds a vector database for semantic search over book descriptions
- Adds category (fiction/non-fiction etc.) + emotion/tone signals.
- Serves recommendations via a Gradio UI

## Setup

### 1) Create a virtualenv + install deps
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Add your API key
Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

### 3) Put the processed artifacts in place
The Gradio app expects these files (created by the tutorial notebooks) to exist:

- `data/processed/books_with_emotions.csv`
- `data/processed/tagged_description.txt`

When already generated  in the tutorial folder, just move them into `data/processed/`.

### 4) Build the vector DB (persisted)
```bash
python -m src.cli build-index

``` 

``` Powershell
python src/cli.py build-index
```
### 5) Run the UI
```bash
python -m src.cli run-app
```
``` Powershell
python src/cli.py run-app
```
## Notes on versioning
Do **not** commit `data/`, `indexes/`, or `models/` (already in `.gitignore`).
If you want a reproducible repo, upload a small sample dataset or add download scripts.
