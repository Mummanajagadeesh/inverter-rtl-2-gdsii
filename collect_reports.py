import os
import re

# Base reports folder
base_dir = r"runs\myrun\reports"

# Output file
output_file = "all_reports_summary_numbers.txt"

# Section names to look for
sections = [
    "report_tns",
    "report_wns",
    "report_worst_slack -max",
    "report_worst_slack -min"
]

# Compile regex to find numbers (integers or decimals)
num_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")

# Flow order for folders
flow_order = ["synthesis", "cts", "placement", "routing", "signoff"]

# List to store considered summary files
considered_files = []

# Dictionary to store extracted numbers per file
results = {}

for root, _, files in os.walk(base_dir):
    for fname in files:
        if fname.endswith(".summary.rpt"):
            # Relative path from base_dir
            rel_path = os.path.relpath(os.path.join(root, fname), base_dir)
            considered_files.append(rel_path)
            results[rel_path] = {}
            path = os.path.join(root, fname)
            try:
                with open(path, "r") as f:
                    content = f.read()
                    for section in sections:
                        section_pattern = re.compile(
                            rf"{section}\s*.*?===========================================================================\s*(.*?)(?=\n=+|$)",
                            re.DOTALL
                        )
                        match = section_pattern.search(content)
                        if match:
                            numbers = num_pattern.findall(match.group(1))
                            results[rel_path][section] = numbers[0] if numbers else "N/A"
                        else:
                            results[rel_path][section] = "N/A"
            except Exception as e:
                print(f"[Error reading {path}: {e}]")
                for section in sections:
                    results[rel_path][section] = "Error"

# Custom sorting function based on flow_order
def sort_key(rel_path):
    folder = rel_path.split(os.sep)[0]  # first folder in path
    try:
        order_index = flow_order.index(folder)
    except ValueError:
        order_index = len(flow_order)  # unknown folders go last
    return (order_index, rel_path)  # sort by flow, then name

# Write the table to output file
with open(output_file, "w") as out:
    out.write(f"Final reports at: {base_dir}\n\n")
    header = "File Name".ljust(50) + "".join([s.ljust(25) for s in sections])
    out.write(header + "\n")
    out.write("-" * len(header) + "\n")
    
    for rel_path in sorted(results.keys(), key=sort_key):
        row = rel_path.ljust(50)
        for section in sections:
            row += str(results[rel_path][section]).ljust(25)
        out.write(row + "\n")

# Print summary
print(f"\nAll numbers extracted into {output_file}")
print("\nList of summary report files considered:")
for f in sorted(considered_files, key=sort_key):
    print(f)
