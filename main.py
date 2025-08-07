

import os
import asyncio

from utils import extract_reports_from_raw_file, save_reports_to_individual_files, basic_cleanup, translate_reports


async def extract_original_reports():

    file_path = "./documents/ReportsDATASET.csv"
    raw_reports = extract_reports_from_raw_file(file_path)
    reports = basic_cleanup(raw_reports)
    print(f"Extracted {len(reports)} reports from {file_path}")
    output_dir = "output_reports"
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    save_reports_to_individual_files(reports, output_dir)

    dest = "de"
    translated_reports = await translate_reports(reports, dest)
    print(f"Translated {len(translated_reports)} to {dest}")
    output_dir_de = f"output_reports_{dest}"
    os.makedirs(output_dir_de, exist_ok=True)
    save_reports_to_individual_files(translated_reports, output_dir_de)    


if __name__ == "__main__":

    asyncio.run(extract_original_reports())


