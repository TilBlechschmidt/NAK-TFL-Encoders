\pagebreak
\pagenumbering{roman}
\setcounter{page}{4}

\section*{Literature}
\addcontentsline{toc}{section}{Literature}

<div id="refs"></div>

\pagebreak
\appendix
\section*{Appendices}
\addcontentsline{toc}{section}{Appendices}
\renewcommand{\thesubsection}{\Alph{subsection}}

## Figures

![Global browser marketshare (March 2019) [@browser-marketshare]](src/graphs/browser_marketshare.pdf){#fig:browsers}

![Screen resolutions in Germany (March 2019) [@screen-resolution-germany]](src/graphs/resolution_marketshare.pdf){#fig:resolutions}

## Code listings

Below is a list of parameters and python scripts that have been used to take all measurements. Additionally the Dockerfile containing the desktop environment and browser has been included. All files listed below can be accessed online at GitHub, however the link has been excluded from this version of the document to retain author anonymity.

### Codec parameters {#sec:codec-list}

The following list has been used to execute the test runs and each cmdline was combined with the common prefix `ffmpeg -y -rtbufsize 1500M -probesize 100M -framerate 15 -video_size 1920x1080 -f x11grab -i :42 -t 00:01:00 -threads 1`.

\tiny

```json
    {
        "name": "Raw",
        "pixel_format": "bgr0",
        "compression": false,
        "container": "nut",
        "cmdline": "-c:v rawvideo -pix_fmt bgr0"
    },

    {
        "name": "H.264",
        "pixel_format": "rgb24",
        "compression": false,
        "container": "mp4",
        "cmdline": "-c:v libx264rgb -preset ultrafast -crf 0 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30 -f mp4"
    },
    {
        "name": "H.264",
        "pixel_format": "rgb24",
        "compression": true,
        "container": "mp4",
        "cmdline": "-c:v libx264 -preset ultrafast -crf 28 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30 -f mp4"
    },

    {
        "name": "H.264",
        "pixel_format": "yuv420p",
        "compression": false,
        "container": "mp4",
        "cmdline": "-c:v libx264 -preset ultrafast -crf 0 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30 -f mp4"
    },
    {
        "name": "H.264",
        "pixel_format": "yuv420p",
        "compression": true,
        "container": "mp4",
        "cmdline": "-c:v libx264 -preset ultrafast -crf 28 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30 -f mp4"
    },

    {
        "name": "H.265",
        "pixel_format": "yuv420p",
        "compression": false,
        "container": "mp4",
        "cmdline": "-c:v libx265 -preset ultrafast -x265-params lossless=1 -pix_fmt yuv420p -f mp4"
    },
    {
        "name": "H.265",
        "pixel_format": "yuv420p",
        "compression": true,
        "container": "mp4",
        "cmdline": "-c:v libx265 -preset ultrafast -crf 28 -pix_fmt yuv420p -f mp4"
    },

    {
        "name": "VP9",
        "pixel_format": "yuv420p",
        "compression": false,
        "container": "webm",
        "cmdline": "-c:v libvpx-vp9 -lossless 1 -cpu-used 8 -deadline realtime -pix_fmt yuv420p"
    },
    {
        "name": "VP9",
        "pixel_format": "yuv420p",
        "compression": true,
        "container": "webm",
        "cmdline": "-c:v libvpx-vp9 -crf 35 -b:v 0 -cpu-used 8 -deadline realtime -pix_fmt yuv420p"
    },

    {
        "name": "ProRes",
        "pixel_format": "yuv422p10le",
        "compression": true,
        "container": "mov",
        "cmdline": "-c:v prores_ks -profile:v 0 -qscale:v 13 -pix_fmt yuv422p10le"
    },

    {
        "name": "VC2",
        "pixel_format": "yuv420p",
        "compression": true,
        "container": "nut",
        "cmdline": "-c:v vc2 -wavelet_depth 1 -b 320K -pix_fmt yuv420p"
    }
```

\normalsize

### Browser control code and CPU measuring code {#sec:browsercontrol}

The following file is executed within the Docker container to record the screen, take measurements and automate the browser. It is called `evaluate.py` on disk.

\tiny

```python
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
cmdline_codec = os.environ['CODEC_CMDLINE']
cmdline = "ffmpeg -y -rtbufsize 1500M -probesize 100M -framerate 15 -video_size 1920x1080 -f x11grab -i "
    + display +
    " -t 00:01:00 -threads 1 "
    + cmdline_codec
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
    print("\tBuild " + str(i + 1) + "/" + str(sample_size), flush=True)
    measurements.append(record())

result = {
    "cmdline": cmdline,
    "measurements": measurements,
}

with open('/out/data.json', 'w') as file:
    json.dump(result, file, sort_keys=True)
```

\normalsize

### Dockerfile

This Dockerfile creates a virtual desktop environment, downloads the remote control driver and its dependencies and installs various python packages. At runtime it starts the virtual framebuffer and launches the evaluation script found under [@sec:browsercontrol].

\tiny

```Dockerfile
FROM alpine

RUN apk add --update --no-cache xvfb ffmpeg firefox-esr ttf-dejavu && rm -rf /var/cache/apk/*

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
	wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
	wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
	apk add glibc-2.30-r0.apk glibc-bin-2.30-r0.apk

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
	tar xzvf geckodriver*.tar.gz && \
	chmod +x geckodriver && \
	mv geckodriver /usr/local/bin

RUN apk add --update --no-cache linux-headers musl-dev gcc python3-dev python3 py3-pip py3-scipy py3-psutil py3-numpy
RUN pip3 install selenium requests

ENV DISPLAY=:42

RUN echo '(Xvfb $DISPLAY -ac -wr +render -noreset +extension GLX -screen 0 1920x1080x24 >/dev/null 2>&1 &) && sleep 2 && /evaluate.py' >/entrypoint.sh
COPY evaluate.py /
CMD /entrypoint.sh
```

\normalsize

### Measurement execution

The following two scripts have been employed to launch docker containers and capture the resulting data for regular measurements and the initial variation check. The first script accesses the codec list defined in [@sec:codec-list] as `codecs.json`.

\tiny

#### measure.py

```python
#!/usr/bin/env python3
import json
import os
import shutil
import subprocess

with open('codecs.json') as json_data:
    codecs = json.load(json_data)

tmp_path = "/tmp/encodings"
output_path = "out"

if not os.path.exists(output_path):
    os.makedirs(output_path)

for i, codec in enumerate(codecs):
    cmdline = codec['cmdline'] + " /out/video." + codec['container']
    compression = "C" if codec['compression'] else "L"
    parameters = compression + ", " + codec['container'] + ", " + codec['pixel_format']
    
    print(codec['name'] + "\t(" + parameters + ") [" + str(i + 1) + "/" + str(len(codecs)) + "]")
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    docker_cmd = [
        "docker", "run",
        "--rm", "-it",
        "--name", "encodings",
        "--shm-size", "2g",
        "--cpuset-cpus", "0",
        "-v", tmp_path + ":/out",
        "-e", "CODEC_CMDLINE=" + cmdline,
        "encodings"
    ]
    
    docker = subprocess.Popen(docker_cmd)
    docker.wait()

    shutil.move(tmp_path, output_path + "/" + codec['name'] + " " + parameters + "")
```

\normalsize

\tiny

#### measure_variation.py

```python
#!/usr/bin/env python3
import json
import os
import shutil
import subprocess

tmp_path = "/tmp/encodings"
out_path = "variations"
cmdline = "-c:v libx264rgb -preset ultrafast -crf 0 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30"
    + " -f mp4 -movflags +frag_keyframe+empty_moov+default_base_moof /out/video.mp4"

sample_sizes = [1, 2, 5, 10, 15, 20, 30]

if not os.path.exists(out_path):
    os.makedirs(out_path)

for sample_size in sample_sizes:
    print(sample_size)

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    docker_cmd = [
        "docker", "run",
        "--rm", "-it",
        "--name", "encodings",
        "--shm-size", "2g",
        "-v", tmp_path + ":/out",
        "-e", "CODEC_CMDLINE=" + cmdline,
        "-e", "SAMPLE_SIZE=" + str(sample_size),
        "encodings"
    ]

    docker = subprocess.Popen(docker_cmd)
    docker.wait()

    shutil.move(tmp_path + "/data.json", out_path + "/data" + str(sample_size) + ".json")
```

\normalsize

### Number processing

Below are the two scripts (and shared library) that process the collected data and return a CSV file with the results.

#### crunch_numbers.py

\tiny

```python
#!/usr/bin/env python3
import json
import os
import csv
import numpy as np

from shared import crunch_number

directory = os.fsencode("out")
folders = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == ".DS_Store":
        continue
    folders.append(filename)

folders.sort()

keys = ['wall', 'user', 'system', 'read', 'write', 'bitrate', 'avg_memory', 'max_memory']
rows = [['name'] + keys]
for codec in folders:
    data, samples = crunch_number("out/" + codec + "/data.json")
    fields = [codec]
    for key in keys:
        fields.append(round(data[key], 4))
    rows.append(fields)

with open('data/all.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
```

\normalsize

#### crunch_variation_numbers.py

\tiny

```python
#!/usr/bin/env python3
import json
import os
import csv
import numpy as np
import scipy.stats
from shared import crunch_number

# https://stackoverflow.com/a/15034143/6397601
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


directory = os.fsencode("variations")
files = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == ".DS_Store":
        continue
    files.append(filename)

files.sort()

keys = ['wall', 'user', 'system', 'read', 'write', 'bitrate', 'avg_memory', 'max_memory']
rows = [['name'] + keys + ['bitrate gamma', 'bitrate t_u', 'bitrate t_v', 'cpu gamma', 'cpu t_u', 'cpu t_v']]
for file in files:
    data, samples = crunch_number("variations/" + file)

    fields = [file]
    for key in keys:
        fields.append(round(data[key], 4))

    gamma, t_u, t_v = mean_confidence_interval(samples['bitrate'])
    fields += [round(gamma, 4), round(t_u, 4), round(t_v, 4)]

    cpu_samples = samples['duration']['user'] + samples['duration']['system']
    gamma, t_u, t_v = mean_confidence_interval(cpu_samples)
    fields += [round(gamma, 4), round(t_u, 4), round(t_v, 4)]

    rows.append(fields)

with open('data/variation.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
```

\normalsize

#### shared.py

\tiny

```python
#!/usr/bin/env python3
import json
import os
import csv
import numpy as np

def last_not_zero_value(lst):
    for value in reversed(lst):
        if value != 0.0:
            return value
    return 0.0

def crunch_number(file):
    with open(file, "r") as f:
        data = json.load(f)

    bitrates = []
    memory_usages = []
    duration = {
        "wall": [],
        "user": [],
        "system": []
    }
    io = {
        "read": [],
        "write": []
    }

    # Extract the values from the measurements
    for measurement in data['measurements']:
        bitrates.append(measurement['bitrate'])
        memory_usages.append(last_not_zero_value(measurement['memory']))
        
        for key in duration:
            duration[key].append(last_not_zero_value(measurement['times'][key]))

        for key in io:
            io[key].append(last_not_zero_value(measurement['io'][key]))

    # Calculate the averages for times and io
    output = {}
    for key in duration:
        output[key] = float(np.median(duration[key]))
    for key in io:
        output[key] = float(np.median(io[key]))

    # Accumulate individual values
    output['bitrate'] = float(np.median(bitrates))
    output['avg_memory'] = float(np.median(memory_usages))
    output['max_memory'] = float(np.max(memory_usages))

    samples = {}
    samples['bitrate'] = bitrates
    samples['memory'] = memory_usages
    samples['duration'] = duration
    samples['io'] = io

    return (output, samples)
```

\normalsize
