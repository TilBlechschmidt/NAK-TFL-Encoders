---
    header-title: Transfer Paper 2
    title: Effective video recording of browser based UI-Tests in software development

    author: Til Blechschmidt
    Zenturie: A17b
    Studiengang: Angewandte Informatik
    Matrikelnummer: 8240

    natbib: true
    bibliography: src/bibliography.json

    lang: en
    lof: true

    fontsize: 12pt

    figPrefix:
      - "figure"
      - "figures"


    secPrefix:
      - "section"
      - "sections"
---

\setcounter{secnumdepth}{3}

# Introduction

In the development of software applications, it is common to do automated UI testing. For web-applications, this is usually done by automating the browser with tools like Puppeteer [@pupeteer] or WebDrivers [@webdriver-standard]. With projects growing larger the test durations are increasing, which in turn requires a testing solution that can scale horizontally. Parallel testing, however, poses a problem in the traceability of errors since one tester is no longer capable of observing all test executions simultaneously. This raises the requirement for a review at a later time which is usually solved by doing a screen recording. Video recordings, however, are typically very resource-intensive due to the amount of data that needs to be processed and compressed. This increases the number of hardware resources required significantly, effectively reducing the degree of parallelization or increasing the budget requirements. This leaves the question of which codecs are the fastest and most efficient in terms of CPU usage while still retaining an acceptable compression ratio to preserve network and disk bandwidth.

Given that question, this work will focus on two aspects of the delivery of screen recordings from parallelized, automated Web-UI tests:

1. Which video codecs have a positive impact on resource usage during screen capture?
2. How can screen recordings be efficiently delivered to the tester?

Like many companies, PPI AG has multiple projects with web-based frontends that require testing. For most projects, this process has already been automated but either parallelization or visual feedback is still lacking. This analysis can aid the process of cost-effectively parallelizing the current testing infrastructure while retaining the visual feedback test operators are used to.

To answer the initial question this document will be split into three parts. Firstly, the empirical method that will be used to compare different codecs will be outlined. The second part uses the described methods to measure and analyze the data. Finally, different technologies and streaming formats that can be used to deliver the screen recording will be compared by taking a look at their format specifications.

\pagebreak
