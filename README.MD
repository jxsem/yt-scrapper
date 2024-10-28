# yt-scrapper 
Main.py script obtains **videoId**, **titles** and **views** of a **Youtube channel** and put data into JSON.
video_requests.py script uses JSON data to use Youtube Transcript API to obtain every video transcripcion.

Finally, use that video transcripcion with prompts specified in prompts_examples.txt

☺ I appreciate if you put an star to the repository ☺

## Pre-requirements
- Python
- [Youtube Transcripcion API](https://pypi.org/project/youtube-transcript-api/)

## Execution
First you need a folder with the youtube channel. Inside the TXT where the HTML is.

Being in the same project path execute following in order to get data from YT channel.
```
python main.py [youtube_channel_name_folder]
```

And then this to transcript videos.
```
python video_requests.py [youtube_channel_name_folder]
```

## Contact 

[Linkedin](https://www.linkedin.com/in/lleirgarcia/)  
[Instagram](https://www.instagram.com/aqualityguy)  
[Youtube](https://www.youtube.com/channel/UCWrU0YCMKzn26kw970Clu3Q)  
[TikTok](https://www.tiktok.com/@aqualityguy)  
[The rest](https://linktr.ee/aqualityguy)  