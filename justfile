default:
    just --list


# test transcribe markers generation
transcribe:
    #!/usr/bin/env bash
    set -exuo pipefail
    uv run markers-transcribe --console --trace generate -i dbn2.txt -o "No Doubt - Just A Girl.xsc"
