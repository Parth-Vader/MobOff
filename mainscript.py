#!usr/bin.python

from pushbullet import Pushbullet
from sys import version_info
import pushbullet
import glob
import os
import subprocess
import json
import click

real_path_of_MobOff = os.path.dirname(os.path.realpath(__file__))

@click.group()
def cli():
    """A command line tool to download, convert
    and send youtube videos or playlists to
    your device via Pushbullet.

    You need to install Pushbullet in all your devices
    for this to work.

    If this is your first time using this,
    please run `moboff initialise` to add required
    information.

    Run `moboff download --help` to know about
    various options while downloading and sending.
    """
    pass


@cli.command('download', short_help='Downloads and sends the video')
@click.option('--link', prompt='Video/Playlist link to download',
              help='Paste the link here to download and send to your device')
@click.option('--newdevice', help='Overwrite the saved device')
@click.option('--video', is_flag=bool, default=False,
              help='Send the video file instead of mp3 file.')
@click.option('--delete', is_flag=bool, default=False,
              help='Delete the music file after sending.')
def download(link, newdevice, video, delete):
    """Download a youtube video or playlist
    in best audio and video quality
    by providing a link, and then send to the
    preferred device, or override it with `--newdevice`
    option.

    Provide the device name for `--newdevice` in quotes for e.g. "OnePlus One".

    Please run `moboff initialise` if this is your first time.
    """
    os.chdir(real_path_of_MobOff)

    if os.path.exists('moboff_cfg.json'):
        with open('moboff_cfg.json') as json_file:
            data = json.load(json_file)
            api_key = data['user']['api_key']
            device = data['user']['device']
    else:
        click.secho(
            "Please run `moboff initialise` first.",
            fg='red',
            bold=True)
        quit()

    os.chdir('Music')

    if video is True:
        downloadcommand = ["youtube-dl",
                           "--metadata-from-title",
                           "%(artist)s - %(title)s",
                           "-f",
                           "bestvideo+bestaudio",
                           "--add-metadata",
                           "--output",
                           "%(artist)s - %(title)s.%(ext)s",
                           link]
    else:
        downloadcommand = ["youtube-dl",
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
                           link]

    try:
        subprocess.check_output(downloadcommand, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Please check your URL, it shouldn't be a private playlist link (eg liked videos)")
        quit()

    click.secho("File successfully downloaded.", fg="green", bold=True)
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

    if newdevice:
        newdevice = "Device('{0}')".format(newdevice)
        click.secho("Overriding preferred device : {0} with given device : {1}").format(
            device, newdevice)
        phone = newdevice

    with open(recent_download, "rb") as song:
        file_data = pb.upload_file(song, recent_download)

    print("Now sending the file to {0}".format(phone))
    pb.push_file(**file_data)

    if(delete):
        os.remove(recent_download)


@cli.command('initialise', short_help='Initialise with info')
def initialise():
    """Initialise the program with yout API key and preferred device."""
    if version_info[0] == 2:
        rawinput = raw_input
    else:
        rawinput = input

    click.secho(
        "Please enter your API Key, you can obtain it from here: https://www.pushbullet.com/#settings/account",
        bold=True)
    api_key = rawinput()

    try:
        pb = Pushbullet(api_key)
    except pushbullet.errors.InvalidKeyError:
        click.secho(
            "Please check your API key again. Run this command again and try.")
        quit()

    click.secho(
        "Enter the serial number (eg 1 or 2) for your preferred device to send your music files",
        bold=True)

    for i, device in enumerate(pb.devices, 1):
        print("{0} : {1}".format(i, device))
   
    device_id = int(rawinput()) - 1

    os.chdir(real_path_of_MobOff)
    if not os.path.exists('Music'):
        os.makedirs('Music')
    click.secho(
        "The music would be downloaded to {0}/Music".format(os.getcwd()))

        

    data = {
         'user': {
                 'api_key': api_key,
                 'device': str(pb.devices[device_id]),
         }
     }
    with open('moboff_cfg.json', 'w') as outfile:
        json.dump(data, outfile)

    click.secho("Now you can run `moboff download` :) ", fg="green", bold=True)


if __name__ == '__main__':
    cli()
