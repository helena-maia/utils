'''
16/March/2019

Download videos from a list and extract subclips

list format (header): label,youtube_id,time_start,time_end,split
'''

import youtube_dl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import argparse
import os

class Download():
    # out_tmpl:	output format with subclip path, without extension ex: "dir/%s"
    # tmp_dir: 	directory to temporarily save full videos
    # ext: 	video extension
    def __init__(self, out_tmpl, tmp_dir, ext = ".mp4"):
        self.ext=ext
        self.out_tmpl=out_tmpl
        self.tmp=tmp_dir
       
        ydl_opts = {
            "outtmpl": os.path.join(self.tmp,"%(id)s"+ext), #<tmp_dir>/yt_id.<ext>
            "quiet": False,
            "no_warnings": True,
        }
        self.ydl = youtube_dl.YoutubeDL(ydl_opts)
       
    # yt_id:			youtube id
    # start_time, end_time:     in seconds, for subclips extraction
    # out_tmpl_data:		values to fill out_tmpl and get the path to the computed subclip
    def download(self,yt_id, start_time, end_time, out_tmpl_data):
        url = 'https://www.youtube.com/watch?v='+yt_id
        ret = 1
        try: 
            self.ydl.download([url])
            ffmpeg_extract_subclip(os.path.join(self.tmp,yt_id+self.ext), start_time, end_time, targetname=self.out_tmpl%out_tmpl_data+self.ext)
        except OSError:
            try:
                ffmpeg_extract_subclip(os.path.join(self.tmp,yt_id+self.ext), start_time, end_time, targetname=self.out_tmpl%out_tmpl_data+".webm")
            except Exception as ex:
                template = "2:An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
                ret = 0 #failure
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            ret = 0 #failure

        return ret

def getArgs():
    parser = argparse.ArgumentParser(description='Download dataset.')
    parser.add_argument("yt_id_list", action='store', type=str, help="path to the list of youtube ids")
    parser.add_argument("video_dir", action='store', type=str, help="directory to save the subclips")
    parser.add_argument("tmp_dir", action='store', type=str, help="directory to temporarily save full videos")
    return parser.parse_args()


if __name__ == "__main__":
    args = getArgs()

    if not os.path.isdir(args.video_dir):
        print("creating folder: "+args.video_dir)
        os.makedirs(args.video_dir)

    if not os.path.isdir(args.tmp_dir):
        print("creating folder: "+args.tmp_dir)
        os.makedirs(args.tmp_dir)

    out_fmt = os.path.join(args.video_dir,"%s_%s_%s") #(train_or_test, class, youtube_id)
    d = Download(out_fmt, args.tmp_dir)

    yt_list = np.loadtxt(args.yt_id_list, delimiter=',',dtype=str)[1:] #ignore header
    total = yt_list.shape[0]

    for ind,v in zip(range(1,total+1),yt_list):
        print ("%d of %d"%(ind, total))
        label, yt_id, start_time, end_time, split = v
        ret = d.download(yt_id, int(start_time), int(end_time), (split,label,yt_id))

        

