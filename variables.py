#!/bin/bash

# get the path from google colab
path="."

# Count the number of png files in the current directory
num_files=$(ls -1q *.png | wc -l)
echo "┌───────────────────────────────────┐"
echo "│ Found ${num_files} PNG Files"
echo "└───────────────────────────────────┘"
#change the filename 
#counter=-1
#for file in $(ls -1t *.png); do # counts wrong direction
#  counter=$((counter+1))
#  mv "$file" "$(printf '%03d' $counter)-$file"
#done

# Get the first filename
first=$(find $path -maxdepth 1 -name '*.png' -printf "%f\n" | sort -n | head -1)
first_path="$path/$first"


# Remove the first digits from the first filename
new_name=$(echo $first)

# Add the counted variable in front of it and make sure it has the desired format
formatted_num=$(printf "%03d" $num_files)
new_filename="$formatted_num"-"$new_name"

# Check if the new filename already exists
if [ ! -f "$path/$new_filename" ]; then
  echo "┌───────────────────────────────────┐" 
  echo "│ Copying first image: ${first_path}"
  echo "| Adding as loop-frame: ${new_filename}"
  echo "└───────────────────────────────────┘"
  cp "$first_path" "$path/$new_filename"
else
  echo "┌───────────────────────────────────┐"
  echo "Skipping: ${new_filename} already exists"
  echo "└───────────────────────────────────┘"
fi
