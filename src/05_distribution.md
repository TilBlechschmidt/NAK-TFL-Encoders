# Distribution

After recording the screen with one of the previously evaluated codecs the files are likely stored in a Storage Area Network [@SAN] and have to be delivered to the person evaluating the test results for review. Multiple methods of delivery exist for protocols like HTTP, RTMP, or even analog broadcasting but since the environment is are already utilizing a web-based platform only protocols in that realm will be considered.

In the domain of plain HTTP, there are many ways of delivering video content and the most used ones according to a reasonably recent survey by bitmovin with 456 participants [@bitmovin-dev-report] will be further analyzed.

## HTTP Live Streaming

The most used streaming format is called HTTP Live Streaming or HLS for short. An initial draft was published by Apple in May 2009 and was changed several times throughout the following years until the RFC was officially approved by the Internet Engineering Task Force (IETF) in August 2017 and has been an official standard since [@rfc8216]. The protocol is natively supported by all devices running iOS 3.0 / Safari 4.0 or later [@apple-hls-support].

The format focuses on simple delivery using only a regular HTTP file server^[e.g. [nginx](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/)]. For this, a manifest file has to be generated which contains references to fragments^[either individual video files or byte offsets in a single fMP4 file] indexed by time offsets to allow fast random access. Supported encodings, however, are restricted to H.264 and H.265 by the standard even though other formats are likely to work if they support the MP4 or MPEG-TS container format.

One advantage of HLS is that it offers both Video on Demand (VOD) and Live delivery modes which allow for both a live view and later availability based on the same file and using the same streaming format with only minor changes to the manifest file.

## MPEG Dynamic adaptive streaming over HTTP

The second format is MPEG Dynamic adaptive streaming over HTTP or MPEG-DASH. The initial draft has been submitted to the ISO in January 2011 and was published in April 2012, following standardization in November 2011.

The format operates very similarly to HLS by segmenting the underlying media into segments of a fixed duration which are referenced by time offsets [@mpeg-dash]. Delivery is also very similar to the previous format as only a regular HTTP server is required once the media has been formatted correctly and manifests have been generated. Unlike HLS the specification is fully coding format-agnostic allowing any codec to be used as long as the receiving device can decode it.

Delivery modes are also very similar to HLS with live and on-demand modes available.

## MPEG Common Media Application Format

As previously mentioned both HLS and MPEG-DASH are using segmented base media formats indexed by time offsets. This similarity leads to further simplification by using a common media file for both streaming formats with the only difference being the format-specific segment index metadata. This usage of the segmented base media has been standardized by the ISO as the MPEG Common Media Application Format (CMAF) [@cmaf]. It further simplifies video delivery to the broadest possible audience since no transmuxing or even transcoding is required when using streaming formats that support CMAF and a wider range of clients can be served with less resource usage.

The [@fig:cmaf-timeline] shows the rough timeline of the CMAF development. Back in 2010 each streaming technology operated independently and required different versions of the same media files in addition to the metadata. In 2016 the underlying media format and segmentation have been standardized and other streaming formats could be derived from this. However, it was still necessary to define all metadata attributes which are not stored in the media tracks seperately. About a year later a common metadata format has been introduced as an extension to the standard which included those attributes. From this point on the manifests for each format can be derived from the shared manifest and only format specific properties need to be set manually to enable multi-format streaming. In theory most formats are still supporting other base media formats (e.g. MPEG-TS for HLS or M2TS for DASH) according to the specifications, however in practice this is rarely used.

![CMAF timeline [@cmaf-image-source]](src/graphs/cmaf-timeline.png){#fig:cmaf-timeline}
