python rt.py
cd imgs
ffmpeg -framerate 30 -i test%%03d.png -qscale:v 30 -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p output.mp4
pause