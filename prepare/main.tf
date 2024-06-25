"""
Prepare ligands with Meeko
"""

def helpMessage() {
  log.info """
  Prepare ligands with Meeko
  """
}

def validateParameters() {
  if (!params.ligands) {
    log.error 'Missing input: ligands'
    exit 1
  }
}

process convertToMol {
  input:
  path ligands

  output:
  path "*.mol"

  publishDir "results"

  script:
  """
  obabel -i pdb ${ligands} -o mol -O ${ligands.baseName}.mol
  """
}

process addHydrogen() {
  input:
  path ligands

  output:
  path "*.mol" 

  publishDir "results"

  script:
  """
  obabel -h -i mol ${ligands} -o mol -O ${ligands.baseName}-with-h.mol
  """
}

process prepareLigand() {
  input:
  path ligands

  output:
  path "*.pdbqt"

  publishDir "results"

script:
  """
  mk_prepare_ligand.py -i ${ligands}
  """
}

workflow {
  if (params.help) {
    helpMessage()
    exit 0
  }

  validateParameters()

  ligandCh = channel.fromPath(params.ligands)

  // This can be used on pdb inputs.
  // However, I get errors unless I start with mol files
  // ERROR: Explicit valence for atom # 0 N, 4, is greater than permitted
  //
  // convertToMol(ligandCh)
  // addHydrogen(convertToMol.out)

  addHydrogen(ligandCh)

  prepareLigand(addHydrogen.out)
}

