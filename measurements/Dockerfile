FROM alpine

RUN apk add --update --no-cache xvfb ffmpeg firefox-esr ttf-dejavu && rm -rf /var/cache/apk/*

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
	wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
	wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
	apk add glibc-2.30-r0.apk glibc-bin-2.30-r0.apk

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
	tar xzvf geckodriver*.tar.gz && \
	chmod +x geckodriver && \
	mv geckodriver /usr/local/bin

RUN apk add --update --no-cache linux-headers musl-dev gcc python3-dev python3 py3-pip py3-scipy py3-psutil py3-numpy
RUN pip3 install selenium requests

ENV DISPLAY=:42

COPY entrypoint.sh /
COPY evaluate.py /
CMD /entrypoint.sh
