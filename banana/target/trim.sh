for i in `ls -1 *png`; do
convert $i  -flatten -fuzz 1% -trim +repage $i
done
