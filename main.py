import requests
import os
import subprocess
import random
import sys

# API Key for Pexels
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# predefined quotes এর লিস্ট
QUOTES = [
    "Believe in yourself and all that you are.",
    "The best way to predict the future is to create it.",
    "Success is not final, failure is not fatal.",
    "Your time is limited, dont waste it.",
    "Hardships often prepare people for an extraordinary destiny.",
    "Stay hungry, stay foolish.",
    "Do what you can, with what you have, where you are.",
    "Everything you ever wanted is on the other side of fear.",
    "Dream big and dare to fail.",
    "Act as if what you do makes a difference. It does."
]

# রিলায়েবল অডিও লিঙ্ক
AUDIO_LINKS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
]

def get_random_video():
    if not PEXELS_API_KEY:
        print("Error: PEXELS_API_KEY is missing in Secrets!")
        return None
    
    headers = {"Authorization": PEXELS_API_KEY}
    # র‍্যান্ডম ক্যাটাগরি সার্চ
    query = random.choice(['nature', 'ocean', 'forest', 'calm'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        videos = response.json().get('videos', [])
        if videos:
            # প্রথম ভিডিওটির ডাউনলোড লিঙ্ক
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
    except:
        pass
    return False

def create_video(quote):
    print(f"Generating Video with Quote: {quote}")
    
    # FFmpeg কমান্ড: ড্র-টেক্সট দিয়ে ভিডিও এবং অডিও মার্জ করা
    # টেক্সটটি ভিডিওর একদম মাঝখানে থাকবে
    cmd = [
        'ffmpeg', '-i', 'input_video.mp4', '-i', 'input_audio.mp3',
        '-vf', f"drawtext=text='{quote}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=10",
        '-map', '0:v:0', '-map', '1:a:0', '-shortest', 
        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', 'output.mp4', '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg Error: {result.stderr}")

if __name__ == "__main__":
    # ১. র‍্যান্ডম কোট এবং ভিডিও লিঙ্ক নেওয়া
    selected_quote = random.choice(QUOTES)
    video_url = get_random_video()
    
    if not video_url:
        print("Failed to get video. Script stopping.")
        sys.exit(1)

    # ২. অ্যাসেটস ডাউনলোড করা
    if download_file(video_url, "input_video.mp4") and download_file(random.choice(AUDIO_LINKS), "input_audio.mp3"):
        # ৩. ভিডিও তৈরি করা
        create_video(selected_quote)
        
        # ৪. আউটপুট চেক করা
        if os.path.exists("output.mp4"):
            print("Done! output.mp4 created successfully.")
        else:
            print("Error: output.mp4 was not generated.")
            sys.exit(1)
    else:
        print("Download failed.")
        sys.exit(1)
