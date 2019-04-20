from multiprocessing import Pool
import cv2
import numpy as np
import os
import argparse
import glob
import time

def run_open(x):
    ind = x[0]
    video_path = x[1]

    print(ind)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        os.remove(video_path)



def getArgs():
    parser = argparse.ArgumentParser(description='Compute visual rhythm (mean).')
    parser.add_argument("video_dir", action='store', type=str, help="directory that contains the subclips")
    parser.add_argument('--num_worker', type=int, default=8, help='')
    parser.add_argument('--ext', type=str, default='avi', choices=['avi','mp4'], help='video file extensions')
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()

    num_worker=args.num_worker
    videos = glob.glob(os.path.join(args.video_dir,"*."+args.ext))

    pool = Pool(num_worker)
    pool.map(run_open,enumerate(videos))
