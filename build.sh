#!/bin/bash

while [[ $# -gt 0 ]]
do
    INPUT="$1"
    case $INPUT in
        -o|--output-dir)
          OUTPUT="$2"
          shift 2
          ;;
        
        *)
            echo "Unknown command: $1. Try again"
            exit 1
    esac
done

[[ -n "$OUTPUT" ]] || { echo "error: --output-dir not provided" && exit 1; }

virtualenv .temp_venv
. .temp_venv/bin/activate

pip install -r requirements.txt

mkdir -p "$OUTPUT"
python -m nuitka --onefile --output-dir="$OUTPUT" pacman_game/main.py
cp -r pacman_game/Assets "$OUTPUT"/Assets

deactivate
rm -r .temp_venv
