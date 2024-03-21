"""
Create an evaluation and training corpus from span annotations. 

python -m scripts.spans_corpus
"""
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import srsly
import typer
from wasabi import msg

LABELLED_DATA_PATH = Path.cwd() / "assets/labelled/correct_guardian_llm.jsonl"


def _train_test_split(
    data: List[Dict[str, Any]], eval_split: float = 0.2, seed: int = 42
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split the data into a training and evaluation set.

    Args:
        data (List[Dict[str, Any]]): Labelled data to split.
        eval_split (int, optional): Evaluation split. Defaults to 0.2.
        seed (int, optional): Random seed. Defaults to 42.

    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: Training and evaluation data.
    """
    random.seed(seed)
    split_idx = int(len(data) * (1 - eval_split))
    train_data, test_data = data[:split_idx], data[split_idx:]
    return train_data, test_data


def split_data(
    data_path: Path = LABELLED_DATA_PATH, eval_split: float = 0.2, random_seed: int = 42
) -> None:
    """Split the data into a training and evaluation set.

    Args:
        data_path (Path, optional): Path to labelled data. Defaults to LABELLED_DATA_PATH.
        eval_split (int, optional): Eval split. Defaults to 0.2.
        seed (int, optional): Seed. Defaults to 42.
    """

    data = list(srsly.read_jsonl(data_path))
    accepted_data = [example for example in data if example["answer"] == "accept"]

    train_data, eval_data = _train_test_split(accepted_data, eval_split, random_seed)
    msg.info(
        f"Training data: {len(train_data)} examples; Evaluation data: {len(eval_data)} examples"
    )

    srsly.write_jsonl(
        data_path.with_name("train_correct_guardian_llm.jsonl"), train_data
    )
    srsly.write_jsonl(data_path.with_name("eval_correct_guardian_llm.jsonl"), eval_data)


if __name__ == "__main__":
    typer.run(split_data)
