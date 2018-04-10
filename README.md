## subtitleSync
use by running the python script with an .srt file and the first instance of dialogue for the video you're syncing
the .srt file to.
### for example:
###    python subtitleSync.py test.srt 00:00:05,340
here we create newSRT.srt that starts screening the subs in test.srt at 00:00:05,340 while keeping all the gaps
between dialogue constant. 
