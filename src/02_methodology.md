
# Methodology {#sec:methodology}

## Screen content

In order to evaluate the resource consumption of different codecs and parameters, a non-empty^[An empty screen would skew the results, since compression algorithms don't have to work as hard], reproducible and realistic screen content is required. Since most tests at PPI AG require a complex environment this research will make use of a tailored screen content which closely resembles a real world environment.

### Compression

Most codecs make use of compression algorithms to save bandwidth. These algorithms behave differently on static or very similar content than they do on very detailed, moving contents with the impact depending on the codec used. To rule out this interference which would not be present in a real world test scenario this research is going to use an automated browser instance that covers the whole screen.

### Browser

Since all browsers are expected to render web-pages the same way the results should be reproducible independently of the browser chosen. Thus the project will make use of the desktop browser with the highest market share as of March 2020, which according to the data in [@fig:browsers] is Google Chrome. It will be automated through the WebDriver REST protocol using a python client. The screen resolution will be set to `1920x1080` which is the most frequently used desktop resolution in Germany over the past 12 months as seen in [@fig:resolutions].

![Global browser marketshare [@browser-marketshare]](src/graphs/browser_marketshare.pdf){#fig:browsers}

![Screen resolutions in Germany [@screen-resolution-germany]](src/graphs/resolution_marketshare.pdf){#fig:resolutions}

### Web pages

During the recording the browser will be loading multiple web-pages and jump to different scroll positions to resemble a realistic test-workload. The pages contain a combination of static and dynamic content together with some animations. In order to automate this process the WebDriver protocol by the W3C will be used in conjunction with the Python Selenium client. A shortened version of the implementation used can be seen below.

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

## Measurement

In order to accurately capture the CPU load created by the encoding process its CPU time (split into user- and system-space) will be used as a measurement value. Additionally the wall time and disk I/O^[as reported by the linux kernel at `/proc/<pid>/io` in the virtual files `rchar` and `wchar`] will be captured. The codecs will be measured in sequence with a pause between them for the thermal system to recover.

<!---
% TODO Explain all of the above WAY more!
-->

### Recording framework

FFMpeg will be used as an encoding pipeline with the X11grab plugin to grab the screen contents. All resulting frames will be written to their recommended container format. Additionally the process will be restricted to a single processor core to recreate an environment with restricted resources.

### Specifications of the test device

All measurements will be recorded on a 2019 16-inch MacBook Pro with 16GB of RAM, 1TB SSD and the Intel Core i9-9880H CPU running macOS 10.15.4. All non-essential applications will be closed during the recordings to prevent any interference. Additionally the device will be attached to a power outlet and sufficient cooling will be provided to prevent excessive CPU throttling.

### Context & sampling {#sec:environment}

To recreate an environment that closely resembles a real-world scenario the recordings will be performed within Docker containers. This however may yield inconsistencies on macOS since Docker makes use of a virtual machine[@linuxkit]. To smooth out any influence this may have each codec will be evaluated multiple times and the median will be used as the final metric. In order to determine a reasonable sample size the test methodology will be executed multiple times with varying sample size and confidence interval calculated. From there a reasonable sample size for the environment will be chosen.

\pagebreak
