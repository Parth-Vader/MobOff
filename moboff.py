#!usr/bin.python

import glob
import os
import subprocess
import json
from sys import version_info

from pushbullet import Pushbullet
import pushbullet
import click

from download_utils import select_directory

real_path_of_MobOff = os.path.dirname(os.path.realpath(__file__))

if version_info[0] == 2:
    rawinput = raw_input
else:
    rawinput = input


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
@click.option('--send', is_flag=bool, default=False,
              help='Send the file to a friend.')

def download(link, newdevice, video, delete,send):
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
            directory = data['user']['directory']
    else:
        click.secho(
            "Please run `moboff initialise` first.",
            fg='red',
            bold=True)
        quit()

    try:
        pb = Pushbullet(api_key)
    except pushbullet.errors.InvalidKeyError:
        click.secho("API key you previously entered is no longer valid. Please rerun moboff initialise.")
        quit()

    phone = device

    if newdevice:
        click.secho("Overriding preferred device : {0} with given device : {1}".format(
            device, newdevice))
        phone = newdevice

    try:
        to_device = pb.get_device(phone)
    except pushbullet.errors.PushbulletError:
        if newdevice:
            click.secho("{0} isn't setup with Pushbullet. "
                        "Please either set it up or check the spelling of entered device".format(newdevice))
        else:
            click.secho("The default device you entered initially doesn't exist anymore. "
                        "Please rerun moboff initialise.")
        quit()

    try:
        os.chdir(directory)
    except OSError:
        click.secho("The directory previously selected to download music can't be accessed."
                    " Please rerun moboff initialise.")
        quit()
    
    os.mkdir("{0}/temp".format(directory))
    os.chdir("{0}/temp".format(directory))
    
    print("This may take a while.")
    
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

    for file in list_of_files: 
        print("File to send : {0}".format(file))
        with open(file, "rb") as song:
            file_data = pb.upload_file(song, file)
        to_device.push_file(**file_data)
        print("The file has been sent to your {0}.".format(to_device))

    if send:
        for i, device in enumerate(pb.chats, 1):
            print("{0} : {1}".format(i, device))
        index=int(rawinput("Enter the corresponding chat no. for the person you want to send the file to. "))
        try:
            chat=pb.chats[index-1]
            for file in list_of_files: 
                print("File to send : {0}".format(file))
                with open(file, "rb") as song:
                    file_data = pb.upload_file(song, file)
                pb.push_file(**file_data, chat=chat)
        except:
            print("Contact does not exist.")
        else:
            print("The file has been sent to ", chat)
  
    for file in list_of_files:
        if file.endswith((".mp3", "mp4", ".mkv")):
            os.rename("{0}/temp/{1}".format(directory, file),"{0}/{1}".format(directory, file))
            
    os.rmdir("{0}/temp".format(directory))   
    os.chdir(directory)

    if delete:
        for file in list_of_files:
            os.remove(file)


@cli.command('initialise', short_help='Initialise with info')
def initialise():
    """Initialise the program with your API key and preferred device."""

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
        print("{0} : {1}".format(i, device.nickname))

    device_id = int(rawinput()) - 1

    if not 0 <= device_id <= len(pb.devices):
        click.secho("Choose from available device.")
        quit()

    click.secho("Please Select a directory for store the Downloads", bold=True)
    directory = select_directory()

    click.secho("The music would be downloaded to {0}".format(directory))

    data = {
        'user': {
            'api_key': api_key,
            'device': pb.devices[device_id].nickname,
            'directory': directory,
        }
    }
    with open(os.path.join(real_path_of_MobOff , 'moboff_cfg.json'), 'w') as outfile:
        json.dump(data, outfile)

    click.secho("Now you can run `moboff download` :) ", fg="green", bold=True)


if __name__ == '__main__':
    cli()
