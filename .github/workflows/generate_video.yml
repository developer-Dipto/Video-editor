name: Generate Small Quote Video

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'

    - name: Install Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y ffmpeg
        pip install requests

    - name: Run Generator
      env:
        PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
      run: python main.py

    - name: Generate Online View Link
      run: |
        echo "--- Your Video Link Below ---"
        curl -F "file=@output.mp4" https://file.io
        echo -e "\n--- Copy the 'link' from above and open in browser ---"

    - name: Upload Artifact
      uses: actions/upload-artifact@v4
      with:
        name: small-video
        path: output.mp4
