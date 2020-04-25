---
    header-title: Transferleistung 2
    title: Effective video recording of browser based UI-Tests in software development

    author: Til Blechschmidt
    Zenturie: A17b
    Studiengang: Angewandte Informatik
    Matrikelnummer: 8240

    bibliography: src/bibliography.bib

    lang: en
    lof: true
---

# Introduction (bit short)

In the development of software applications it is common to do automated UI testing. For web-applications this is usually done by automating the browser with tools like Puppeteer [@pupeteer] or WebDrivers [@webdriver-standard]^[WebDrivers are a W3C standard for browser automation using a REST API with implementations from [all major browser vendors](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference)]. With projects growing larger the test durations are increasing, which in turn requires a testing solution that can scale horizontally, executing tests in parallel. Parallel testing however poses a problem in the traceability of errors since one tester is no longer capable of observing all test executions simultaneously. This raises the requirement for a review at a later time which is usually solved by doing a screen recording. Video recordings however are typically very resource intensive due to the amount of data that needs to be processed and compressed increasing the amount of hardware resources required significantly, effectively reducing the degree of parallelisation or increasing the budget requirements.

This work will focus on two aspects of the delivery of screen recordings from parallelised, automated Web-UI tests:

1. Which encoding codecs and parameters have a positive impact on the resource usage during screen capture?
2. How can screen recordings be efficiently delivered to the tester?

## Relevance for the PPI AG

<!---
% TODO: This section should be removed? At least not be a child of this thing. Maybe just a \paragraph{}
-->

Like many companies the PPI AG has multiple projects with web-based frontends that require testing. For most projects this process has already been automated but either parallelisation or visual feedback is still lacking. This work can aid the process of cost-effectively parallelising the current testing infrastructure while retaining the visual feedback test operators are used to.

\pagebreak
