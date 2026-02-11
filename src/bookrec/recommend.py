from __future__ import annotations

import numpy as np
import pandas as pd

from .index import load_chroma
from .settings import Paths


TONES = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]


def load_books(csv_path: str | None = None) -> pd.DataFrame:
    paths = Paths()
    p = paths.BOOKS_WITH_EMOTIONS if csv_path is None else csv_path
    books = pd.read_csv(p)

    books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
    books["large_thumbnail"] = np.where(
        books["large_thumbnail"].isna(),
        "cover-not-found.jpg",
        books["large_thumbnail"],
    )
    return books


def retrieve_semantic_recommendations(
    query: str,
    category: str = "All",
    tone: str = "All",
    initial_top_k: int = 50,
    final_top_k: int = 16,
    *,
    books_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    books = load_books() if books_df is None else books_df
    db = load_chroma()

    recs = db.similarity_search(query, k=initial_top_k)
    # Each line in tagged_description.txt begins with isbn13
    books_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)

    if category and category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category].head(final_top_k)
    else:
        book_recs = book_recs.head(final_top_k)

    if tone == "Happy":
        book_recs.sort_values(by="joy", ascending=False, inplace=True)
    elif tone == "Surprising":
        book_recs.sort_values(by="surprise", ascending=False, inplace=True)
    elif tone == "Angry":
        book_recs.sort_values(by="anger", ascending=False, inplace=True)
    elif tone == "Suspenseful":
        book_recs.sort_values(by="fear", ascending=False, inplace=True)
    elif tone == "Sad":
        book_recs.sort_values(by="sadness", ascending=False, inplace=True)

    return book_recs


def format_gallery_results(book_recs: pd.DataFrame):
    results = []
    for _, row in book_recs.iterrows():
        description = row.get("description", "")
        truncated = " ".join(str(description).split()[:30]) + "..."

        authors = str(row.get("authors", ""))
        authors_split = authors.split(";") if authors else []
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = authors

        caption = f"{row.get('title','')} by {authors_str}: {truncated}"
        results.append((row.get("large_thumbnail", "cover-not-found.jpg"), caption))
    return results
