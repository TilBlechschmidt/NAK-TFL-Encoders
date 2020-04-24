Xvfb $DISPLAY -ac -wr +render -noreset +extension GLX -screen 0 1920x1080x24 >/dev/null 2>&1 &
sleep 2

/evaluate.py
