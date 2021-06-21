from pytube import YouTube
from pytube.cli import on_progress
import argparse
import subprocess
import os

DESCRIPTION = "A command line tool to download YouTube videos and songs"
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("url", help="Video URL")
parser.add_argument("-o", "--output", help="Output directory")
parser.add_argument("-f", "--format", help="Video format", default='mp4')
parser.add_argument("-a", "--audio", action="store_true",
                    help="Download audio only")
parser.add_argument("-q", "--limitless", action="store_true",
                    help="Remove 1080p quality upper limit")
args = parser.parse_args()

LIMIT = True
AUDIO_ONLY = False
URL = args.url
RESOLUTIONS = [
    '2160p',
    '1440p',
    '1080p',
    '720p',
    '360p'
]

if args.audio:
    AUDIO_ONLY = True

if args.limitless:
    LIMIT = False

video = YouTube(URL, on_progress_callback=on_progress)


def download(video, path):
    os.chdir(path)
    print(f"Downloading '{video.title}'")
    audioStream = getAudioStream(video)
    audioFileName = audioStream.default_filename

    if not AUDIO_ONLY:
        videoStream = getVideoStream(video)
        videoStream.download(path)
        videoFileName = videoStream.default_filename
        if not videoStream.includes_audio_track:
            print("\nDownloading audio...")
            os.rename(videoFileName, 'video_' + videoFileName)
            audioStream.download(path, filename_prefix='audio_')

            print("\nMerging audio...")
            mergeCommand = f'ffmpeg -i video_"{videoFileName}" -i "audio_{audioFileName}" -c:v copy -c:a aac "{videoFileName[:-5]}.{args.format}"'
            execute(mergeCommand)

            os.remove(f'video_{videoFileName}')
            os.remove(f'audio_{audioFileName}')
    else:
        audioStream.download(path)
        extractAudioCommand = f'ffmpeg -i "{audioFileName}" "{audioFileName[:-4]}".mp3'
        execute(extractAudioCommand)
        os.remove(audioFileName)


# Get highest available stream
def getVideoStream(video):
    videoStream = None
    streams = video.streams
    resolutions = RESOLUTIONS if not LIMIT else RESOLUTIONS[2:]

    for resolution in resolutions:
        videoStream = streams.filter(
            res=resolution, mime_type='video/webm').first()
        if videoStream is not None:
            break

    return videoStream


def getAudioStream(video):
    return video.streams.filter(only_audio=True, mime_type='audio/mp4').first()


def execute(command):
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )


download(video, args.output)
print('\nDONE.')
