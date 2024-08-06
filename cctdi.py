def fingerprint_molecule(molecule):
    """
    Generate a fingerprint for a molecule using Indigo.
    
    Args:
        molecule (IndigoObject): An Indigo molecule object.
    
    Returns:
        str: The generated fingerprint as a string.
             Returns None if there is an error generating the fingerprint.
    """

    try:
        fingerprint = molecule.fingerprint("sim").oneBitsList()
        return ','.join(map(str, fingerprint))
    except Exception as e:
        print(f"Error generating fingerprint: {e}")
        return None

def update_top_similarities(similarity_list, new_similarity, molecule, filename, top_count):
    """
    Update the list of top similarities with a new similarity score.

    Args:
        similarity_list (list): The current list of top similarities.
        new_similarity (float): The new similarity score to be added.
        molecule (IndigoObject): The Indigo molecule object associated with the similarity score.
        filename (str): The filename associated with the molecule.
        top_count (int): The maximum number of top similarities to retain in the list.

    Returns:
        list: The updated list of top similarities, sorted by similarity score in descending order.
    """

    similarity_list.append((new_similarity, molecule, filename))
    similarity_list.sort(reverse=True, key=lambda x: x[0])
    return similarity_list[:top_count]

def filenames_from_file(filename):
    """
    Generate filenames from a file containing filenames, one per line.

    Args:
        filename (str): Path to the file containing filenames.

    Yields:
        str: Each filename stripped of surrounding whitespace.
    """

    with open(filename, "r") as file:
        for filename in file:
            yield filename.strip()

def read_indigo_molecules_from_files(indigo, file_iterator):
    """
    Extract Indigo molecules from files using an Indigo instance.

    Args:
        indigo (Indigo): An instance of the Indigo toolkit.
        file_iterator (iterable): An iterable providing filenames.

    Yields:
        tuple: A tuple containing the Indigo molecule object and the filename from which it was extracted.
    """
    for filename in file_iterator:
        molecule = indigo.loadMoleculeFromFile(filename)
        yield molecule, filename

