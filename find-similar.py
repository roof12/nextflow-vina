#!/usr/bin/env python3

from cctdi import read_indigo_molecules_from_files, update_top_similarities, fingerprint_molecule, filenames_from_file
from indigo import Indigo

indigo = Indigo()

def main(molecule, ligands_file, top_count, log=None):
    top_similarities = []  # List to store top similarities

    # load molecule
    molecule = indigo.loadMoleculeFromFile(molecule)
    molecules = read_indigo_molecules_from_files(indigo, filenames_from_file(ligands_file))

    if log: log.write(f"Reading {ligands_file}:\n")

    i = 0
    for i, (mol, filename) in enumerate(molecules):
        if log and i % 1 == 0: log.write(".")
        fingerprint = fingerprint_molecule(mol)
        if fingerprint is not None:
            similarity = indigo.similarity(molecule, mol, "tanimoto")
            top_similarities = update_top_similarities(top_similarities, similarity, mol, filename, top_count)

    if log:
        log.write(f"\nFound {i} molecules.\n")
        log.write("Top similarities:\n")
        for score, _, filename in top_similarities:
            log.write(f"Molecule '{filename}' similarity = {score}\n")

    for _, _, filename in top_similarities:
        print(filename)

if __name__ == "__main__":
    import argparse
   
    # parse args
    parser = argparse.ArgumentParser(description="Find similar molecules.")
    parser.add_argument('-l', '--logfile', help='Output file with log information')
    parser.add_argument("molecule", help="comparison molecule")
    parser.add_argument("ligands_file", help="file containing the filenames of input molecules")
    parser.add_argument("top_count", type=int, help="number of similar molecules to find")
    args = parser.parse_args()

    log = None
    if args.logfile:
        log = open(args.logfile, 'w')

    main(args.molecule, args.ligands_file, args.top_count, log)

    if log: log.close()

