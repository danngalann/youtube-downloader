# youtube-downloader
Python YouTube downloader. Suports 4k video and audio extraction.

Got tired of searching for online converters only to find them capped at 720p and riddled with ads, so I wrote my own.

This script will download a video at a given location. It defaults to the highest available resolution with a cap at 1080p to keep files small. This cap can be removed with the `--limitless` parameter.
You can also choose to download just the audio with the `-a` option. Full usage below.

## Usage
```
usage: download.py [-h] [-o OUTPUT] [-f FORMAT] [-a] [-q] url

A command line tool to download YouTube videos and songs

positional arguments:
  url                   Video URL

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory
  -f FORMAT, --format FORMAT
                        Video format
  -a, --audio           Download audio only
  -q, --limitless       Remove 1080p quality upper limit
```

## Requirements & Installation
For this script to work you'll need **pytube** and **ffmpeg**. The first one is provided by the requirements.txt, the second one you can get following [this guide](https://www.wikihow.com/Install-FFmpeg-on-Windows).
To install pytube run:
```
pip3 install -r requirements.txt
```
