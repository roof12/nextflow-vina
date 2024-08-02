#!/usr/bin/env python3

from indigo import Indigo

def read_sdf_file(indigo, sdf_input):
    """
    Reads an SDF file and extracts all molecules.
    
    Parameters:
    sdf_input(str): The path to the SDF file.
    
    Returns:
    list: A list of Indigo molecules.
    """
    molecules = []
    
    try:
        for molecule in indigo.iterateSDFile(sdf_input):
            molecules.append(molecule)
    except Exception as e:
        print(f"Error reading {sdf_input}: {e}")
    
    return molecules

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

def update_top_similarities(similarity_list, new_similarity, molecule_id, top_count):
    """
    Update the list of top similarities.
    
    Parameters:
    similarity_list (list): The current list of top similarities.
    new_similarity (float): The new similarity score.
    molecule_id(int): The molecule ID.
    
    Returns:
    list: The updated list of top similarities.
    """
    similarity_list.append((new_similarity, molecule_id))
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    return similarity_list[:top_count]

def write_similar_molecules_to_sdf(indigo, molecule, molecules, similarity_list, output_sdf):
    """
    Write the molecules in the similarity list to an SDF file.
    
    Parameters:
    molecules (list): List of all molecules.
    similarity_list (list): List of top similarities.
    output_sdf (str): Path to the output SDF file.
    """
    with indigo.writeFile(output_sdf) as sdf_writer:
        sdf_writer.sdfAppend(molecule)
        for similarity, mol_id in similarity_list:
            if mol_id < 0 or mol_id >= len(molecules):
                print(f"Molecule ID {mol_id} is out of range.")
                continue

            print(f"writing {mol_id} to sdf, similarity: {similarity}")
            out_mol = molecules[mol_id]
            sdf_writer.sdfAppend(out_mol)
    print(f"Similar molecules saved to {output_sdf}.")
    print(similarity_list)

def main(molecule, sdf_input, top_count, sdf_output):
    indigo = Indigo()
    top_similarities = []  # List to store top similarities

    # load molecule
    molecule = indigo.loadMoleculeFromFile(args.molecule)

    # read molecules for comparison from sdf
    molecules = read_sdf_file(indigo, sdf_input)
    print(f"Found {len(molecules)} molecules in {sdf_input}.")
 
    for i, mol in enumerate(molecules):
        fingerprint = fingerprint_molecule(mol)
        if fingerprint is not None:
            similarity = indigo.similarity(molecule, mol, "tanimoto")
            #print(f"Molecule {i} similarity: {similarity}")
            top_similarities = update_top_similarities(top_similarities, similarity, i, top_count)

    # Print the top similarities
    print("Top similarities:")
    for score, mol_id in top_similarities:
        print(f"Molecule {mol_id} Similarity = {score}")

    # Write similar molecules to SDF
    write_similar_molecules_to_sdf(indigo, molecule, molecules, top_similarities, sdf_output)

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

