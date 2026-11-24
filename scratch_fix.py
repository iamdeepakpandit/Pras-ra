import os, subprocess

# 1. Rename backup file
if os.path.exists("index_lyric_backup.html"):
    if os.path.exists("index_lyric_backup.html.bak"):
        os.remove("index_lyric_backup.html.bak")
    os.rename("index_lyric_backup.html", "index_lyric_backup.html.bak")
    print("Renamed index_lyric_backup.html to .bak")

# 2. Regenerate ambient audio to exactly 76s
out_path = r"C:\Users\c-deepak.sharma\Desktop\content\assets\audio\humans_ambient.mp3"
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "sine=frequency=55:duration=76",
    "-f", "lavfi", "-i", "sine=frequency=110:duration=76",
    "-f", "lavfi", "-i", "sine=frequency=164.81:duration=76",
    "-f", "lavfi", "-i", "anoisesrc=d=76:c=pink:r=44100:a=0.03",
    "-filter_complex",
    "[0:a]volume=0.4[sub];"
    "[1:a]volume=0.2,lowpass=f=220,tremolo=f=0.2:d=0.4[mid];"
    "[2:a]volume=0.12,lowpass=f=300,tremolo=f=0.15:d=0.5[hi];"
    "[3:a]lowpass=f=400,volume=0.12[noise];"
    "[sub][mid][hi][noise]amix=inputs=4:duration=first:dropout_transition=3[mixed];"
    "[mixed]afade=t=in:ss=0:d=2.5,afade=t=out:st=73:d=3[out]",
    "-map", "[out]",
    "-b:a", "192k",
    out_path
]
subprocess.run(cmd, check=True)
print("Regenerated ambient audio to 76s")

# 3. Update all human_sceneX.html files
for i in range(1, 9):
    fn = f"compositions/human_scene{i}.html"
    if os.path.exists(fn):
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("font-size:24px; font-weight:600;", "font-size:28px; font-weight:600;")
        content = content.replace('id="bg-img" class="clip full-frame"', 'id="bg-img" class="clip full-frame" data-layout-allow-overflow="true"')
        with open(fn, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {fn}")
