# MobOff

> A command line tool to add your music and videos directly to several devices.

## Why?

Almost all of us use youtube for our music purposes, whether it is a new single released by Eminem or an old classic by Queen. 

Scenario : You need to travel the next day and you realise that the `diff` between your offline mobile playlist and youtube playlist is too large.

Now you have to use an online mp3 converter to convert all the songs one by one, and then connect your device via USB to paste all the music. That too without the metadata.

There is a need for a tool which would directly download and convert the video, add available metadata and send it to your device, all at the same time.

### Enters *MobOff*.

## Features

* Download the best available audio, or video (by `--video` option) in common mobile player compatible extensions.
* Playlists can also be downloaded.
* Adds metadata automatically from the title.
* Add a preffered device to send music, or override it with `--newdevice` option.
* Delete the downloaded video/music file from the computer via `--delete` option.

## How to use?

(Tested on Ubuntu with Python 3)

>The initial setting up of the Pushbullet account seems a little tiring but it is just a one-time setup, and the gains are endless.

1. You need a [Pushbullet](https://www.pushbullet.com/) account to send the files. 

Pushbullet is a great tool for sending text messages, links, files and seeing phone's notifications on your computer.

  * Create yout account on it using your Google or Facebook login.
  * Install the Pushbullet App on your iOS or Android device.
  * Install the Chrome/Firefox extension for Pushbullet on your computer.

2. After setting Pushbullet up, you need to install MobOff.

It is recommended that you use `virtualenv` (especially for `conda` users).

  * Installing `virtualenv` : ` sudo pip install virtualenv`
  * `virtualenv venv --python=python3`
  * `. venv/bin/activate`
  * `pip3 install moboff`

### You can also install it system-wide by `pip3 install MobOff` 

3. You need to initialise with some of your information.
  
  * Run `moboff initialise`
  * Obtain your Pushbullet API key via [Pushbullet Settings](https://www.pushbullet.com/#settings/account) by clicking on "Create Access Token" button.
  * Enter the serial number for your preffered device to send the music/video files to when asked to.
  
### You're all set up.

## Usage

### `moboff --help`
    Usage: moboff [OPTIONS] COMMAND [ARGS]...

      A command line tool to download, convert and send youtube videos or
      playlists to your device via Pushbullet.

      You need to install Pushbullet in all your devices for this to work.

      If this is your first time using this, please run `moboff initialise` to
      add required information.

      Run `moboff download --help` to know about various options while
      downloading and sending.

    Options:
      --help  Show this message and exit.

    Commands:
      download    Downloads and sends the video
      initialise  Initialise with info

### `moboff download --help`
    Usage: moboff download [OPTIONS]

      Download a youtube video or playlist in best audio and video quality by
      providing a link, and then send to the preffered device, or override it
      with `--newdevice` option.

      Provide the device name for `--newdevice` in quotes for e.g. "OnePlus
      One".

      Please run `moboff initialise` if this is your first time.

    Options:
      --link TEXT       Paste the link here to download and send to your device
      --newdevice TEXT  Overwrite the saved device
      --video           Send the video file instead of mp3 file.
      --delete          Delete the music file after sending.
      --help            Show this message and exit.

## Contribute

This is a very young project. If you have got any suggestions for new features or improvements, please comment over here. Pull Requests are most welcome !

❤

Please star if you liked it :)
