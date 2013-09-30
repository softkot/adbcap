adbcap
======

View and capture android screen via adb screencap function. Store the captured stream in advance, for futher video compilation.

It is written on PyGtk and utilize adb tool from Android SDK.

Basic usage
___________

> Usage: adbcap.py [options]
>
>Options:
>  -h, --help            show this help message and exit
>  -H HOST, --host=HOST  host to connect
>  -P PORT, --port=PORT  port to connect
>  -s DEVICE, --device=DEVICE
>                        specific device name
>  --width=WIDTH         window width
>  --height=HEIGHT       window height
>  --jpg-stream=STREAM   write a JPG stream to file for later ffmpeg/avconv processing


For example you can start 
> adbcap.py --jpg-stream=stream.jpgs

View and record the session and convert it into the regulat MP4 via ffmpeg/avconv tool

> avconv -y -f image2pipe -r 2 -vcodec mjpeg -i stream.jpgs -r 10 video.mp4

