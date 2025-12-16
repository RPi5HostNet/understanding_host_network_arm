function add_folder () {
  grep -h Throughput $1/stream-core* | cut -d ':' -f2 | tr -d ' ' | paste -sd+ | bc
}
