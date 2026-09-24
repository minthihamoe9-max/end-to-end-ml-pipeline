import glob
import os
import pickle
import time
from sentence_transformers import SentenceTransformer
import argparse
import logging
import pandas as pd
from sqlalchemy import create_engine

# Import your helper functions
# Ensure you have added the 'day_parser' function to helper_functions.py!
from helper_functions import (
    pdf_to_text_with_ocr, pull_text_from_html, read_text_files, 
    calculate_ocr_quality, plot_ocr_quality_histogram, 
    process_texts_to_dataframe, run_classification_model,
    day_parser 
)
# Configure logging (Exercise 3)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    sent_emb_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    logging.info("SentenceTransformer model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading SentenceTransformer model: {e}")
    exit(1)

def process_and_classify_files(input_folder, output_folder, model_folder, 
                               output_format='excel', threshold=0.5):
    """
    Orchestrates the pipeline with advanced logging and output options.
    """
    logging.info(f"Starting pipeline. Input: {input_folder}, Output Format: {output_format}")

    text_dir = os.path.join(output_folder, 'text_files')
    os.makedirs(text_dir, exist_ok=True)

    # 1. Ingest Files with Advanced Logging (Exercise 3.2 & 3.3)
    pdf_files = glob.glob(os.path.join(input_folder, '*.pdf'))
    html_files = glob.glob(os.path.join(input_folder, '*.html')) + glob.glob(os.path.join(input_folder, '*.htm'))
    
    logging.info(f"Files identified: {len(pdf_files)} PDFs, {len(html_files)} HTMLs.") # Exercise 3.2

    for pdf_file in pdf_files:
        start_time = time.time()
        try:
            pdf_to_text_with_ocr(pdf_file, text_dir)
            duration = time.time() - start_time
            logging.info(f"OCR Complete: {os.path.basename(pdf_file)} in {duration:.2f}s") # Exercise 3.3
        except Exception as e:
            logging.error(f"Failed OCR on {pdf_file}: {e}")

    # (HTML processing remains similar...)
    html_texts = pull_text_from_html(html_files)
    for html_file, text_content in zip(html_files, html_texts):
        if text_content:
            file_name = os.path.basename(html_file).rsplit('.', 1)[0] + '.txt'
            with open(os.path.join(text_dir, file_name), 'w', encoding='utf-8') as f:
                f.write(text_content)

    # 2. Process Data & Classification
    texts, filenames = read_text_files(text_dir)
    df = process_texts_to_dataframe(texts, filenames)
    df['Embedding'] = df['sentence_text'].apply(lambda x: sent_emb_model.encode(x))
    
    df_model_results = run_classification_model(df, model_folder, threshold=threshold)

    # 3. Day Parser Integration (Exercise 1.3 & 1.4)
    # We apply the parser to the context identified by the model
    logging.info("Running Day Parser on extracted contexts...")
    df_model_results['parsed_days'] = df_model_results['sentence_text'].apply(day_parser)

    # 4. Flexible Output Options (Exercise 4.3)
    if output_format == 'excel':
        path = os.path.join(output_folder, 'results.xlsx')
        df_model_results.to_excel(path, index=False)
        logging.info(f"Saved Excel to {path}")
    
    elif output_format == 'pickle':
        path = os.path.join(output_folder, 'results.pkl')
        df_model_results.to_pickle(path)
        logging.info(f"Saved Pickle to {path}")
        
    elif output_format == 'sql':
        engine = create_engine(f"sqlite:///{os.path.join(output_folder, 'results.db')}")
        df_model_results.to_sql('classifications', engine, if_exists='replace')
        logging.info("Saved results to SQLite database.")

    return df_model_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End ML Pipeline")
    parser.add_argument("--input_folder", required=True)
    parser.add_argument("--output_folder", required=True)
    parser.add_argument("--model_folder", required=True)
    parser.add_argument("--output_format", choices=['excel', 'pickle', 'sql'], default='excel') # Exercise 4.3
    parser.add_argument("--threshold", type=float, default=0.5)

    args = parser.parse_args()
    process_and_classify_files(args.input_folder, args.output_folder, 
                               args.model_folder, args.output_format, args.threshold)
    

    