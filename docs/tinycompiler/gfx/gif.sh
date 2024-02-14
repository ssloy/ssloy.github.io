#for i in `seq 0 6`; do ffmpeg -y -i fire$i.webm -vf palettegen palette$i.png ; ffmpeg -y -i fire$i.webm -i palette$i.png -filter_complex paletteuse -s 320x167 -r 30 fire$i.gif ; rm palette$i.png ; done
#ffmpeg -i breakout.webm  -vf "fps=30,scale=336:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=4:reserve_transparent=0[p];[s1][p]paletteuse" -loop 0 breakout.gif
#ffmpeg -i sunset-race.webm  -vf "fps=20,scale=336:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:reserve_transparent=0[p];[s1][p]paletteuse" -loop 0 sunset-race.gif
ffmpeg -i metaballs.webm  -vf "fps=10,scale=336:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:reserve_transparent=0[p];[s1][p]paletteuse" -loop 0 metaballs.gif
