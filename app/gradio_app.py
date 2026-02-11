from __future__ import annotations

import gradio as gr

from bookrec.recommend import retrieve_semantic_recommendations, format_gallery_results, load_books, TONES


def recommend_books(query: str, category: str, tone: str):
    books = load_books()
    recs = retrieve_semantic_recommendations(query, category, tone, books_df=books)
    return format_gallery_results(recs)


def main():
    books = load_books()
    categories = ["All"] + sorted(books["simple_categories"].dropna().unique().tolist())
    tones = TONES

    with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
        gr.Markdown("# Semantic book recommender")

        with gr.Row():
            user_query = gr.Textbox(
                label="Please enter a description of a book:",
                placeholder="e.g., A story about forgiveness",
            )
            category_dropdown = gr.Dropdown(choices=categories, label="Select a category:", value="All")
            tone_dropdown = gr.Dropdown(choices=tones, label="Select an emotional tone:", value="All")
            submit_button = gr.Button("Find recommendations")

        gr.Markdown("## Recommendations")
        output = gr.Gallery(label="Recommended books", columns=8, rows=2)

        submit_button.click(
            fn=recommend_books,
            inputs=[user_query, category_dropdown, tone_dropdown],
            outputs=output,
        )

    dashboard.launch()


if __name__ == "__main__":
    main()
