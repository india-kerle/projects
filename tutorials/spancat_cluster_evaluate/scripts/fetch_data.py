"""
Fetch articles from the Guardian API related from the environment section.

python -m scripts.fetch_data
"""
import os
import random
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import spacy
import srsly
import typer
from dotenv import load_dotenv
from spacy.language import Language
from typing_extensions import Annotated

load_dotenv()

api_key = os.getenv("GUARDIAN_API_KEY")
if not api_key:
    print("No GUARDIAN_API_KEY. Please set it in .env")

BASE_URL = "https://content.guardianapis.com/search"

PARAMETERS = {
    "api-key": api_key,
    "section": "environment",
    "show-fields": "all",
    "page-size": 200,
    "order-by": "newest",
}

OUTPUT_PATH = Path.cwd() / "assets/raw/"

nlp = spacy.load("en_core_web_sm")


def _get_relevant_data(article: Dict[str, Any], nlp: Language = nlp) -> Dict[str, str]:
    """Get relevant data from the Guardian article. Also chunk
        the outputs if it is more than 10 sentences.

    Args:
        article (Dict[str, Any]): Dictionary with the article data.

    Returns:
        Dict[str, str]: Dictionary with the relevant data.
    """
    clean_dict = {}
    article_chunks = []

    id_ = article["id"]
    article_text = article["fields"]["bodyText"]
    doc = nlp(article_text)

    sentences = list(doc.sents)
    for i in range(0, len(sentences), 10):
        chunk = sentences[i : i + 10]
        chunk_text = " ".join([sent.text for sent in chunk])
        id_chunk = f"{id_}_{i//10}"
        clean_dict = {
            "text": chunk_text,
            "meta": {"id": id_chunk, "publication_date": article["webPublicationDate"]},
        }
        article_chunks.append(clean_dict)

    return article_chunks


def fetch_data(
    output_path: Annotated[Optional[Path], typer.Argument()] = OUTPUT_PATH
) -> Dict[str, str]:
    """Fetch data from the Guardian API.

    Args:
        output_path: (str): Path to save the data.

    Returns:
        Dict[str, Any]: Response from the Guardian API.
    """

    clean_articles = []
    current_page = 1
    total_pages = 3  # get the first 3 pages (600 articles)

    while current_page <= total_pages:
        PARAMETERS["page"] = current_page
        response = requests.get(BASE_URL, params=PARAMETERS)
        if response.ok:
            data = response.json()["response"]
            articles = data["results"]
            for article in articles:
                clean_data = _get_relevant_data(article)
                clean_articles.extend(clean_data)
            print(f"completed page {current_page}...")
            current_page += 1
        else:
            print(f"The response code is: {response.status_code}")
            break

    random.seed(45)
    articles_shuffled = random.sample(clean_articles, len(clean_articles))

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f"saving to... {output_path}")

    # save a little sample of the data
    sample_output_path = output_path / "guardian_data_sample.jsonl"
    srsly.write_jsonl(sample_output_path, articles_shuffled[:200])

    # save main data
    full_output_path = output_path / "guardian_data.jsonl"
    srsly.write_jsonl(full_output_path, articles_shuffled[200:])


if __name__ == "__main__":
    typer.run(fetch_data)
