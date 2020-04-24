#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, time
from scipy.interpolate import interp1d
from threading import Thread
import numpy
import os
import csv
import json
import subprocess
import psutil

display = ":42"
cmdline_codec = os.environ['CODEC_CMDLINE']   # "-c:v libx264rgb -crf 0 -preset ultrafast -g 30 -f mp4 -movflags +frag_keyframe+empty_moov+default_base_moof"
cmdline = "ffmpeg -y -rtbufsize 1500M -probesize 100M -framerate 15 -video_size 1920x1080 -f x11grab -i " + display + " -t 00:01:00 -threads 1 " + cmdline_codec
driver = webdriver.Firefox()

sites = [
    # Regular websites
    "http://www.python.org",

    # Stress the codec with particles
    "https://vincentgarreau.com/particles.js/#nasa",
    "https://codepen.io/themegatb/full/VwvaNpv",
    "https://vincentgarreau.com/particles.js/#nyancat2",

    # Some UI animations
    "https://www.highcharts.com/demo",
    "https://www.highcharts.com/demo/column-stacked",
    "https://www.highcharts.com/demo/column-parsed"
]

def scroll_script(speed):
    return """
        function scroll() {{
            document.scrollingElement.scrollTop += {step};
            window.requestAnimationFrame(scroll);
        }}

        scroll()
    """.format(step=speed)

def scroll(speed):
    sleep(2)
    driver.execute_script(scroll_script(speed))

def setup_browser():
    driver.set_window_size(1920, 1080)

def do_browser_stuff():
    # Iterate over all the pages
    for site in sites:
        driver.get(site)
        sleep(3)

    # Finish off with some scrolling on a heavily scroll-animated and "contentful" web-page
    driver.get("https://www.apple.com/de/macbook-pro-16/")
    scroll(20)

def read_bitrate(path):
    ffprobe_cmd = ("ffprobe -v error -select_streams v:0 -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 " + path).split(" ")
    ffprobe = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ffprobe.wait()
    stdout, stderr = ffprobe.communicate()

    # If no bitrate is available (e.g. raw video)
    if stdout == b'N/A\n':
        stdout = b'-1'

    return int(stdout)

def record():
    animator = Thread(target=do_browser_stuff)
    ffmpeg = subprocess.Popen(cmdline.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process = psutil.Process(ffmpeg.pid)

    animator.start()

    recordingInfo = {
        "bitrate": 0,
        "memory": [],
        "times": {
            "user": [],
            "system": [],
            "wall": []
        },
        "io": {
            "read": [],
            "write": []
        }
    }

    while ffmpeg.poll() is None:
        # Don't use too much CPU
        sleep(0.25)

        # Grab some data from the process
        with process.oneshot():
            memory = process.memory_info().rss / 1024 / 1024
            times = process.cpu_times()
            timestamp = round(time() - process.create_time(), 4)
            io = process.io_counters()

            recordingInfo['memory'].append(memory)

            recordingInfo['times']['user'].append(times.user)
            recordingInfo['times']['system'].append(times.system)
            recordingInfo['times']['wall'].append(timestamp)

            recordingInfo['io']['read'].append(io.read_chars)
            recordingInfo['io']['write'].append(io.write_chars)

    process.wait()
    animator.join()

    recordingInfo['bitrate'] = read_bitrate(cmdline.split(" ")[-1])

    stdout, stderr = ffmpeg.communicate()
    with open('/out/log.txt', 'ab') as log:
        log.write(stdout)

    return recordingInfo

print("\t" + cmdline, flush=True)
setup_browser()
measurements = []

sample_size = int(os.environ.get('SAMPLE_SIZE', "20"))

for i in range(0, sample_size):
    print("\tBuild " + str(i), flush=True)
    measurements.append(record())

result = {
    "cmdline": cmdline,
    "measurements": measurements,
}

with open('/out/data.json', 'w') as file:
    json.dump(result, file, sort_keys=True)
