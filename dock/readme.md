# Dock workflow

This currently is limited to local execution. Autodock Vina must be installed.

Parameters are listed in `nextflow.config`. You can create a file `params.yml` or pass them in on the command line.

Usage:

`nextflow run main.tf -params-file params.yml`

Results are symlinked into the directory `results`.

