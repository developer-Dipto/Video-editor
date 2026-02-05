import requests
import os
import subprocess
import random

# API Keys from GitHub Secrets
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
QUOTES_API_URL = "https://zenquotes.io/api/random"

# নির্ভরযোগ্য রয়্যালটি ফ্রি মিউজিক লিস্ট (সরাসরি ডাউনলোড লিঙ্ক)
# আপনি চাইলে এখানে আপনার পছন্দের আরও লিঙ্ক যোগ করতে পারেন
AUDIO_LINKS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3"
]

def get_random_quote():
    try:
        response = requests.get(QUOTES_API_URL)
        if response.status_code == 200:
            data = response.json()
            return f"\"{data[0]['q']}\" \n- {data[0]['a']}"
    except Exception as e:
        print(f"Quote API Error: {e}")
    return "Keep pushing forward. \n- Unknown"

def get_random_video():
    try:
        query = random.choice(['nature', 'clouds', 'ocean', 'abstract'])
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            videos = response.json().get('videos', [])
            if videos:
                # সবচেয়ে ভালো মানের ছোট ভিডিওটি নেওয়া
                return random.choice(videos)['video_files'][0]['link']
    except Exception as e:
        print(f"Video API Error: {e}")
    return None

def download_file(url, filename):
    print(f"Downloading: {filename}...")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk: f.write(chunk)
        return True
    return False

def create_video(quote):
    # FFmpeg কমান্ড: ভিডিও + অডিও + টেক্সট বসানো
    # টেক্সট র‍্যাপিং এবং পজিশন ঠিক করা হয়েছে
    cmd = (
        f'ffmpeg -i input_video.mp4 -i input_audio.mp3 -vf '
        f'"drawtext=text=\'{quote}\':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2:'
        f'box=1:boxcolor=black@0.5:boxborderw=10" '
        f'-map 0:v:0 -map 1:a:0 -shortest -c:v libx264 -preset fast -pix_fmt yuv420p output.mp4 -y'
    )
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    print("Step 1: Fetching Quote...")
    quote = get_random_quote()
    
    print("Step 2: Fetching Video Link...")
    video_url = get_random_video()
    
    if video_url:
        # ভিডিও এবং একটি র‍্যান্ডম অডিও ডাউনলোড
        if download_file(video_url, "input_video.mp4") and download_file(random.choice(AUDIO_LINKS), "input_audio.mp3"):
            print("Step 3: Creating Final Video...")
            create_video(quote)
            print("Success! output.mp4 is ready.")
        else:
            print("Failed to download assets.")
    else:
        print("Could not get video from Pexels. Check your API Key.")
