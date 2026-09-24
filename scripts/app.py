import streamlit as st
import os
import subprocess
import shutil
import sys  # This is the magic library that fixes the environment issue!

# 1. Set up the web page design
st.set_page_config(page_title="Legal Extraction AI", layout="centered")
st.title("📄 Legal Contract Clause Extractor")
st.write("Upload your PDFs or HTML files below, and our AI will extract the Payment Terms and Liability clauses into a clean Excel file.")

# 2. Create temporary folders for the UI to use
INPUT_DIR = "./ui_input"
OUTPUT_DIR = "./ui_output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3. Create the File Uploader
uploaded_files = st.file_uploader("Upload Contracts (PDF/HTML)", type=["pdf", "html", "htm"], accept_multiple_files=True)

# 4. Create the Process Button
if st.button("Process Documents"):
    if not uploaded_files:
        st.warning("Please upload at least one document first!")
    else:
        with st.spinner("AI is reading your documents... This may take a few minutes per PDF."):
            
            # Save uploaded files to the input folder
            for uploaded_file in uploaded_files:
                with open(os.path.join(INPUT_DIR, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            
            try:
                
                command = [
                    sys.executable, "scripts/pipeline.py", 
                    "--input_folder", INPUT_DIR, 
                    "--output_folder", OUTPUT_DIR, 
                    "--model_folder", "./data/models",
                    "--output_format", "excel" 
                ]
                
              
                process = subprocess.run(command, capture_output=True, text=True)
                
                if process.returncode != 0:
                    st.error("The AI pipeline crashed! Here is the exact reason why:")
                    st.code(process.stderr)
                else:
                    # Generated Excel file
                    result_file = os.path.join(OUTPUT_DIR, "results.xlsx") 
                    
                    if os.path.exists(result_file):
                        st.success("✅ Processing Complete!")
                        
                        # 5. Create the Download Button
                        with open(result_file, "rb") as file:
                            btn = st.download_button(
                                label="📥 Download Excel Results",
                                data=file,
                                file_name="Extracted_Clauses.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    else:
                        st.error("Processing finished, but the Excel file was not found.")
            
            except Exception as e:
                st.error(f"A system error occurred: {e}")
            
            finally:
                # Clean up the input folder for the next user
                shutil.rmtree(INPUT_DIR, ignore_errors=True)