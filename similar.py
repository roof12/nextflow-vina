#!/usr/bin/env python3

from indigo import Indigo

indigo = Indigo()

def fingerprint_molecule(molecule):
    """
    Generate a fingerprint for a molecule using Indigo.
    
    Parameters:
    molecule (IndigoObject): An Indigo molecule object.
    
    Returns:
    str: The generated fingerprint as a string.
    """
    try:
        fingerprint = molecule.fingerprint("sim").oneBitsList()
        return ','.join(map(str, fingerprint))
    except Exception as e:
        print(f"Error generating fingerprint: {e}")
        return None

def update_top_similarities(similarity_list, new_similarity, molecule_id, molecule, top_count):
    """
    Update the list of top similarities.
    
    Parameters:
    similarity_list (list): The current list of top similarities.
    new_similarity (float): The new similarity score.
    molecule_id(int): The molecule ID.
    
    Returns:
    list: The updated list of top similarities.
    """
    similarity_list.append((new_similarity, molecule_id, molecule))
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    return similarity_list[:top_count]

def filenames_from_file(filename):
    with open(filename, "r") as file:
        for filename in file:
            yield filename.strip()

def extract_indigo_molecules_from_files(file_iterator):
    for filename in file_iterator:
        molecule = indigo.loadMoleculeFromFile(filename)
        yield molecule

def main(molecule, ligands_file, top_count):
    top_similarities = []  # List to store top similarities

    # load molecule
    molecule = indigo.loadMoleculeFromFile(molecule)
    molecules = extract_indigo_molecules_from_files(filenames_from_file(ligands_file))
    # for mol in molecules:
    #     print("------------------------")
    #     print(mol)

    i = 0
    print(f"Reading {ligands_file}:")
    for i, mol in enumerate(molecules):
        if i % 10000 == 0: print(".", end="", flush=True)
        fingerprint = fingerprint_molecule(mol)
        if fingerprint is not None:
            similarity = indigo.similarity(molecule, mol, "tanimoto")
            print(f"{similarity=}")
            top_similarities = update_top_similarities(top_similarities, similarity, i, mol, top_count)

    print(f"\nFound {i} molecules.")

    # Print the top similarities
    print("Top similarities:")
    for score, mol_id, _ in top_similarities:
        print(f"Molecule {mol_id} Similarity = {score}")


if __name__ == "__main__":
    import argparse
    import os
    import sys
   
    # parse args
    parser = argparse.ArgumentParser(description="Find similar molecules from an SDF file using Indigo fingerpints.")
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting the file if it exists')
    parser.add_argument("molecule", help="comparison molecule")
    parser.add_argument("ligands_file", help="SDF file containing the input molecules.")
    parser.add_argument("top_count", type=int, help="number of similar molecules to find")
    parser.add_argument("sdf_output", help="SDF file containing the output molecules.", nargs="?", default="")
    #args = parser.parse_args()

    molecule = "/home/scott/work/computational-drug-design/vina/klf15/mcule/2ent-small/mol/2ent-small-1.mol"
    ligands_file = "data/mol-ligands.txt"
    top_count = 2
    main(molecule, ligands_file, top_count)

