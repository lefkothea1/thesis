from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

dir1 = 'G:\\PP5\\recordings_pp5\\'
os.chdir(dir1)

vid_name = '766128782097970_2.mkv'

name = 'pp05_stress'
#sec. NEUTRAL:
# starttime = 1679 ; endtime = starttime + (30*60)
#STRESS
endtime = 6757 ; starttime = endtime- (30*60)

ffmpeg_extract_subclip(vid_name, starttime, endtime, targetname= name +".mkv")
# with open("times.txt") as f:
#   times = f.readlines()
# times = [x.strip() for x in times] 
# for time in times:
#   starttime = int(time.split("-")[0])
#   endtime = int(time.split("-")[1])
#   ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=str(times.index(time)+1)+".mp4")