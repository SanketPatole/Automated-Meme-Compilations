import random
import subprocess
import sys
import urllib.request
import re
import pytube
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
from os.path import isfile, join
import shutil
from collections import defaultdict
import datetime
from googleapiclient.http import MediaFileUpload
import googleapiclient.errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import date


num_to_month = {
	1: "Jan",
	2: "Feb",
	3: "Mar",
	4: "Apr",
	5: "May",
	6: "June",
	7: "July",
	8: "Aug",
	9: "Sept",
	10: "Oct",
	11: "Nov",
	12: "Dec"
}

current_project_path = os.popen("pwd").read()[:-1]
videos_path = current_project_path + '/videos_sigma_rule_compilations/'
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=sigma+rule+memes&sp=CAMSBggDEAEYAw%253D%253D")
video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

INTRO_VID = 'funniest_meme_compilations_intro.mp4'	# SET AS '' IF YOU DON'T HAVE ONE
OUTRO_VID = 'funniest_meme_compilations_outro.mp4'
TOTAL_VID_LENGTH = 60*60
MAX_CLIP_LENGTH = 10*60
MIN_CLIP_LENGTH = 0
now_timestamp = datetime.datetime.now()
outputFile = "sigma_rule_compilations_" + num_to_month[now_timestamp.month].upper() + "_" + str(now_timestamp.year) + "_v" + str(
	now_timestamp.day) + ".mp4"

videonumber = date.today() - date(2021, 11, 8)
videonumber = videonumber.days
title = "MEME MARATHON | TRY NOT TO LAUGH | Best SIGMA Male Rule Compilations Volume #" + str(videonumber)
description = "MEME MARATHON | TRY NOT TO LAUGH | Best SIGMA Male Rule Compilations Volume #" + str(
	videonumber) + "\n\nEnjoy the memes! :)\n\nlike and subscribe to @Sigma Male Rule Meme Compilations for more Videos\n\nCopyright Disclaimer, Under Section 107 of the Copyright Act 1976, allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research. Fair use is a use permitted by copyright statute that might otherwise be infringing. Non-profit, educational or personal use tips the balance in favor of fair use.\n\nI as an individual creator do not earn any money from these compilation videos due to 6-7 copyright claims on all of the videos, and YouTube also does not monetize these compilation channels.\nIf you want me to keep making these amazing compilation videos, please become a Patron, support me and do not forget to subscribe to my channel.\nhttps://www.patreon.com/join/funniestmemecompilations\n\n\n\n#memes #dankmemes #compilation #funny #funnyvideos\n\n\n\nCredits (Please hit a like to the original videos and subscribe to their channels)\n\n"
tags = ['#memes', '#dankmemes', '#compilation', '#funny', '#funnyvideos', 'memes', 'dankmemes', 'compilation', 'funny',
		'funnyvideos', 'try not to laugh', 'dank memes', 'Sigma Rule', 'Sigma Rule 101', 'Sigma Rule Memes', 'Sigma Male']

counter = 0
for video_id in video_ids:
	try:
		video_url = "https://www.youtube.com/watch?v=" + video_id
		youtube = pytube.YouTube(video_url)
		video = youtube.streams.filter(progressive=True).get_highest_resolution()
		if youtube.title.lower().find("sigma") != -1 and youtube.title.lower().find("react") == -1 and youtube.title.lower().find("reacts") == -1 and youtube.title.lower().find("reaction") == -1 and youtube.description.lower().find("reacts") == -1 and youtube.description.lower().find("reaction") == -1 and youtube.title.lower().find("bollywood news mirchi") == -1 and youtube.description.lower().find("bollywood news mirchi") == -1:
			video.download(videos_path, str(counter) + ".mp4")
			counter += 1
			description = description + "Title: " + video.title + "\nLink: " + video_url + "\n\n"
			print(video.title)
	except:
		print("Video could not be downloaded.")

videos_list = os.listdir(videos_path)
random.shuffle(videos_list)
duration = 0

os.system("echo file \\'" + INTRO_VID + "\\'>inputs.txt")
os.system('ffmpeg -safe 0 -f concat -i inputs.txt -c copy -y ' + outputFile)

for fileName in videos_list:
	filePath = join(videos_path, fileName)
	print("File Path: " + filePath)
	if isfile(filePath) and fileName.endswith(".mp4"):
		print(fileName)
		if os.stat(filePath).st_size < 5000:
			print("File is too small")
			os.system("rm " + filePath)
			continue
		clip_size = float(os.popen("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + filePath).read()[:-2])
		tbn = 0
		try:
		    tbn = int(os.popen("ffprobe -show_streams " + filePath + ">temp 2>&1;cat temp|grep tbn|cut -d ' ' -f 26").read()[:-1])
		except:
		    print("Unable to pull tbn info")
		    os.system("rm " + filePath)
		    continue
		print("Clip size: " + str(clip_size))
		if int(clip_size) < MAX_CLIP_LENGTH:
			if tbn != 15360:
				os.system("ffmpeg -i " + filePath + " -video_track_timescale 15360 -y " + videos_path + "fixed_" + fileName)
				os.system("mv " + videos_path + "fixed_" + fileName + " " + filePath)
			os.system("ffmpeg -i " + filePath + " -ss 7 -vcodec copy -acodec copy trimmed.mp4 -y")
			os.system("mv trimmed.mp4 " + filePath)
			try:
				os.system("ffmpeg  -i " + filePath + " -t $(( $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + filePath + " |cut -d\. -f1) - 10 )) -c copy temp.mp4;mv temp.mp4 " + filePath)
			except:
				print("Could not remove trailer")
			os.system('cp ' + outputFile + ' tempfile.mp4')
			os.system("echo file \\'tempfile.mp4\\'>inputs.txt")
			os.system("echo file \\'" + filePath + "\\'>>inputs.txt")
			os.system('ffmpeg -safe 0 -f concat -i inputs.txt -c copy -y ' + outputFile)
			duration += float(clip_size)
		else:
			print("File Exceeds max size")
		os.system("rm " + filePath)
		if duration > TOTAL_VID_LENGTH:
			print("Total Length exceeded: " + str(duration))
			break
	elif isfile(filePath) and fileName.endswith(".mp4") == False:
		os.system("rm " + filePath)

os.system('cp ' + outputFile + ' tempfile.mp4')
os.system("echo file \\'tempfile.mp4\\'>inputs.txt")
os.system("echo file \\'" + OUTRO_VID + "\\'>>inputs.txt")
os.system('ffmpeg -safe 0 -f concat -i inputs.txt -c copy -y ' + outputFile)
os.system("rm tempfile.mp4")
os.system("rm inputs.txt")

TOKEN_NAME = "token.json"	# Don't change

# Setup Google
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "googleAPI.json"

def uploadYtvid(VIDEO_FILE_NAME='',
								title='Intro Video!',
								description=':) ',
								tags=[],
								googleAPI=None):
		now_timestamp = datetime.datetime.now()
		upload_date_time = datetime.datetime(now_timestamp.year, now_timestamp.month, now_timestamp.day, now_timestamp.hour,
																				 now_timestamp.minute,
																				 int(now_timestamp.second)).isoformat() + '.000Z'

		request_body = {
				'snippet': {
						'categoryId': 23,
						'title': title,
						'description': description,
						'tags': tags
				},
				'status': {
						'privacyStatus': 'public',
						'selfDeclaredMadeForKids': False,
				},
				'notifySubscribers': False
		}

		mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)

		response_upload = googleAPI.videos().insert(
				part='snippet,status',
				body=request_body,
				media_body=mediaFile
		).execute()

		googleAPI.thumbnails().set(
				videoId=response_upload.get('id'),
				media_body=MediaFileUpload(current_project_path + "/sigma_rule_compilations_thumbnails/thumbnail_" + str(random.randrange(1, 12)) + ".jpg")
		).execute()

# Handle GoogleAPI oauthStuff
print("Handling GoogleAPI")
creds = None
# The file token1.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(TOKEN_NAME):
		creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
		else:
				flow = InstalledAppFlow.from_client_secrets_file(
						client_secrets_file, SCOPES)
				creds = flow.run_console()
		# Save the credentials for the next run
		with open(TOKEN_NAME, 'w') as token:
				token.write(creds.to_json())

googleAPI = build('youtube', 'v3', credentials=creds)

#outputFile = "D:\\Stock Analysis\\automated_youtube_channel-master\\automated_youtube_channel-master\\" + outputFile

uploadYtvid(VIDEO_FILE_NAME=outputFile,
						title=title,
						description=description,
						tags=tags,
						googleAPI=googleAPI)
print("Uploaded To Youtube!")

os.remove(outputFile)
