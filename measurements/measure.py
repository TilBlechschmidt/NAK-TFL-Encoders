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

for codec in codecs:
    cmdline = codec['cmdline'] + " /out/video." + codec['container']
    compression = "C" if codec['compression'] else "L"
    parameters = compression + ", " + codec['container'] + ", " + codec['pixel_format']
    
    print(codec['name'] + "\t(" + parameters + ")")
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    docker_cmd = [
        "docker", "run",
        "--rm", "-it",
        "--name", "encodings",
        "--shm-size", "2g",
        "-v", tmp_path + ":/out",
        "-e", "CODEC_CMDLINE=" + cmdline,
        "encodings"
    ]
    
    docker = subprocess.Popen(docker_cmd)
    docker.wait()

    shutil.move(tmp_path, output_path + "/" + codec['name'] + " " + parameters + "")
