# Evaluation

<!-- Glossary for framebuffer -->

The following section contains the execution of the methodology described in [@sec:methodology]. Codecs have been chosen based on their maturity and software support however some emerging ones have been included as well.

## Codecs and Encoders

The first codec to include consist of a raw data dump directly from the framebuffer to establish a baseline to compare against^[Called rawvideo in the case of FFmpeg].
The second codec, H.264, has been selected due to its wide support in both software and hardware in addition to the maturity and degree of optimization that available encoders have^[the x264 encoder implementation will be used]. Two versions of the encoder are available where one uses the $RGB$ pixel format (the framebuffers native format) and the other the $YC_BC_R$ format which is more common in video processing pipelines - both versions will be evaluated.

The successor of H.264, HEVC/H.265, will also be included since it promises better video quality [@netflix-video-quality-comparison] at the same compression levels and similar to its predecessor both software and hardware implementations are around the corner for many platforms^[the x265 encoder implementation will be used].

Another very common codec [@bitmovin-dev-report] and a competitor to the two aforementioned ones is VP9 which is developed by Google Inc. [@vp9] and used by YouTube [@vp9-at-youtube] and other streaming platforms like Netflix [@vp9-at-netflix] which makes it a mentionable contender^[the libvpx-vp9 encoder implementation will be used].

One codec which is heavily in use for proxy media^[intermediate video files used for faster editing in VFX workflows] and final video delivery^[e.g. on BluRays] called ProRes will be included for its optimizations regarding the use as intermediate media [@prores] as well as another broadcasting related codec developed by the BBC called VC2^[formerly called Dirac] which has the potential for efficient encoding of screen content due to its low overhead and low latency design [@vc2].

A recent innovation in the media industry is the AV1 codec which promises even higher compression ratios than VP9 or H.265 at a comparable visual quality [@av1-promises]. However, running a test using the publicly available and self-proclaimed "fastest" encoder available called [rav1e](https://github.com/xiph/rav1e) yielded very poor performance even across 16 threads taking more than three seconds per frame at full CPU utilization^[Note that this situation may change very fast due to the ongoing development of encoders [@mhv2019]]. That makes the codec unviable for application in a test-recording environment where resources are at a premium and thus it will be excluded from the test.

The following codecs, encoders and container formats will be used:

<!-- Maybe add sources for mov, mp4 and webm containers -->

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

Using the method described in [@sec:environment] measurements for different sample sizes have been made. The resulting confidence intervals can be seen in [@fig:confidence_intervals] (with t_u being the lower bound, t_v the upper bound, and gamma representing the median of the measured values). They exhibit a large variation at sample sizes below 15 and only marginal improvement in interval size beyond 20. To achieve a reasonable trade-off between computing time and statistical relevance a sample size of 20 will be used for all further measurements.

\begin{figure}
\centering
\subfigure[Bitrate]{\includegraphics[width=0.5\textwidth,height=6cm]{src/graphs/bitrate_confidence.pdf}}
\subfigure[CPU time]{\includegraphics[width=0.5\textwidth,height=6cm]{src/graphs/cputime_confidence.pdf}}
\caption{Confidence intervals}
\label{fig:confidence_intervals}
\end{figure}

## Measurements

All measurements have been made over a period of just over 3,5 hours and the resulting data processed using a python script which can be found in the accompanying [GitHub repository](https://github.com/TilBlechschmidt/TFL-Encoders). The resulting medians for bitrates, CPU times and disk I/O have been plotted. The graphs will be analyzed in the following subsections. X-Axis labels contain the codec, compression (L = Lossless, C = Compressed), the container format, and finally the pixel format.

\clearpage

### Bitrate

\begin{wrapfigure}{r}{0.5\textwidth}
  \begin{center}
    \includegraphics[width=0.48\textwidth]{src/graphs/bitrate.pdf}
  \end{center}
  \caption{Measurement - Bitrate}
  \label{fig:bitrate}
\end{wrapfigure}

The data in [@fig:bitrate] shows the expected difference between compressed and lossless with ProRes and VC2 as outliers that are even higher than lossless versions of most other codecs. This could be attributed to their optimization for the video industry where file size is secondary and decode time matters far more [@prores].

H.265 exhibits a very low bitrate in comparison to H.264 and VP9 in both compressed and lossless mode. However, the resulting video files have a very low framerate that undercuts the target of 15 FPS by a large margin. This phenomenon has been analyzed further and only exhibits itself when the encoder is restrained to a single core which might indicate a CPU bottleneck or very poor single-core optimization.

The difference between the two H.264 files is only marginal in compressed mode while the native pixel format yields about double the rate in lossless mode. The raw dump, on the other hand, shows a bitrate that is significantly higher than all the other codecs at 21 times the bitrate of VC2 making it unfeasible for any kind of short and long term storage^[Using a technology proposed in 2010 that enables 4.2 Gigabit/s write speeds on SSDs [@ssd-speed] only five parallel recordings would be possible before completely saturating the write bandwidth].

\clearpage

### CPU

\begin{wrapfigure}{r}{0.5\textwidth}
  \begin{center}
    \includegraphics[width=0.48\textwidth]{src/graphs/cputime.pdf}
  \end{center}
  \caption{Measurement - CPU time}
  \label{fig:cputime}
\end{wrapfigure}

The graph for the CPU in [@fig:cputime] shows stacked bars where the blue portion represents the time spent by the process calculating in userspace^[e.g. compression of data] while the green portion exhibits the time spent in kernel calls^[e.g. `write(2)` or `read(2)`]. It is notable that while the raw write takes almost no time in user-space, it spends a significant amount of time in system-space which can be attributed to the high amount of write operations performed in comparison to other codecs with a significantly lower bitrate making it almost as slow as lossless H.264 ($RGB$).

Also notable is the difference between lossless and compressed codecs with H.264 ($RGB$) and H.265 behaving as expected with lossless taking less time while others like H.264 ($YC_BC_R$) and VP9 are contrary to that with compressed being faster. This behavior could simply be attributed to measurement inaccuracy or minor differences in screen content due to page load times.

Another feature of the data is the minimal difference between the two versions of the H.264 encoder with the two compressed configurations using the same amount of CPU (within the margin of error). Differences emerge when using the lossless option where the source pixel format is using slightly fewer resources.

It should also be noted that while the aforementioned issues with H.265 are represented in the bitrate graph by a very low bitrate they are not visible from the CPU usage. The current testing environment restrains all codecs to a single CPU core, however, by removing these constraints and instead of asking the codecs to use just a single core a similar result can be achieved except for H.265 which uses almost 70 seconds of CPU time. This confirms the previously mentioned bottleneck and explains the very low bitrate and framerate under regular test conditions.

<!-- TODO Make cpu uniformly capitalized and use gls -->

\clearpage
