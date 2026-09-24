# Legal Clause Extraction Pipeline

## Overview
This repository contains an end-to-end Machine Learning pipeline designed to automatically ingest, parse, and classify enterprise legal contracts (PDF and HTML). It extracts critical business clauses—specifically "Payment Terms" and "Limitation of Liability"—using Optical Character Recognition (OCR), Hugging Face Semantic Embeddings (`all-MiniLM-L6-v2`), and a Gradient Boosting Classifier.

## Data Handling & Reproducibility
**Note on Data Size:** The original contract corpus used to train and evaluate this model exceeds **14 GB**. To ensure this repository remains lightweight, portable, and within submission constraints, the full dataset has been excluded from this zip file. 

**Sample Data Provided:** A curated subset of sample contracts has been retained in the `./data/data_test` directory. This allows the unit tests, the command-line script, and the Streamlit UI to run successfully "out-of-the-box" for grading purposes. 


## Prerequisites
1. **Python 3.11** installed on your system.
2. **Tesseract OCR** binary installed:
   - *Windows*: Download from the UB-Mannheim repository and add to System Path.
   - *Linux*: Run `sudo apt-get update && sudo apt-get install tesseract-ocr`
   - *Mac*: Run `brew install tesseract`

## 1. Setup and Installation
Open your terminal and execute the following commands in order:

# Navigate to the project directory
cd "Project Folder Name"

# Activate your virtual environment (Windows)
.\-env\Scripts\activate


# Install the required Python packages
pip install -r requirements.txt or requirements-detailed.txt 


## 2. Running the Tests
Verify the integrity of the pipeline, file error handling, and data extraction logic by running the automated test suite on the provided sample data:

python scripts/unit_tests.py

*(A successful run will output "Ran 14 tests... OK" at the bottom of the terminal).*


## 3. Running the Application
Launch the graphical web interface to interactively upload sample contracts and download your extracted Excel results:

streamlit run scripts/app.py

*(This will automatically open a browser window at http://localhost:8501)*


## 4. Deploying with Docker
To completely containerize the application for deployment (packaging the OS dependencies, Tesseract, and Python libraries into one image), run these commands:

# Build the image
docker build -t ai-pipeline .

# Run the containerized application
docker run -p 8501:8501 ai-pipeline