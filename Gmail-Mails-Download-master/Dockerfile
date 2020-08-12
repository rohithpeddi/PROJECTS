FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3-dev \
	openjdk-8-jdk \
	python-dev \
	wkhtmltopdf \
	xvfb \
	libfontconfig

WORKDIR /src

ADD ./scripts/ /src/

ADD ./startup_script.sh /src/

RUN mkdir emails_backup

WORKDIR emails_backup

CMD ../startup_script.sh
