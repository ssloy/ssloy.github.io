for i in `ls -1 *potential*png`; do
convert $i  -flatten -fuzz 1% -trim +repage `basename $i png`jpg
done
