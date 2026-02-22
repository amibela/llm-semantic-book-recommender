from __future__ import annotations

import typer

from bookrec.index import build_chroma
from bookrec.settings import Paths
import runpy
runpy.run_path("app/gradio_app.py", run_name="__main__")

app = typer.Typer(add_completion=False)


@app.command()
def build_index(
    tagged_description: str | None = typer.Option(None, help="Path to tagged_description.txt"),
    persist_dir: str | None = typer.Option(None, help="Directory to persist Chroma DB"),
):
    """Build and persist the vector database (Chroma)."""
    paths = Paths()
    db = build_chroma(
        persist_dir=persist_dir or str(paths.CHROMA_DIR),
        tagged_description_path=tagged_description or str(paths.TAGGED_DESCRIPTION),
    )
    typer.echo(f"Chroma DB built at: {db._persist_directory}")


@app.command()
def run_app():
    """Run the Gradio dashboard."""
    from app.gradio_app import main
    main()


if __name__ == "__main__":
    app()
