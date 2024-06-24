// main.nf

def helpMessage() {
  log.info """
  vina pipeline
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

process vina {
    input:
    path ligands

    output:
    path "*"

    publishDir "results"

    // Command to run AutoDock Vina
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

// Define workflow input
workflow {
  if (params.help) {
    helpMessage()
    exit 0
  }

  validateParameters()

  ligand_ch = channel.fromPath(params.ligands)
  vina(ligand_ch)
}

