from pushbullet import Pushbullet
import glob
import os

import json
import youtube_dl

import click

@click.group()
def cli():
    """A tool to download, convert and send youtube music and videos using Pushbullet"""
    pass

@cli.command()
@click.option('--link', prompt='Video/Playlist link to download',
              help='Paste the link here to download and send to your device')
@click.option('--newdevice', help='Overwrite the saved device')
@click.option('--video', is_flag=bool, default=False,
              help='Send the video file instead of mp3 file.')
@click.option('--delete', is_flag=bool, default=False,
              help='Delete the music file after sending.')
def download(link, newdevice, video, delete):
    """Download the youtube song or video and send it to a device"""
    if os.path.exists('data.txt'):
        with open('data.txt') as json_file:
            data = json.load(json_file)
            for p in data['user']:
                api_key = p['api_key']
                device = p['device']
    else:
        click.secho(
            "Please run `moboff initialise` first.",
            fg='red',
            bold=True)
        quit()

    os.chdir('Music')

    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'forcefilename': 'True',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    if video is True:
        ydl_opts = {
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    list_of_mp3_files = glob.glob('*mp3')
    list_of_mp4_files = glob.glob('*mp4')
    recent_download = max(
        list_of_mp3_files +
        list_of_mp4_files,
        key=os.path.getctime)

    print("File to send : {0}".format(recent_download))

    pb = Pushbullet(api_key)
    phone = device

    if(newdevice):
        phone = newdevice

    with open(recent_download, "rb") as song:
        file_data = pb.upload_file(song, recent_download)

    print("Now sending the file to {0}".format(phone))
    #push = pb.push_file(**file_data)
    if(delete):
        os.remove(recent_download)


@cli.command()
def initialise():
    """Initialise the program with yout API key and preffered device."""
    click.secho(
        "Please enter your API Key, you can obtain it from here: https://www.pushbullet.com/#settings/account",
        bold=True)
    api_key = input()

    click.secho(
        "Enter the serial number for your preffered device to send your music files",
        bold=True)

    pb = Pushbullet(api_key)

    i = 0
    for device in pb.devices:
        print("{0} : {1}".format(i + 1, device))
        i += 1

    device_id = int(input()) - 1

    if not os.path.exists('Music'):
        os.makedirs('Music')
    click.secho(
        "The music would be downloaded to {0}/Music".format(os.getcwd()))

    data = {}
    data['user'] = []
    data['user'].append({
        'api_key': api_key,
        'device': str(pb.devices[device_id]),
    })
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    click.secho("Now you can run `moboff download` :) ", fg="green", bold=True)

if __name__ == '__main__':
    cli()