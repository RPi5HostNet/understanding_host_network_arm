#!/bin/sh
OUTPUT_FILE="$(date +'%Y%m%d_%H%M%S')_fio_iso"
sudo fio ./p2m-iso.fio --output  "$OUTPUT_FILE"
