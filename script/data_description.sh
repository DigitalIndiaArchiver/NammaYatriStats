#!/bin/bash
for file in raw-data/*.json
do
  echo $file >> output.txt
  jq -r '.[0] | keys | @csv' "$file" >> output.txt
done
