# Download

Download videos from a list and extract subclips

list format (header): label,youtube_id,time_start,time_end,split

Kinetics: https://deepmind.com/research/open-source/open-source-datasets/kinetics/

remove_empty: remove files with 0 bytes

missing_download: list missing files 

Exec:
1) Download videos

python download.py <yt_id_list> <video_dir> <tmp_dir>

python download.py kinetics_train.csv videos/ tmp/

2) Remove empty files

python remove_empty.py <video_dir>

python remove_empty.py videos/

3) Remove videos that can't be opened

python pool_check.py <video_dir> --num_worker <n> --ext <ext>

python pool_check.py videos/ --num_worker 4 --ext mp4

4) List missing files

python missing_download.py <yt_id_list> <video_dir> <missing_list>

python missing_download.py kinetics_train.csv videos/ videos/missing.txt





