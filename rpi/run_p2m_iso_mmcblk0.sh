#!/bin/sh
OUTPUT_FILE="$(date +'%Y%m%d_%H%M%S')_fio_iso_mmcblk0.txt"
sudo fio ./p2m-iso-mmcblk0.fio --output  "$OUTPUT_FILE"
