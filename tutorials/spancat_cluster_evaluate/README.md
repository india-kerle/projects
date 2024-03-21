<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Evaluation techniques in a DS pipeline with multiple components 

This example project demonstrates various evaluation considerations when building an end-to-end data science pipeline that contains multiple components. 

The components include:

1. **Extracting Spans**: A SpanCat model is used to extract spans like `Project`, `Initative`, `Technology` and `Policy` from climate-related newspaper articles from the Guardian. An example of the labelling task is shown below:

<p align="center">
  <img src="tutorials/spancat_cluster_evaluate/images/label_example.png" alt="SpanCat labelling"/>
</p>

2. **Clustering Spans**: The extracted spans are then clustered to create a list of unique entities.

3. **Labelling Clusters**: A Large Language Model is used to label the clusters.

A number of evaluation techniques are used to assess the performance of the pipeline. These include:

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `fetch-news` | Fetch data on from the Environment section using the Guardian's API |
| `prodigy-llm-label` | Label a sample of the news data in bulk using `spacy-llm` |
| `prodigy-llm-review` | Review the LLM-labelled news data |
| `prodigy-spans-correct` | Label additional Guardian data using smaller, task specific spancat model |
| `spancat-corpus` | Create train and evaluate databases based on the reviewed training data |
| `spancat-train` | Train spancat model using reviewed LLM labels |
| `spancat-evaluate` | Print evaluation metrics of spancat model|
| `spancat-extract` | Apply the SpanCat model to the Guardian data |
| `cluster-spans` | Cluster the extracted spans to create a list of unique entities |
| `cluster-label` | Use an LLM to label the clusters |
| `cluster-evaluate` | Evaluate pipelines related to clustering spans |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `data` | `fetch-news` |
| `label` | `prodigy-llm-label` &rarr; `prodigy-llm-review` &rarr; `prodigy-spans-correct` |
| `spancat` | `spancat-corpus` &rarr; `spancat-train` &rarr; `spancat-evaluate` &rarr; `spancat-extract` |
| `cluster` | `cluster-spans` &rarr; `cluster-label` &rarr; `cluster-evaluate` |
| `evaluate` | `spancat-evaluate` &rarr; `cluster-evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| [`assets/guardian_data_sample.jsonl`](assets/raw/guardian_data_sample.jsonl) | Local | An initial sample of Guardian articles to bulk label using an LLM|
| [`assets/raw/guardian_data.jsonl`](assets/raw/guardian_data.jsonl) | Local | A full dataset of Guardian articles |
| [`assets/labelled/labelled_guardian_data_llm.jsonl`](assets/labelled/labelled_guardian_data_llm.jsonl) | Local | LLM-generated span labels for the sample of Guardian articles |
| [`assets/labelled/correct_guardian_llm.jsonl`](assets/labelled/correct_guardian_llm.jsonl) | Local | Human-in-the-loop corrected Guardian labels |
| [`assets/labelled/train_correct_guardian_llm.jsonl`](assets/labelled/train_correct_guardian_llm.jsonl) | Local | Training data from the corrected Guardian labels |
| [`assets/labelled/eval_correct_guardian_llm.jsonl`](assets/labelled/train_correct_guardian_llm.jsonl) | Local | Evaluation data from the corrected Guardian labels |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
