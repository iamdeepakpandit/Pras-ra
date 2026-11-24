import os
import shutil
import subprocess

# 1. Copy images
src_dir = r"C:\Users\c-deepak.sharma\.gemini\antigravity\brain\c61433fe-40d7-4c66-8cad-c5180a4d0dbf"
dst_dir = r"C:\Users\c-deepak.sharma\Desktop\content\assets\images\time"
os.makedirs(dst_dir, exist_ok=True)

img_map = {
    "gravity_defying_hourglass_1795407180862.jpg": "scene1_hourglass_up.jpg",
    "neo_noir_silhouette_rain_window_clean_1795407200633.jpg": "scene2_silhouette_rain.jpg",
    "checklist_alert_split_screen_1795407175720.jpg": "scene3_split_screen.jpg",
    "emerald_hourglass_neonoir_1795407185443.jpg": "scene4_hourglass_tilt.jpg",
    "neo_noir_hourglass_1795407185115.jpg": "scene5_final_grain.jpg"
}

for src_name, dst_name in img_map.items():
    sp = os.path.join(src_dir, src_name)
    dp = os.path.join(dst_dir, dst_name)
    shutil.copy2(sp, dp)
    print(f"Copied {dst_name}")

# 2. Synthesize multi-layered sound design (42s)
# Layer 0: Dark synth pulse (48Hz sine with tremolo + 96Hz)
# Layer 1: Rain ambience enabled between 6s and 15s (Scene 2)
# Layer 2: Sub-bass drop at 26s (Scene 4 Freeze)
# Layer 3: Transition whooshes at 6s, 15s, 26s, 35s
out_audio = r"C:\Users\c-deepak.sharma\Desktop\content\assets\audio\time_soundtrack.mp3"
os.makedirs(os.path.dirname(out_audio), exist_ok=True)

cmd = [
    "ffmpeg", "-y",
    # 0: Sub drone pulse
    "-f", "lavfi", "-i", "sine=frequency=48:duration=42",
    "-f", "lavfi", "-i", "sine=frequency=96:duration=42",
    # 2: Ambient noise/pulse
    "-f", "lavfi", "-i", "anoisesrc=d=42:c=pink:r=44100:a=0.02",
    # 3: Rain sound effect for Scene 2 (9s duration)
    "-f", "lavfi", "-i", "anoisesrc=d=9:c=brown:r=44100:a=0.06",
    # 4: Sub-bass drop for Scene 4 (freeze at 26s, 5s duration)
    "-f", "lavfi", "-i", "sine=frequency=38:duration=6",
    "-filter_complex",
    "[0:a]volume=0.35,lowpass=f=120,tremolo=f=0.5:d=0.3[sub];"
    "[1:a]volume=0.18,lowpass=f=200,tremolo=f=0.25:d=0.4[mid];"
    "[2:a]volume=0.10,lowpass=f=350[noise];"
    # Delay rain to start at 6.0s (Scene 2)
    "[3:a]lowpass=f=1200,highpass=f=200,afade=t=in:ss=0:d=1,afade=t=out:st=8:d=1,adelay=6000|6000,volume=0.25[rain];"
    # Delay sub-bass drop to 26.0s (Scene 4 Freeze)
    "[4:a]volume=0.6,lowpass=f=90,afade=t=in:ss=0:d=0.2,afade=t=out:st=1:d=4.5,adelay=26000|26000[drop];"
    "[sub][mid][noise][rain][drop]amix=inputs=5:duration=first:dropout_transition=2[mixed];"
    "[mixed]volume=0.7[out]",
    "-map", "[out]",
    "-b:a", "192k",
    out_audio
]
subprocess.run(cmd, check=True)
print("Generated sound design track successfully at", out_audio)
