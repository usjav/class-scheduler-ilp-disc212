import csv

# Input and output file names
input_file = "courses.csv"
output_file_mw = "courses_MW.csv"
output_file_tr = "courses_TR.csv"

# Open the input file
with open(input_file, mode="r") as infile:
    reader = csv.DictReader(infile)
    reader.fieldnames = [header.strip() for header in reader.fieldnames]  # Strip whitespace from headers

    # Prepare output files
    with open(output_file_mw, mode="w", newline="") as mw_file, \
         open(output_file_tr, mode="w", newline="") as tr_file:
        
        # Initialize writers with the same header as the input file
        headers = reader.fieldnames
        mw_writer = csv.DictWriter(mw_file, fieldnames=headers)
        tr_writer = csv.DictWriter(tr_file, fieldnames=headers)
        
        # Write headers to both output files
        mw_writer.writeheader()
        tr_writer.writeheader()
        
        # Process each row and write to the appropriate file
        for row in reader:
            days = row["Days"].strip()
            if days == "MW":
                mw_writer.writerow(row)
            elif days == "TR":
                tr_writer.writerow(row)
