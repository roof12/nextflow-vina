#!/usr/bin/env python3
import argparse
import random

def main(filename, num_lines):
    # Open the file
    with open(filename, "r") as f:
        # Use a reservoir sampling technique to select num_lines random lines
        reservoir = []
        line_number = 0

        for line in f:
            line_number += 1
            # Fill the reservoir with the first num_lines lines
            if len(reservoir) < num_lines:
                reservoir.append(line.rstrip())
            else:
                # Randomly replace elements in the reservoir
                random_index = random.randint(0, line_number - 1)
                if random_index < num_lines:
                    reservoir[random_index] = line.rstrip()

    # Print the sampled lines
    for line in reservoir:
        print(line)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sample lines from an input file")
    parser.add_argument("input_file", help="File to sample")
    parser.add_argument("num_lines", type=int, help="number of lines to sample")
    args = parser.parse_args()

    main(args.input_file, args.num_lines)

