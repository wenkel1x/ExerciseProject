#!/bin/bash

REQ_FILE="$1"

if [[ ! -f "$REQ_FILE" ]]; then
    exit 1
fi
TEMP_REQS="$(mktemp)"
echo "auto_gptq" > "$TEMP_REQS"

parse_requirements() {
    local file="$1"
    while IFS= read -r line || [[ -n "$line" ]]; do
        line=$(echo "$line" | xargs)
        [[ -z "$line" || "$line" == \#* || "$line" =~ ^openvino* ]] && continue
        if [[ "$line" == -r* ]]; then
            included_file=$(echo "$line" | cut -d' ' -f2)
            included_path=$(realpath "$(dirname "$file")/$included_file")
            parse_requirements "$included_path"
        elif [[ "$line" == --* ]]; then
            echo "$line" >> "$TEMP_REQS"
        else
            pkg=$(echo "$line" | sed 's/[<>=!~].*//' | cut -d'#' -f1 | xargs)
            base_pkg=$(echo "$pkg" | sed 's/\[.*\]//')
            extras=$(echo "$pkg" | grep -oP '\[\K[^\]]+')
            echo "$base_pkg" >> "$TEMP_REQS"
            if [[ -n "$extras" ]]; then
                IFS=',' read -ra extra_pkgs <<< "$extras"
                for extra in "${extra_pkgs[@]}"; do
                    echo "$extra" >> "$TEMP_REQS"
                done
            fi
        fi
    done < "$file"
}

parse_requirements "$REQ_FILE"

freeze_output=$(pip freeze | awk '{print tolower($0)}'| sed 's/_/-/g')

> requirement_convert.txt
while IFS= read -r pkg; do
    if [[ "$pkg" == --* ]]; then
        echo "$pkg" >> requirement_convert.txt
    else
        base_pkg=$(echo "$pkg" | sed 's/\[.*\]//'| sed 's/_/-/g')
        match=$(echo "$freeze_output" | grep -Ei "^${base_pkg}==|^${base_pkg} @")
        if [[ -n "$match" ]]; then
            echo "$match" >> requirement_convert.txt
        else
            echo "not find: $pkg" >&2
        fi
    fi
done < "$TEMP_REQS"

rm "$TEMP_REQS"
echo "generate requirement_convert.txt done"