import requests
import os
import subprocess
import random
import sys

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

QUOTES = [
    "Believe in yourself and all that you are.",
    "The best way to predict the future is to create it.",
    "Your time is limited, dont waste it.",
    "Success is not final, failure is not fatal.",
    "Stay hungry, stay foolish."
]

AUDIO_LINKS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
]

def get_random_video():
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/videos/search?query=nature&per_page=5"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        return r.json()['videos'][0]['video_files'][0]['link']
    except: return None

def download(url, name):
    print(f"Downloading {name}...")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(name, 'wb') as f:
            for chunk in r.iter_content(1024*1024): f.write(chunk)
        return True
    return False

def create_video(quote):
    print(f"Processing Video...")
    # Ubuntu-তে DejaVuSans ফন্ট ডিফল্ট থাকে, তাই এর পুরো পাথ দিচ্ছি
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    # scale=1280:-2 নিশ্চিত করে যে উচ্চতা সবসময় জোড় সংখ্যা হবে
    cmd = [
        'ffmpeg', '-i', 'input_video.mp4', '-i', 'input_audio.mp3',
        '-t', '10', 
        '-vf', f"scale=1280:-2,drawtext=fontfile='{font_path}':text='{quote}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=20",
        '-map', '0:v:0', '-map', '1:a:0', '-shortest', 
        '-c:v', 'libx264', '-crf', '28', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', 'output.mp4', '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error Log:\n{result.stderr}")

if __name__ == "__main__":
    q = random.choice(QUOTES)
    v_url = get_random_video()
    
    if v_url and download(v_url, "input_video.mp4") and download(AUDIO_LINKS[0], "input_audio.mp3"):
        create_video(q)
        if os.path.exists("output.mp4") and os.path.getsize("output.mp4") > 1000:
            print("Video Created Successfully!")
        else:
            print("Error: Video file is empty or too small.")
            sys.exit(1)
