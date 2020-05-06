\pagebreak
\appendix
\section*{Appendices}
\pagenumbering{roman}
\addcontentsline{toc}{section}{Appendices}
\renewcommand{\thesubsection}{\Alph{subsection}}

## Figures

![Global browser marketshare (March 2019) [@browser-marketshare]](src/graphs/browser_marketshare.pdf){#fig:browsers}

![Screen resolutions in Germany (March 2019) [@screen-resolution-germany]](src/graphs/resolution_marketshare.pdf){#fig:resolutions}

## Codec parameters

The following list has been used to execute the test runs and each cmdline was combined with the common prefix `ffmpeg -y -rtbufsize 1500M -probesize 100M -framerate 15 -video_size 1920x1080 -f x11grab -i :42 -t 00:01:00 -threads 1`. To keep the document size within reasonable limits the python scripts have been omitted. They can be found in the public GitHub repository at [https://github.com/TilBlechschmidt/TFL-Encoders](https://github.com/TilBlechschmidt/TFL-Encoders).

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

## Browser control code {#sec:browsercontrol}

```python
sites = [
    # Static content
    "http://www.python.org",

    # Stress the codec with particle animations
    "https://vincentgarreau.com/particles.js/#nasa",
    "https://codepen.io/themegatb/full/VwvaNpv",
    "https://vincentgarreau.com/particles.js/#nyancat2",

    # Some UI animations
    "https://www.highcharts.com/demo",
    "https://www.highcharts.com/demo/column-stacked",
    "https://www.highcharts.com/demo/column-parsed"
]

# Iterate over all the pages
for site in sites:
    driver.get(site)
    sleep(3)

# Finish off with some scrolling on a heavily
#   scroll-animated and "contentful" web-page
#   (scrolling 20px per animation frame)
driver.get("https://www.apple.com/de/macbook-pro-16/")
scroll(20)
```

## Literature
