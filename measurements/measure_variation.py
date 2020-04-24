#!/usr/bin/env python3
import json
import os
import shutil
import subprocess

tmp_path = "/tmp/encodings"
out_path = "variations"
cmdline = "-c:v libx264rgb -preset ultrafast -crf 0 -tune stillimage -x264-params keyint=30:scenecut=0:keyint_min=30 -f mp4 -movflags +frag_keyframe+empty_moov+default_base_moof /out/video.mp4"

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
