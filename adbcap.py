#!/usr/bin/python
import pygtk
import gtk
import gobject
import os
import threading
import subprocess
from optparse import OptionParser

class Adb_Capture(object):

	def delete_event(self, widget, event, data=None):
		return False

	def destroy(self, widget, data=None):
		self.quit=True
		gtk.main_quit()

	def __init__(self):
		parser = OptionParser("usage: %prog [options]")
		parser.add_option("-H", "--host", dest="host", 
					help="host to connect")
		parser.add_option("-P", "--port", dest="port", 
					help="port to connect")
		parser.add_option("-s", "--device", dest="device",
					help="specific device name")

		parser.add_option("", "--width", dest="width", default=320,
					help="window width")

		parser.add_option("", "--height", dest="height", default=470,
					help="window height")

		parser.add_option("", "--jpg-stream", dest="stream",
					help="write a JPG stream to file for later ffmpeg/avconv processing. "\
		"For example: avconv -y -f image2pipe -r 2 -vcodec mjpeg -i stream.jpgs -r 10 video.mp4")

		(options, args) = parser.parse_args()
		self.params=["adb"]
		if (options.host):
			self.params+=["-H",options.host]
		if (options.port):
			self.params+=["-P",options.port]
		if (options.device):
			self.params+=["-s",options.device]

		self.stream=None

		if (options.stream):
			self.stream=options.stream

		self.params+=["shell",'screencap -p']
		self.temp_height = 0
		self.temp_width = 0
		self.pixbuf=None
		self.quit=False
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)


		self.image = gtk.Image()
		self.image.set_from_file("")
		self.image.show()
		self.image.connect('expose-event', self.on_image_resize, self.window)

		box = gtk.ScrolledWindow()
		box.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		box.add(self.image)
		self.window.resize(options.width,options.height)
		self.window.add(box)
		self.window.show_all()

	def main(self):
		gtk.gdk.threads_init()
		loader = AdbCaptureThread(self)
		loader.daemon=True
		loader.start()

		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()

	def on_image_resize(self, widget, event, window):
		if self.pixbuf is None:
			return
		allocation = widget.get_allocation()
		if self.temp_height != allocation.height or self.temp_width != allocation.width:
			self.temp_height = allocation.height
			self.temp_width = allocation.width
			pixbuf = self.pixbuf.scale_simple(allocation.width, allocation.height, gtk.gdk.INTERP_BILINEAR)
			widget.set_from_pixbuf(pixbuf)

class AdbCaptureThread(threading.Thread):
	def __init__(self, app):
		super(AdbCaptureThread, self).__init__()
		self.app = app

	def update_image(self,pixbuf):
		self.app.pixbuf=pixbuf
		self.app.temp_height=0
		self.app.on_image_resize(self.app.image,None,self.app.window)
		return False

	def grab_frame(self):
		self.subproc = subprocess.Popen(self.app.params,stdout=subprocess.PIPE)

	def save_stream(self,buffer,data=None):
		data.write(buffer)

	def run(self):
		self.grab_frame()
		outstream=None
		if (self.app.stream):
			try:
				outstream=open(self.app.stream, 'w')
			except:
				pass
		while not self.app.quit:
			proc=self.subproc
			self.grab_frame()
			content=proc.stdout.read()
			if self.app.quit:
				break
			pixbuf=None
			try:
				loader = gtk.gdk.PixbufLoader("png")
				loader.write(content.replace("\r\n","\n"))
				loader.close()
				pixbuf=loader.get_pixbuf()
				gobject.idle_add(self.update_image, pixbuf)
				if (outstream and pixbuf):
					pixbuf.save_to_callback(self.save_stream, "jpeg", {"quality":"100"},outstream)
					outstream.flush()
			except:
				pass
		if (outstream):
			outstream.close()

if __name__ == '__main__':
	Adb_Capture().main()
