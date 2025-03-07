for i in `seq 0 6`; do
ffmpeg -i fire$i.webm -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" fire$i.mp4
done
