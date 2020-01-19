python rt.py
cd imgs
ffmpeg -framerate 30 -i test%%03d.png output.mp4
pause