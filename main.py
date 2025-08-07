

import os
import asyncio

from utils import extract_reports_from_raw_file, save_reports_to_individual_files, basic_cleanup, translate_reports


async def extract_and_translate_reports(dest = 'de', save_original = False):

    file_path = "./documents/ReportsDATASET.csv"
    raw_reports = extract_reports_from_raw_file(file_path)
    reports = basic_cleanup(raw_reports)
    assert(len(reports)==1982)
    print(f"Extracted {len(reports)} reports from {file_path}")

    if save_original:
        output_dir = "output_reports"
        os.makedirs(output_dir, exist_ok=True)
        save_reports_to_individual_files(reports, output_dir)

    translated_reports = await translate_reports(reports, dest)
    print(f"Translated {len(translated_reports)} to {dest}")
    output_dir_de = f"output_reports_{dest}"
    os.makedirs(output_dir_de, exist_ok=True)
    save_reports_to_individual_files(translated_reports, output_dir_de)    


if __name__ == "__main__":
    import sys

    dest = 'de'
    save_original = False
    if len(sys.argv) >1:
        dest = sys.argv[1]
    
    if len(sys.argv) >2:
        save_original = sys.argv[2].lower()=='true'

    print(dest, save_original)
    asyncio.run(extract_and_translate_reports(dest = dest, save_original=save_original))


