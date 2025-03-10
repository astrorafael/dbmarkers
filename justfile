default:
    just --list

# Build the package
build:
    rm -fr dist/*
    uv build

# Publish the package to PyPi
publish pkg="dbmarkers": build
    twine upload -r pypi dist/*
    uv run --no-project --with {{pkg}} --refresh-package {{pkg}} \
        -- python -c "from {{pkg}} import __version__; print(__version__)"

# Publish to Test PyPi server
test-publish pkg="dbmarkers": build
    twine upload --verbose -r testpypi dist/*
    uv run --no-project  --with {{pkg}} --refresh-package {{pkg}} \
        --index-url https://test.pypi.org/simple/ \
        --extra-index-url https://pypi.org/simple/ \
        -- python -c "from {{pkg}} import __version__; print(__version__)"

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

