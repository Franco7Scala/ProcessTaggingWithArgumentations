# Combining abstract argumentation and machine learning for efficiently analyzing low-level process event streams

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the code and resources for the framework presented in the research paper "Combining Abstract Argumentation and Machine Learning for Efficiently Analyzing Low-Level Process Event Streams". Our proposal addresses the challenge of analyzing and interpreting low-level process event streams by combining machine learning tagging capabilities with formal abstract argumentation theory, providing an explainable, robust, and logic-based approach to classify and annotate process elements.

## Key Features

* **Argumentation-Based Reasoning:** Exploits formal abstract argumentation frameworks to resolve conflicting interpretations of trace events and derive robust tags for process activities;
* **Explainable Tagging Framework:** Extends traditional sequence-tagging methods by providing a transparent, argumentative chain of reasoning for every assigned tag, enhancing user trust and interpretability;
* **Neuro-Symbolic Approach:** Combines a data-efficient machine learning sequence tagger (to suggest highly-probable candidate event interpretations) with an AAF-based reasoner to refine the results and compensate for the scarcity of annotated training data;
* **Reproducibility:** Facilitates replication of our research results, including the generation of the argumentation framework and the robustness evaluations on various process datasets.

## Repository Structure

* **`src/`**: Core source code directory.
  * `main.py`: Main entry point to run the tagging framework and evaluate the argumentation-based classifications;
  * `argumentation/`: Contains the logic for building and evaluating the Abstract Argumentation Frameworks (AAF), including arguments generation, attack relations, and acceptance evaluation;
  * `ml_tagger/`: Scripts to train and execute the sequence-tagging model for suggesting candidate event interpretations;
  * `dataset/`: Utilities for dataset loading, preprocessing, and formatting of the low-level process event streams;
  * `evaluation/`: Implementation of the evaluation metrics to compare our neuro-symbolic approach against baseline trace interpretation methods;
  * `utils/helper.py`: Helper functions for data manipulation and visualization.
    
* **`requirements.txt`**: List of project dependencies.

## Requirements

To run the code, ensure you have the libraries specified in `requirements.txt` installed. The main dependencies include:

* Python (>=3.8)
* NetworkX (for argumentation graph modeling)
* PyTorch / Scikit-learn (for the ML sequence tagger)
* NumPy
* Pandas

## Citation

```bibtex
  @article{Fazzinga2026,
    author = {Fazzinga, Bettina and Flesca, Sergio and Furfaro, Filippo and Pontieri, Luigi and Scala, Francesco},
    title = {Combining abstract argumentation and machine learning for efficiently analyzing low-level process event streams},
    journal = {Complex \& Intelligent Systems},
    year = {2026},
    month = {jun},
    volume = {12},
    number = {9},
    pages = {218},
    issn = {2198-6053},
    doi = {10.1007/s40747-026-02340-1},
    url = {https://doi.org/10.1007/s40747-026-02340-1},
  }
