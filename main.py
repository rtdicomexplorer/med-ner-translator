
from utils import extract_reports_from_raw_file, save_reports_to_individual_files
import os





def extract_original_reports():

    file_path = "./documents/ReportsDATASET.csv"
    reports = extract_reports_from_raw_file(file_path)

    print(f"Extracted {len(reports)} reports from {file_path}")
    output_dir = "output_reports"
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    save_reports_to_individual_files(reports, output_dir)

    

if __name__ == "__main__":

   extract_original_reports()


