# Conclusion

Overall H.264 turns out to be the most time-efficient codec while still retaining a reasonable bitrate. Even though the codec is close to 17 years old it still provides one of the most mature, configurable and well-optimized encoders and has very good encoding and decoding support by both software and hardware alike. More modern codecs may have the potential to provide an even lower bitrate at comparable quality as the results showed for both VP9 and H.264. However, that comes with a significant cost in computing resources due to a lack of optimization^[this may change in the future] making potential bitrate savings of up to 50% [@netflix-video-quality-comparison] with more recent codecs unviable.

For screen recordings H.264's space efficiency remains sufficient at just over one Gigabyte per hour especially since most screen recordings will only be viewed over the local network. The pixel format conversion between the source and $YC_BC_R$ takes almost no additional resources when the video is being compressed and since the latter format is required by e.g. HLS doing the conversion in the initial encoding phase makes a secondary conversion step obsolete, effectively saving resources, cost, and reducing complexity.

Thanks to the standardization of a common media fragment format (namely CMAF) it is no longer necessary to decide between different streaming formats and one source file can be used without any format-specific transmuxing or transcoding. Additionally, both live and on-demand delivery is supported by all mentioned streaming formats which makes the delivery of screen recordings simple. It is even possible to generate HLS and MPEG-DASH manifests directly during the capture with the used encoding framework FFMPEG [@ffmpeg-segments] which further reduces the overall system complexity and simplifies the storage and delivery of screen recordings.

## Applicability {#sec:applicability}

Various factors may limit the applicability of the results obtained. They are tied to the specific environment they have been recorded in and different CPUs, operating systems and other variations may shift the absolute numbers due to higher or lower computing capability or hardware optimizations. For this reason only the relative difference between the numbers should be used directly and absolute numbers should be re-evaluated within the target environment.

In addition, various codecs may react differently to varying screen contents. This may change the results significantly depending on the screen contents as various compression algorithms operate differently and thus may use varying amounts of computing resources and yield differing compression ratios [@bitrate-content-association]. For this reason only applications where similar screen contents are used should incorporate the results directly into decisions. For other scenarios a re-evaluation may be necessary.

## Further research

This work specifically excluded hardware-accelerated encoding due to the limited availability and special hardware requirements. However, especially for very common codecs like H.264 and H.265, it has the potential to provide significant speed benefits while delivering higher quality [@nvenc] making it interesting for further research.

Additionally, a more complex two-stage compression method could be evaluated where the first stage makes use of a very fast codec that provides reasonable space efficiency but does not need to fit into the playback constraints set by e.g. HLS. A second stage would then compress the video even further and convert it to the target format on a different CPU to prevent interference with the test. This method could provide even greater bandwidth savings when storage space is limited.
