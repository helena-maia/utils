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
import glob

class Download():
    # out_tmpl:	output format with subclip path, without extension ex: "dir/%s"
    # tmp_dir: 	directory to temporarily save full videos
    # ext: 	video extension
    def __init__(self, out_tmpl, tmp_dir):
        self.out_tmpl=out_tmpl
        self.tmp=tmp_dir
        self.conv_cmd = "ffmpeg -y -i '%s' -strict experimental -c:a aac '%s'"
       
        ydl_opts = {
            "outtmpl": os.path.join(self.tmp,"%(id)s"), #<tmp_dir>/yt_id, ydl automatically adds the extension
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
            self.ydl.download([url]) #download

            occur = glob.glob(os.path.join(self.tmp, yt_id)+"*") #check video occurences in tmp
            if (len(occur) != 1): raise Exception('None or multiple video occurrences: %d'%(len(occur))) 

            occur = occur[0]
            ext = "."+occur.split(".")[-1]   
            ffmpeg_extract_subclip(occur, start_time, end_time, targetname=self.out_tmpl%out_tmpl_data+ext) #extract subclip

            #subclip conversion to mp4
            if (ext == ".webm" or ext == ".mkv"):
                path_src = self.out_tmpl%out_tmpl_data+ext
                path_dest = self.out_tmpl%out_tmpl_data+".mp4"
                os.system(self.conv_cmd%(path_src, path_dest))
                os.remove(path_src)

            os.remove(occur) #remove video from tmp

        except Exception as ex:
            template = "Item: ({},{},{},{}). An exception of type {} occurred. Arguments:\n{!r}"
            message = template.format(yt_id, str(start_time), str(end_time), self.out_tmpl%out_tmpl_data, type(ex).__name__, ex.args)
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

    out_fmt = os.path.join(args.video_dir,"%s_%s_%s_%04d") #(train_or_test, class, youtube_id, start_time)
    d = Download(out_fmt, args.tmp_dir)

    yt_list = np.loadtxt(args.yt_id_list, delimiter=',',dtype='U100')[1:] #ignore header
    total = yt_list.shape[0]

    for ind,v in zip(range(1,total+1),yt_list):
        print ("%d of %d"%(ind, total))
        label, yt_id, start_time, end_time, split = v
        label = label.replace(" ","-")
        ret = d.download(yt_id, int(start_time), int(end_time), (split,label,yt_id, int(start_time)))

        

