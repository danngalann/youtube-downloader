from pytube import YouTube
import argparse

DESCRIPTION = "A command line tool to download YouTube videos and songs"
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("url", help="Video URL")
parser.add_argument("-a", "--audio", action="store_true", help="Download audio only")
parser.add_argument("-q", "--limitless", action="store_true", help="Remove 1080p quality upper limit")
args = parser.parse_args()

LIMIT = True
AUDIO_ONLY = False
URL = args.url
RESOLUTIONS = [
    '1080p',
    '720p',
    '360p'
]

if args.audio:
    AUDIO_ONLY = True

if args.limitless:
    LIMIT = False

video = YouTube(URL)

def download(video, path):
    print(f"Downloading {video.title}")
    videoStream = getVideoStream(video)
    videoStream.download(path)

    if not videoStream.includes_audio_track:
        #TODO Download and merge audio
        pass

# Get highest available stream
def getVideoStream(video):
    videoStream = None
    streams = video.streams
    #TODO: Enable 4k download if LIMIT=False
    for resolution in RESOLUTIONS:
        videoStream = streams.filter(res=resolution, mime_type='video/mp4').first()
        if videoStream is not None:
            break

    return videoStream

download(video, r'c:\Users\danngalann\Desktop')