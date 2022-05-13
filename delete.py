import os, time, shutil

def deletefile(folder, old_time_in_second):

	files = os.listdir(folder)

	if files == []:
		pass
	else:
		for file in files:
			now = time.time() - old_time_in_second
			f = os.path.join(folder, file)
			creation = os.stat(f).st_mtime
			if creation < now:
				shutil.rmtree(f)

# deletefile('./static/decoder/', 120)
