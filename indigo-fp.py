#!/usr/bin/env python3

from indigo import Indigo

def sdf_input_iterator(indigo, sdf_input):
    """
    Returns a molecule iterator from an SDF file.
    
    Parameters:
    sdf_input(str): The path to the SDF file.
    
    Returns:
    iterator: An iterator of Indigo molecules.
    """

    return indigo.iterateSDFile(sdf_input)

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

def write_similar_molecules_to_sdf(indigo, molecule, similarity_list, output_sdf):
    """
    Write the molecules in the similarity list to an SDF file.
    
    Parameters:
    molecule (IndigoObject): 
    similarity_list (list): List of top similarities.
    output_sdf (str): Path to the output SDF file.
    """
    with indigo.writeFile(output_sdf) as sdf_writer:
        sdf_writer.sdfAppend(molecule)
        for _, _, similar_molecule in similarity_list:
            sdf_writer.sdfAppend(similar_molecule)
    print(f"Similar molecules saved to {output_sdf}.")

def main(molecule, sdf_input, top_count, sdf_output):
    indigo = Indigo()
    top_similarities = []  # List to store top similarities

    # load molecule
    molecule = indigo.loadMoleculeFromFile(args.molecule)

    # read molecules for comparison from sdf
    molecules = sdf_input_iterator(indigo, sdf_input)

    i = 0
    print(f"Reading {sdf_input}:")
    for i, mol in enumerate(molecules):
        if i % 10000 == 0: print(".", end="", flush=True)
        fingerprint = fingerprint_molecule(mol)
        if fingerprint is not None:
            similarity = indigo.similarity(molecule, mol, "tanimoto")
            top_similarities = update_top_similarities(top_similarities, similarity, i, mol, top_count)

    print(f"\nFound {i} molecules.")

    # Print the top similarities
    print("Top similarities:")
    for score, mol_id, _ in top_similarities:
        print(f"Molecule {mol_id} Similarity = {score}")

    # Write similar molecules to SDF
    write_similar_molecules_to_sdf(indigo, molecule, top_similarities, sdf_output)

if __name__ == "__main__":
    import argparse
    import os
    import sys
   
    # parse args
    parser = argparse.ArgumentParser(description="Find similar molecules from an SDF file using Indigo fingerpints.")
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting the file if it exists')
    parser.add_argument("molecule", help="comparison molecule")
    parser.add_argument("sdf_input", help="SDF file containing the input molecules.")
    parser.add_argument("top_count", type=int, help="number of similar molecules to find")
    parser.add_argument("sdf_output", help="SDF file containing the output molecules.", nargs="?", default="")
    args = parser.parse_args()

    sdf_output = args.sdf_output or f"top-{args.top_count}-similar.sdf"

    # error and exit if file exists and no overwrite
    if os.path.isfile(args.sdf_output):
        if not args.overwrite:
            print(f"Error: File '{args.sdf_output}' already exists and overwrite is not allowed.")
            sys.exit(1)

    main(args.molecule, args.sdf_input, args.top_count, sdf_output)

