import os

# Base reports folder
base_dir = r"runs\myrun\reports"

# Output file
output_file = "all_reports_summary.txt"

with open(output_file, "w") as outfile:
    for root, _, files in os.walk(base_dir):
        for fname in sorted(files):
            if fname.endswith(".summary.rpt") or fname.endswith(".rpt"):
                path = os.path.join(root, fname)
                outfile.write(f"\n{'='*80}\n")
                outfile.write(f"FILE: {path}\n")
                outfile.write(f"{'='*80}\n")
                try:
                    with open(path, "r") as f:
                        lines = f.readlines()
                        # You can filter specific lines if needed
                        for line in lines:
                            outfile.write(line)
                except Exception as e:
                    outfile.write(f"[Error reading {path}: {e}]\n")

print(f"\nAll reports collected into {output_file}")
