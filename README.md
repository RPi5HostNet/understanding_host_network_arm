# Understanding the Host Network: ARM Edition

This project seeks to evaluate the effects on the contention of the host network of the Raspberry PI. We draw inspiration from [Vuppalapati et al](#1).

## Directory Structure

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
### `fio`
The `p2m-iso.fio` files contains the configuration used for isolated Fio runs. 

```bash
sudo fio ./p2m-iso.fio --output OUTPUT_FILE
```
runs fio with the specified configuration and stores the output in the specified `OUTPUT_FILE`. 
`fio` is configured to run on core *3*

### `GAPBS`

`GAPBS` isolated benchmark is run using the `gapbs.py` file. By setting the `gapbs_core_list` variable to the desired cores, the program can be pinned to said cores. We have taken measurements for running on `[0]`, `[0, 1]`, `[0, 1, 2]` cores.

The configuration used here has $2^{21}$ nodes.

### `STREAM`
`stream.py` runs the `STREAM` benchmarks. 


## Co-located benchmarks

### `fio` and `STREAM`
`run_stream_fio.py`  runs all R/W combinations of Fio and STREAM. 

### `fio` and `GAPBS`
`fio.py` and `gapbs.py` are run together to co-locate  Fio and GAPBS. Fio's configuration has the runtime set to a large value. `fio.py` can be started first, followed by `gapbs.py`. 

The results are all stored in `data/` folder.


## `STREAM` Ouput
```tree
stream_alone_read_012
├── stream-core0
├── stream-core1
└── stream-core2

1 directory, 3 files
```

`STREAM` outputs are given in a per-core basis. To find the aggregated throughput, the results from each core
must to be added. `sum_stream_folders.sh` is used to perform this function. It defines a function `add_folder()`, which takes a folder name as its arguement and returns the aggregated throughput.

## Citation
This project is free for use for research/education. Please cite as below.

```
@software{Berberian_Understanding_the_Host_2025,
author = {Berberian, John and Chinnasame Rani, Deebakkarthi and Ermovick, Ethan},
month = dec,
title = {{Understanding the Host Network: ARM Edition}},
url = {https://github.com/RPi5HostNet/understanding_host_network_arm},
year = {2025}
}
```

## References
<a id="1">[1]</a>
Midhul Vuppalapati, Saksham Agarwal, Henry Schuh, Baris Kasikci,
Arvind Krishnamurthy, and Rachit Agarwal. 2024. Understanding the
Host Network. In Proceedings of the ACM SIGCOMM 2024 Conference
(ACM SIGCOMM ’24). Association for Computing Machinery, New
York, NY, USA, 581–594. https://doi.org/10.1145/3651890.3672271