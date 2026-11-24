import subprocess
import json
import os

files = [
    r"C:\Users\c-deepak.sharma\Desktop\content\reference videos\1.mp4",
    r"C:\Users\c-deepak.sharma\Desktop\content\reference videos\2.mp4"
]

for f in files:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", f]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    info = json.loads(res.stdout)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    print("=" * 50)
    print("File:", os.path.basename(f))
    print("Duration:", info["format"].get("duration"), "s")
    print("Resolution:", f"{v.get('width')}x{v.get('height')}")
    print("FPS:", v.get("r_frame_rate"))
    print("Audio:", [s.get("codec_name") for s in a])
    print("Audio sample rate:", [s.get("sample_rate") for s in a])
