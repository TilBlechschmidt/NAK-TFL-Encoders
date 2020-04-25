# Evaluation

<!-- Glossary for framebuffer -->

The following section contains the execution of the methodology described in [@sec:methodology]. Codecs have been choosen based on their maturity, spread however some promising young ones have been included as well.

## Codecs & Encoders

The first codec to include (which strictly speaking is not much of a codec) consist of a raw data dump directly from the framebuffer to establish a baseline to compare against.
The second codec, H.264, has been selected due to its wide support in both software and hardware in addition to the maturity and degree of optimization that available encoders have^[the x264 encoder implementation will be used]. Two versions of the encoder are available where one uses the $RGB$ pixel format (the framebuffers native format) and the other the $YC_BC_R$ format which is more common in video processing pipelines - both versions will be evaluated.

The successor of H.264, HEVC/H.265, will also be included since it promises better video quality at the same compression levels and similar to its predecessor both software and hardware implementations are around the corner for many platforms^[the x265 encoder implementation will be used].

Another very common codec and competitor to the two aforementioned ones is VP9 which is developed by Google Inc. [@vp9] and thus used by YouTube [@vp9-at-youtube] and other streaming platforms like Netflix [@vp9-at-netflix] which makes it an interesting contender^[the libvpx-vp9 encoder implementation will be used].

One codec which is heavily in use for proxy media^[intermediate video files used for faster editing in VFX workflows] and final video delivery^[e.g. on BluRays] called ProRes will be included as well as another broadcasting related codec developed by the BBC called VC2^[formerly called Dirac] which has the potential for efficient encoding of screen content due to its low overhead and low latency design [@vc2].

The following codecs, encoders and container formats will be used:

|                 Codec | &nbsp;&nbsp;&nbsp;Container | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Encoder |
|----------------------:|----------------------------:|--------------------------------------------:|
| &nbsp;&nbsp;&nbsp;Raw |                         nut |                                           - |
|                   VC2 |                         nut |                                   reference |
|                   VP9 |                        webm |                                  libvpx-vp9 |
|                 H.264 |                         mp4 |                                        x264 |
|                 H.264 |                         mp4 |                                     x264rgb |
|                 H.265 |                         mp4 |                                        x265 |
|                ProRes |                         mov |                                   prores_ks |

## Determining a sample size

Using the method described in [@sec:environment] measurements for different sample sizes have been made. The resulting confidence intervals can be seen in [@fig:bitrate_confidence] and [@fig:cputime_confidence]. They exhibit a large variation at sample sizes below 15 and only marginal improvement in interval size beyond 20. In order to achieve a reasonable trade-off between compute time and statistical relevance a sample size of 20 will be used for all further measurements.

![Bitrate confidence intervals](src/graphs/bitrate_confidence.pdf){#fig:bitrate_confidence}

![CPU time confidence intervals](src/graphs/cputime_confidence.pdf){#fig:cputime_confidence}

## Measurements

All measurements have been made over a period of just over 3,5 hours and the resulting data processed using a python script which can be found in the appendix. The resulting medians for bitrates, cpu times and disk I/O have been plotted using Numbers. The graphs will be analysed in the following subsections. X-Axis labels are formatted by the following syntax where `L` means lossless and `C` compressed:

```javascript
codec = "Raw" | "VC2" | "VP9" | "H.264" | "H.265" | "ProRes";
container = "mp4" | "mov" | "webm" | "nut";
compression = "L" | "C";
pixelFormat = "bgr0" | "rgb24" | "yuv420p" | "yuv422p10le";
label = codec, compression, ",", container, ",", pixelFormat;
```

<!-- TODO Append the python script -->

### Bitrate

![Measurement - Bitrate](src/graphs/bitrate.pdf){#fig:bitrate}

The data in [@fig:bitrate] shows the expected difference between compressed and uncompressed with ProRes and VC2 as outliers that are even higher than uncompressed versions of most other codecs. This could be attributed to their optimization for the video industry where file size is secondary and decode time matters far more [@prores].

H.265 exhibits a very low bitrate in comparison to H.264 and VP9 in both compressed and lossless mode however the resulting video files have a very low framerate that undercuts the target of 15 FPS by a large margin. This phenomenon has been analysed further and only exhibits itself when the encoder is restrained to a single core which might indicate a cpu bottleneck or very poor single-core optimization.

The difference between the two H.264 files is only marginal in compressed mode while the native pixel format yields about double the rate in lossless mode. The RAW dump on the other hand shows a bitrate that is significantly higher than all the other codecs at 21x the bitrate of VC2 making it unfeasible for any kind of short and long term storage^[Using a technology proposed in 2010 that enables 4.2 Gbps write speeds on SSDs [@ssd-speed] only 5 parallel recordings would be possible before completely saturating the write bandwidth].

### CPU

![Measurement - CPU time](src/graphs/cputime.pdf){#fig:cputime}

The graph for the CPU shows stacked bars where the blue portion represents the time spent by the process calculating in userspace^[e.g. compression of data] while the green portion exhibits the time spent in calls to the kernel^[e.g. `write(2)` or `read(2)`]. It is notable that while the RAW write takes second to no time in user-space it spends a significant amount of time in system-space which can be attributed to the high amount of write operations performed in comparison to other codecs with a lower bitrate.

\clearpage
