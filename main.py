import requests
import os
import subprocess
import random

# API Keys (GitHub Secrets থেকে আসবে)
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
QUOTES_API_URL = "https://zenquotes.io/api/random"

def get_random_quote():
    response = requests.get(QUOTES_API_URL)
    data = response.json()
    return f"\"{data[0]['q']}\" \n- {data[0]['a']}"

def get_random_video():
    query = random.choice(['nature', 'calm', 'space', 'sky'])
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=10"
    response = requests.get(url, headers=headers)
    videos = response.json().get('videos', [])
    return random.choice(videos)['video_files'][0]['link']

def get_random_audio():
    # Pixabay থেকে মিউজিক খোঁজা
    query = random.choice(['lofi', 'ambient', 'calm', 'peaceful'])
    url = f"https://pixabay.com/api/videos/audio/?key={PIXABAY_API_KEY}&q={query}"
    response = requests.get(url)
    audio_hits = response.json().get('hits', [])
    return random.choice(audio_hits)['downloads'][0]['link'] # সরাসরি অডিও লিঙ্ক

def download_file(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk: f.write(chunk)

def create_video(quote):
    # FFmpeg কমান্ড: ভিডিও + অডিও + টেক্সট
    # -shortest ফ্ল্যাগটি ব্যবহার করা হয়েছে যাতে ভিডিও বা অডিওর মধ্যে যেটি ছোট, সেখানেই ভিডিও শেষ হয়।
    cmd = (
        f'ffmpeg -i input_video.mp4 -i input_audio.mp3 -vf '
        f'"drawtext=text=\'{quote}\':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=(h-text_h)/2:'
        f'box=1:boxcolor=black@0.6:boxborderw=20" '
        f'-map 0:v:0 -map 1:a:0 -shortest -c:v libx264 -preset fast -pix_fmt yuv420p output.mp4 -y'
    )
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    print("Fetching data...")
    quote = get_random_quote()
    video_url = get_random_video()
    audio_url = get_random_audio()
    
    print("Downloading assets...")
    download_file(video_url, "input_video.mp4")
    download_file(audio_url, "input_audio.mp3")
    
    print("Merging everything into final video...")
    create_video(quote)
    print("Done! Check output.mp4")
