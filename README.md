# Legal Clause Extraction Pipeline

## Overview
This repository contains an end-to-end Machine Learning pipeline designed to automatically ingest, parse, and classify enterprise legal contracts (PDF and HTML). It extracts critical business clauses—specifically "Payment Terms" and "Limitation of Liability"—using Optical Character Recognition (OCR), Hugging Face Semantic Embeddings (`all-MiniLM-L6-v2`), and a Gradient Boosting Classifier.

## Data Handling & Reproducibility
* **Large Dataset Exclusion:** The complete contract corpus used to train and evaluate this model exceeds **14 GB**. To keep the repository lightweight and portable, the full corpus is stored externally.
* **Sample Data Provided:** A curated subset of sample contracts is retained in the `./data/data_test` directory. This allows the unit tests, command-line processing pipeline, and Streamlit UI to run out-of-the-box.

## Prerequisites
1. **Python 3.11** installed on your system.
2. **Tesseract OCR** binary installed:
   - *Windows*: Download from the UB-Mannheim repository and add to System Path.
   - *Linux*: Run `sudo apt-get update && sudo apt-get install tesseract-ocr`
   - *macOS*: Run `brew install tesseract`

## 1. Setup and Installation
Clone the repository and set up your virtual environment:

```bash
# Clone and enter the repository
git clone [https://github.com/minthihamoe9-max/end-to-end-ml-pipeline.git](https://github.com/minthihamoe9-max/end-to-end-ml-pipeline.git)
cd end-to-end-ml-pipeline

# Create and activate virtual environment (Windows)
python -m venv .env
.\.env\Scripts\activate

# Install dependencies
pip install -r requirements-details.txt