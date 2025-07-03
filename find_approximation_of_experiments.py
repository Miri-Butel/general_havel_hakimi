import re
import os
import glob


def find_approximation_of_experiments(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        min_approx_ratio = 1  # Initialize to 1 since approx_ratio is between 0 and 1
        previous_line = None
        for line in infile:
            # Match lines containing 'n=' and 'p=' to extract n and p values
            match_n_p = re.search(r'n=(\d+),\s*p=([\d.]+)', line)
            # Match lines containing 'min:' to extract min value
            match_min = re.search(r'min:\s(\d+)', line)
            
            if match_n_p:
                previous_line = match_n_p.groups()  # Store n and p for later use
            elif match_min and previous_line:
                n, p = previous_line
                min_value = int(match_min.group(1))
                approx_ratio = min_value / (int(n) / 2)
                assert 0 <= approx_ratio <= 1, f"Invalid approx_ratio: {approx_ratio}"  # Ensure valid range
                min_approx_ratio = min(min_approx_ratio, approx_ratio)  # Update minimum
                outfile.write(f"n={n}, p={p}, min={min_value}, approx_ratio={approx_ratio:.4f}\n")
                previous_line = None  # Reset after processing

        outfile.write(f"\nMinimum approx_ratio: {min_approx_ratio:.4f}\n")


if __name__ == "__main__":
    # import argparse
    
    # parser = argparse.ArgumentParser(description="Find minimum approximation ratio from experiment logs.")
    # parser.add_argument('--input_filepath', type=str, help="Path to the input log file.", default="experiment_results/experiment_log.txt")
    # parser.add_argument('--output_filepath', type=str, help="Path to the output file for results.", default="experiment_results/experiments_approx_ratios_log.txt")
    
    # args = parser.parse_args()
    
    # input_filepath = args.input_filepath
    # output_filepath = args.output_filepath
    # find_approximation_of_experiments(input_filepath, output_filepath)

    experiment_dir = "experiment_results"  # Directory for both input and output files

    # Find all files matching the pattern "experiment_log_s*.txt"
    log_files = glob.glob(os.path.join(experiment_dir, "experiment_log_*s*.txt"))
    
    for log_file in log_files:
        base_name = os.path.basename(log_file).replace("experiment_log", "experiments_approx_ratios")
        output_file = os.path.join(experiment_dir, base_name)
        
        print(f"Processing {log_file} -> {output_file}")
        find_approximation_of_experiments(log_file, output_file)
