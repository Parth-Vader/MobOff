FROM ubuntu

# set up timezone
RUN echo "America/New_York" > /etc/timezone

# install required packages
RUN apt-get update \
&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    ffmpeg python3-tk \
    git-core \
&& rm -rf /var/lib/apt/lists/*

# setup locales and language to utf-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# clone moboff repository
RUN git clone https://github.com/Parth-Vader/MobOff.git

# install setuptools
RUN pip3 install setuptools

# change working directory to MobOff
WORKDIR /MobOff

# run the installation script
RUN python3 setup.py install

# run bash
CMD ["/bin/bash"]
