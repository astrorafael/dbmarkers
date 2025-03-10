default:
    just --list


# test transcribe markers generation
transcribe:
    #!/usr/bin/env bash
    set -exuo pipefail
    uv run markers-transcribe --console --trace generate -i data/transcribe/dbm.txt -o data/transcribe/song.xsc

# test reaper project markers generation
reaper:
    #!/usr/bin/env bash
    set -exuo pipefail
    uv run markers-reaper --console --trace generate -i data/reaper/dbm.txt -o data/reaper/markers.csv

