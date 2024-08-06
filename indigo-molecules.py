#!/usr/bin/env python3
from indigo import Indigo

indigo = Indigo()

def filenames_from_file(filename):
    with open(filename, "r") as file:
        for filename in file:
            yield filename.strip()

def extract_indigo_molecules_from_files(file_iterator):
    for filename in file_iterator:
        yield indigo.loadMoleculeFromFile(filename)

if __name__ == "__main__":
        ligands_file = "data/mol-ligands.txt"
        molecules = extract_indigo_molecules_from_files(filenames_from_file(ligands_file))
        for molecule in molecules:
            print("------------------------")
            print(molecule)
