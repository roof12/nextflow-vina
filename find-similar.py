#!/usr/bin/env python3

from cctdi import read_indigo_molecules_from_files, update_top_similarities, fingerprint_molecule, filenames_from_file
from indigo import Indigo

indigo = Indigo()

def main(molecule, ligands_file, top_count, verbose=False):
    top_similarities = []  # List to store top similarities

    # load molecule
    molecule = indigo.loadMoleculeFromFile(molecule)
    molecules = read_indigo_molecules_from_files(indigo, filenames_from_file(ligands_file))

    if verbose: print(f"Reading {ligands_file}:")

    i = 0
    for i, (mol, filename) in enumerate(molecules):
        if verbose and i % 10000 == 0: print(".", end="", flush=True)
        fingerprint = fingerprint_molecule(mol)
        if fingerprint is not None:
            similarity = indigo.similarity(molecule, mol, "tanimoto")
            top_similarities = update_top_similarities(top_similarities, similarity, mol, filename, top_count)

    if verbose:
        print(f"\nFound {i} molecules.")
        print("Top similarities:")
        for score, _, filename in top_similarities:
            print(f"Molecule '{filename}' similarity = {score}")

    for _, _, filename in top_similarities:
        print(filename)

if __name__ == "__main__":
    import argparse
   
    # parse args
    parser = argparse.ArgumentParser(description="Find similar molecules.")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument("molecule", help="comparison molecule")
    parser.add_argument("ligands_file", help="file containing the filenames of input molecules")
    parser.add_argument("top_count", type=int, help="number of similar molecules to find")
    args = parser.parse_args()

    main(args.molecule, args.ligands_file, args.top_count, args.verbose)

