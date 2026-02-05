import requests
import os
import subprocess
import random
import sys

# API Key for Pexels
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# predefined quotes
QUOTES = [
    "Believe in yourself and all that you are.",
    "The best way to predict the future is to create it.",
    "Success is not final, failure is not fatal.",
    "Your time is limited, dont waste it.",
    "Stay hungry, stay foolish.",
    "Dream big and dare to fail.",
    "Act as if what you do makes a difference."
]

# রিলায়েবল অডিও লিঙ্ক
AUDIO_LINKS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
]

def get_random_video():
    if not PEXELS_API_KEY:
        print("Error: PEXELS_API_KEY is missing!")
        return None
    
    headers = {"Authorization": PEXELS_API_KEY}
    query = random.choice(['nature', 'ocean', 'forest', 'mountains'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        videos = response.json().get('videos', [])
        if videos:
            # ছোট সাইজের ভিডিও লিঙ্ক (SD বা HD) নেওয়ার চেষ্টা করা
            return videos[0]['video_files'][0]['link']
    except Exception as e:
        print(f"Video API Error: {e}")
    return None

def download_file(url, filename):
    print(f"Downloading {filename}...")
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            return True
    except: return False
    return False

def create_video(quote):
    print(f"Generating Compressed Video...")
    
    # FFmpeg Optimization:
    # 1. scale=1280:-1 (HD 720p তে রিসাইজ করা)
    # 2. -t 10 (ভিডিওটি ১০ সেকেন্ডে কেটে ছোট করা)
    # 3. -crf 28 (ফাইলের সাইজ অনেক কমানো)
    # 4. -preset faster (দ্রুত রেন্ডার করা)
    
    cmd = [
        'ffmpeg', '-i', 'input_video.mp4', '-i', 'input_audio.mp3',
        '-t', '10', 
        '-vf', f"scale=1280:-1,drawtext=text='{quote}':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=15",
        '-map', '0:v:0', '-map', '1:a:0', '-shortest', 
        '-c:v', 'libx264', '-crf', '28', '-preset', 'faster', '-pix_fmt', 'yuv420p', 'output.mp4', '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error: {result.stderr}")

if __name__ == "__main__":
    selected_quote = random.choice(QUOTES)
    video_url = get_random_video()
    
    if video_url and download_file(video_url, "input_video.mp4") and download_file(random.choice(AUDIO_LINKS), "input_audio.mp3"):
        create_video(selected_quote)
        
        if os.path.exists("output.mp4"):
            print("Successfully created compressed output.mp4")
        else:
            sys.exit(1)
    else:
        print("Download failed.")
        sys.exit(1)
