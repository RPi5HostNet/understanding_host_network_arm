# Understanding the Host Network: ARM Edition

# Directory Structure

`rpi/` directory contains the Python scripts to run the benchmarks. `finalized-data/` has the results of all the benchmarks. `graph.py` was used for generating the graphs in the report.

```tree
.
├── finalized-data/
├── graphs.py
├── README.md
└── rpi/
```

## `rpi`
```tree
.
├── clean.sh
├── data
├── fio.py
├── gapbs.py
├── p2m-iso
├── p2m-iso.fio
├── redis.py
├── run_all.py
├── run_stream_fio.py
├── stream_modified
├── stream_orig
├── stream.py
└── sum_stream_folders.sh
```

# Running the benchmarks
## Isolated benchmarks
### Fio
The `p2m-iso.fio` files contains the configuration used for isolated Fio runs. 

```bash
sudo fio ./p2m-iso.fio --output OUTPUT_FILE
```
runs fio with the specified configuration and stores the output in the specified `OUTPUT_FILE`. 
Fio is configured to run on core *3*

### GAPBS

GAPBS isolated benchmark is run using the `gapbs.py` file. By setting the `gapbs_core_list` variable to the desired cores, the program can be pinned to said cores. We have taken measurements for running on `[0]`, `[0, 1]`, `[0, 1, 2]` cores.

The configuration used here has $2^21$ nodes.

### STREAM
`stream.py` runs the STREAM benchmarks. 


## Co-located benchmarks

### Fio and STREAM
`run_stream_fio.py`  runs all R/W combinations of Fio and STREAM. 

### Fio and GAPBS
`fio.py` and `gapbs.py` are run together to co-locate  Fio and GAPBS. Fio's configuration has the runtime set to a large value. `fio.py` can be started first and then `gapbs.py` be started. 


The results are all stored in `data/` folder.



