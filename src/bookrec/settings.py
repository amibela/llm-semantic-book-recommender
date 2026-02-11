from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    # project root is two levels above this file: src/bookrec/settings.py
    ROOT: Path = Path(__file__).resolve().parents[2]

    DATA_RAW: Path = ROOT / "data" / "raw"
    DATA_PROCESSED: Path = ROOT / "data" / "processed"

    # expected artifacts created by the notebooks / pipeline scripts
    BOOKS_CLEANED: Path = DATA_PROCESSED / "books_cleaned.csv"
    BOOKS_WITH_CATEGORIES: Path = DATA_PROCESSED / "books_with_categories.csv"
    BOOKS_WITH_EMOTIONS: Path = DATA_PROCESSED / "books_with_emotions.csv"
    TAGGED_DESCRIPTION: Path = DATA_PROCESSED / "tagged_description.txt"

    # persisted vector DB
    CHROMA_DIR: Path = ROOT / "indexes" / "chroma"
