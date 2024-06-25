"""
Dock prepared ligands with Vina.
"""

def helpMessage() {
  log.info """
  Dock prepared ligands with Vina. 
  """
}

def validateParameters() {
  if (!params.receptor) {
    log.error 'Missing input: receptor'
    exit 1
  }
 
  if (!params.ligands) {
    log.error 'Missing input: ligands'
    exit 1
  }

  if (!params.center_x.toString().isNumber()) {
    log.error "Parameter must be a number: center_x"
    exit 1
  }

  if (!params.center_y.toString().isNumber()) {
    log.error "Parameter must be a number: center_y"
    exit 1
  }

  if (!params.center_z.toString().isNumber()) {
    log.error "Parameter must be a number: center_z"
    exit 1
  }

  if (!params.size_x.toString().isNumber()) {
    log.error "Parameter must be a number: size_x"
    exit 1
  }

  if (!params.size_y.toString().isNumber()) {
    log.error "Parameter must be a number: size_y"
    exit 1
  }

  if (!params.size_z.toString().isNumber()) {
    log.error "Parameter must be a number: size_z"
    exit 1
  }
}

// Dock with Vina, saving the docked file and stdout
process vina {
  input:
  path ligands

  output:
  path "*-out.txt", emit: outputs
  path "*-docked.pdbqt", emit: dockings

  publishDir "results"


  script:
  """
  vina --receptor ${params.receptor} \
       --ligand ${ligands} \
       --out ${ligands.baseName}-docked.pdbqt \
       --num_modes ${params.num_modes} \
       --exhaustiveness ${params.exhaustiveness} \
       --center_x ${params.center_x} \
       --center_y ${params.center_y} \
       --center_z ${params.center_z} \
       --size_x ${params.size_x} \
       --size_y ${params.size_y} \
       --size_z ${params.size_z} > ${ligands.baseName}-out.txt
  """
}

// Extract the ligand name and score from the docking output
process extractScores {
  input:
  path outputs

  output:
  stdout

  script:
  """
#!/usr/bin/env python3

def getLigandAndValues(filename):
  ligand = None
  with open(filename, "r") as file:
    for line in file:
      if line.startswith("Ligand: "):
        ligand = line.strip().split()[1]
      elif line.startswith("   1 "):
        return [ligand] + line.split()

values = getLigandAndValues("${outputs}")
print(",".join(values))
  """
}

workflow {
  if (params.help) {
    helpMessage()
    exit 0
  }

  receptorName = Path.of(params.receptor).baseName
  validateParameters()

  ligandCh = channel.fromPath(params.ligands)
  vina(ligandCh)
  extractScores(vina.out.outputs) | collectFile(name: "${receptorName}-scores.csv", storeDir: "results")
}

