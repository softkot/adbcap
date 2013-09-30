adbcap
======

View and capture android screen via adb screencap function. Store the captured stream in advance, for futher video compilation.

It is written on PyGtk and utilize adb tool from [Android SDK](http://developer.android.com/sdk/index.html).

Due to android platform to support adb screencap method, it works with most android 4.x devices connected with adb in developer mode.

Basic usage
-----------

```
Usage: adbcap.py [options]

Options:
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  host to connect
  -P PORT, --port=PORT  port to connect
  -s DEVICE, --device=DEVICE
                        specific device name
  --width=WIDTH         window width
  --height=HEIGHT       window height
  --jpg-stream=STREAM   write a JPG stream to file for later ffmpeg/avconv processing
```

For example you can start the tool to view and record the session 
```
adbcap.py --jpg-stream=stream.jpgs
```

And convert it right after into the regular MP4 via [ffmpeg](http://www.ffmpeg.org/) or [libav](http://libav.org/) tools.

```
avconv -y -f image2pipe -r 2 -vcodec mjpeg -i stream.jpgs -r 10 video.mp4
```

