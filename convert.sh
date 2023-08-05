#convert html files in hallticket folder to pdf
dir=hallticket
cd $dir

sudo apt-get update
sudo apt install libreoffice

mkdir pdf

for i in '*.html'	
	do
		lowriter --convert-to pdf $i
	done

for i in '*.pdf'	
	do
		mv $i pdf
	done