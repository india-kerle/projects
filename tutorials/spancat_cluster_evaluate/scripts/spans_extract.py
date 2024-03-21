"""
This script extract spans from the dataset and save them in a file.

python -m scripts.extract_spans 
"""
from pathlib import Path
from typing import Dict, List, Union

import spacy
import srsly
import typer
from spacy.tokens import Doc
from tqdm import tqdm
from wasabi import msg

ASSETS_PATH = Path.cwd() / "assets"

ARTICLES_PATH = ASSETS_PATH / "raw/guardian_data.jsonl"
MODEL_PATH = Path.cwd() / "training/model-best"


def _get_span_information(doc: Doc) -> Union[List[Dict[str, str]], None]:
    """Get span information for a given Doc object.

    Args:
        doc (Doc): A Doc object.

    Returns:
        Union[List[Dict[str, str]], None]: A list of dictionaries containing span information.
    """

    spans = doc.spans["sc"]
    span_information = []

    if len(spans) > 0:
        span_scores = spans.attrs["scores"]
        for span, span_score in zip(spans, span_scores):
            spans_dict = {
                "span": span.text,
                "label": span.label_,
                "score": float(round(span_score, 2)),
            }
            span_information.append(spans_dict)
        return span_information
    else:
        return None


def get_spans(
    model_path: Path = MODEL_PATH, articles_path: Path = ARTICLES_PATH
) -> None:
    """Extract spans from the dataset and save them in a file.

    Args:
        model_path (Path): Path to the spaCy model.
        articles_path (Path): Path to the articles file.
    """

    nlp = spacy.load(model_path)

    predicted_spans = []
    for example in tqdm(srsly.read_jsonl(articles_path)):
        doc = nlp(example["text"])
        span_info = _get_span_information(doc)
        predicted_spans_dict = {"id": example["meta"]["id"], "sc_info": span_info}
        predicted_spans.append(predicted_spans_dict)

    msg.good(f"Extracted spans from the {len(predicted_spans)} guardian articles.")
    srsly.write_jsonl(ASSETS_PATH / "labelled/predicted_spans.jsonl", predicted_spans)


if __name__ == "__main__":
    typer.run(get_spans)
