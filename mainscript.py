from pushbullet import Pushbullet
import glob
import os
import subprocess
import json

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

    if video is True:
        subprocess.call(["youtube-dl",
                         "--metadata-from-title",
                         "%(artist)s - %(title)s",
                         "-f",
                         "bestvideo+bestaudio",
                         "--add-metadata",
                         "--output",
                         "%(artist)s - %(title)s.%(ext)s",
                         link])
    else:
        subprocess.call(["youtube-dl",
                         "--metadata-from-title",
                         "%(artist)s - %(title)s",
                         "--extract-audio",
                         "--audio-format",
                         "mp3",
                         "--audio-quality",
                         "0",
                         "--add-metadata",
                         "--output",
                         "%(artist)s - %(title)s.%(ext)s",
                         link])
    
    types = ('*.mp3', '*.mp4', '*.mkv')
    list_of_files = []
    for files in types:
        list_of_files.extend(glob.glob(files))

    recent_download = max(
        list_of_files,
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
        "Enter the serial number (eg 1 or 2) for your preffered device to send your music files",
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
