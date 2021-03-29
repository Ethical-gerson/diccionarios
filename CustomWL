#!/bin/bash
echo "Recuerda que debes tener python instalado" 
echo "Iniciando CeWL en" $1 
wget https://gist.githubusercontent.com/FrankSpierings/8809a737c63059f7447dfb380c1563f9/raw/b5e579ae206e80191fdd332dea77c8049425333b/crewl.py
pip install scrapy
pip3 install scrapy
timeout 20 python3 crewl.py https://$1 wordlist1
sed -i 'y/áÁàÀãÃâÂéÉêÊíÍóÓõÕôÔúÚñÑçÇ/aAaAaAaAeEeEiIoOoOoOuUnNcC/' wordlist1
cat wordlist1 | sed 's/[^a-z  A-Z]//g'| sort | uniq > wordlist2
cat wordlist2 | grep -E "[a-zA-Z]{3,10}" > WordList

rm wordlist1 wordlist2


echo "Finaliza  CeWl"
