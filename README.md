# Meme-Compilations


## Introduction

This repository contains the codebase, which I used to generate meme compilation videos.
The videos are 1 hour long in length and are set up for automated upload to YouTube with all the required metadata.
The entire code is purely written in Python.

The utility checks all the relevent and funny short videos uploaded recently to YouTube.
It then trims intro and outro from these videos and stitches them together.
Later, intro and outro is added to the final combined video and is uploaded to YouTube.
The videos are uploaded with, title, description, SEO tags and thumbnails.


## Prerequisites

### Python requirements

* You need to install Python with version 3.0 or more. You can find the latest version of Python at https://www.python.org/downloads/

* You need to have following Python libraries to be installed.
```sh
pip install pytube
pip install moviepy
pip install shutil
pip install googleapiclient
pip install google_auth_oauthlib
pip install google
```

### YouTube API account

* To automate video uploads to YouTube, you need to have YouTube API account setup beforehand. Please refer following webpage for more details.
  https://developers.google.com/youtube/v3/getting-started

* Once the api account is set up, you need to audit your application with YouTube. If your application is not audited by YouTube, you won't be able to make your videos public. Please refer following webpage for more details.
  https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits

* Once audit is completed, copy client_id and client_secrets for your YouTube API account and paste it into googleAPI.json file. Please refer following webpage for more details.
  https://developers.google.com/youtube/registering_an_application


## How to run the code

* You need to clone the repository to your local system. Open command line/terminal or git bash and run following command.
```sh
git clone https://github.com/SanketPatole/Meme-Compilations.git
```

* Open command line/terminal and go inside any video folder you want to generate video for. For example: "Funniest_Meme_Compilations"
```sh
cd "Funniest_Meme_Compilations"
```

* If token.json file is not present on the current path or existing token in token.json is expired, run following command to regenerate token.json file.
```sh
python "token_generator.py"
```

* Once the token is generated, run following command to generated compilation video and upload it automatically to YouTube.
```sh
python "video_generator.py"
```


## License Information

Please refer "LICENSE" file to know the license details.
Before reusing this code, you will need to take a written permission from me.
You can contact me at sanketpatole1994@outlook.com

