from __future__ import annotations

from typing import Iterable

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from .settings import Paths


def build_documents(tagged_description_path: str | None = None):
    paths = Paths()
    src_path = paths.TAGGED_DESCRIPTION if tagged_description_path is None else tagged_description_path

    raw_documents = TextLoader(str(src_path)).load()
    # One record per line; do not chunk across lines
    splitter = CharacterTextSplitter(separator="\n", chunk_size=0, chunk_overlap=0)
    return splitter.split_documents(raw_documents)


def build_chroma(persist_dir: str | None = None, tagged_description_path: str | None = None) -> Chroma:
    paths = Paths()
    persist = paths.CHROMA_DIR if persist_dir is None else persist_dir
    persist = str(persist)

    docs = build_documents(tagged_description_path=tagged_description_path)
    db = Chroma.from_documents(
        docs,
        OpenAIEmbeddings(),
        persist_directory=persist,
    )
    return db


def load_chroma(persist_dir: str | None = None) -> Chroma:
    paths = Paths()
    persist = str(paths.CHROMA_DIR if persist_dir is None else persist_dir)
    return Chroma(
        persist_directory=persist,
        embedding_function=OpenAIEmbeddings(),
    )
