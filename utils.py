# Load the file and print lines to understand the separator
def extract_reports_from_raw_file(file_path):
    reports = []
    current_report = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Strip leading/trailing whitespace
            line = line.strip()

            # Skip empty lines
            if line == "":
                continue

            # If line is only a double quote and we have a report, it’s a separator
            if line == '"' and current_report:
                full_report = " ".join(current_report).strip()
                reports.append(full_report)
                current_report = []
            elif line != '"':
                current_report.append(line)

    # Catch any final report not ended with a quote
    if current_report:
        full_report = " ".join(current_report).strip()



        reports.append( __basic_cleanup(full_report))

    return reports

def __basic_cleanup(reports):
    """
    Remove '"'   present in the reposts.
    """
    cleaned = []
    for report in reports:

        text = report.replace('"', '') 
        if text.lower() == "text" or len(text) < 100:
            continue
        cleaned.append(text)
    return cleaned

def save_reports_to_individual_files(reports, output_dir):
    import os
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for idx, report in enumerate(reports, start=1):
        # Clean up the report (optional)
        clean = report.strip()

        # Define the filename
        filename = f"report_{idx:04d}.txt"  # e.g., report_0001.txt

        # Full path
        file_path = os.path.join(output_dir, filename)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean)
    print(f"Saved {idx} reports {output_dir}")