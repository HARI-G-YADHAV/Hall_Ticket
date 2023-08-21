#convert html files in hallticket folder to pdf
dir=hallticket
cd $dir

mkdir pdf

for i in '*.html'	
	do
		wkhtmltopdf --user-style-sheet static/custom.css --page-size A4 --no-images $i a.pdf
	done

#!/bin/bash

input_pdf="a.pdf"
output_prefix="NA20PICS"

# Use pdftk to burst the PDF into individual pages
pdftk "$input_pdf" burst output tmp_%04d.pdf

# Rename the output files using the desired pattern
count=1
for page_pdf in tmp_*.pdf; do
    output_name="${output_prefix}$(printf "%02d" "$count").pdf"
    mv "$page_pdf" "$output_name"
    count=$((count + 1))
done

# Clean up temporary files
rm tmp_*.pdf


for i in '*.pdf'	
	do
		mv $i pdf
	done