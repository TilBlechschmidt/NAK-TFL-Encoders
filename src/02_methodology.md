
# Methodology {#sec:methodology}

In order to ensure the reproducibility and to extend the applicability of the result to the broadest possible set of scenarios, a clear methodology has to be defined. This includes criteria like the screen content, effects on compression, browser use, web pages, how measurements are taken and later evaluated. Many of these can be choosen arbitrarily and decisions have been made based on the environment this research originates from. Others are backed by public research and usage numbers.

## Screen content

To evaluate the resource consumption of different codecs and parameters, a non-empty^[An empty screen would skew the results since compression algorithms do not have to work as hard], reproducible, and realistic screen content is required. Since most tests at PPI AG require a complex environment, this research will make use of a tailored screen content that closely resembles a real-world testing environment.

#### Compression

Most codecs make use of compression algorithms to save bandwidth. These algorithms behave differently on static or very similar content than they do on very detailed, moving contents with the impact on CPU and bitrate depending on the codec used [@bitrate-content-association]. To rule out this interference which would not be present in a real-world test scenario this research is going to use an automated browser instance that covers the whole screen. This however will have some implications on the applicability of the results — more details can be found in [@sec:applicability].

#### Browser

All browsers are expected to render web-pages the same way and the results should be reproducible independently of the browser chosen. Thus, the project will make use of the desktop browser with the highest market share as of March 2020, which according to the data in [@fig:browsers] is Google Chrome. It will be automated by using the Python Selenium library^[Available at [https://github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium/tree/master/py)] which interacts with the browser through a REST API provided by the vendor^[More details available at [https://selenium.dev/](https://www.selenium.dev/documentation/en/)]. The screen resolution will be set to `1920x1080` which is the most frequently used desktop resolution in Germany over the past 12 months as seen in [@fig:resolutions].

#### Web pages

During the recording, the browser will be loading multiple web-pages and jump to different scroll positions to resemble a realistic test-workload. The pages contain a combination of static and dynamic content together with some animations. To automate this process the previously mentioned Selenium library will be used. The implementation can be found in [@sec:browsercontrol].

## Measurement

To accurately capture the CPU load created by the encoding process the CPU time will be used as a measurement value. It represents the amount of time a process is actively running instructions on the CPU. In comparison to the regular duration the process ran, it takes scheduling into account and prevents any interruptions of the process from affecting the final result. This value can be further divided into the time spent in the so-called user-space and system-space. The former includes all instructions and calculations the program did (e.g. compression) while the latter includes all instructions performed by the operating system on behalf of the process like for example disk read/write operations. The regular duration and file size of the resulting video will be recorded as well. The codecs will be measured one after another with a pause in between each evaluation. This pause is employed to prevent any influence that other mechanisms may have like swapping or thermal load.

#### Recording framework

A cross-platform program to record videos called FFMpeg will be used as an encoding tool with the X11grab plugin which records the screen contents on Linux by requesting the framebuffer contents from the window server. All resulting frames will be written to the codecs recommended container format. Alternatively, a low overhead container called NUT will be used if no recommended format is available. Additionally, the process will be restricted to a single processor core using Linux control groups to recreate an environment with restricted resources.

#### Specifications of the test device

All measurements will be recorded on a 2019 16-inch MacBook Pro with 16 GB of RAM, 1 TB SSD, and the Intel Core i9-9880H CPU running macOS 10.15.4. All non-essential applications will be closed during the recordings to prevent any interference. Additionally, the device will be attached to a power outlet and sufficient cooling will be provided to prevent excessive CPU throttling.

#### Context and sampling {#sec:environment}

To recreate an environment that closely resembles a real-world scenario the recordings will be performed within Docker containers described in detail in [@sec:docker]. This, however, may yield inconsistencies on macOS since Docker makes use of a virtual machine [@linuxkit]. To smooth out any influence this may have each codec will be evaluated multiple times and the median will be used as the final metric. To determine a reasonable sample size the test methodology will be executed multiple times with varying sample sizes and the resulting confidence interval calculated. From there a reasonable sample size will be chosen.

#### Docker environment {#sec:docker}

By default, most Docker containers are headless and do not contain a desktop environment required for both screen recording and browser automation. A full desktop environment comes with a lot of overhead in terms of window management, rendering, and additional services required. To reduce this overhead as much as possible, a virtual implementation of the X11 protocol will be used that provides a virtual, in-memory framebuffer which is not backed by any graphics devices (more specifically [Xvfb](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)). This choice could have positive effects on the CPU usage claimed by the importer, which reads frames from the framebuffer, and since the importer and exporter can not be measured independently it should give more accurate results.
