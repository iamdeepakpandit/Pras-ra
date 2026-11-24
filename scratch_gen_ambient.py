import subprocess
import os

out_path = r"C:\Users\c-deepak.sharma\Desktop\content\assets\audio\humans_ambient.mp3"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

# Generate a 73-second dark ambient cinematic drone with sub-bass pulses and lowpass atmosphere using ffmpeg
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "sine=frequency=55:duration=73",       # Sub-bass root drone (A1)
    "-f", "lavfi", "-i", "sine=frequency=110:duration=73",      # Mid octave drone (A2)
    "-f", "lavfi", "-i", "sine=frequency=164.81:duration=73",   # Minor third / fifth harmonic (E3)
    "-f", "lavfi", "-i", "anoisesrc=d=73:c=pink:r=44100:a=0.04", # Tape / atmospheric cosmic noise
    "-filter_complex",
    "[0:a]volume=0.45[sub];"
    "[1:a]volume=0.25,lowpass=f=220,tremolo=f=0.15:d=0.4[mid];"
    "[2:a]volume=0.12,lowpass=f=300,tremolo=f=0.08:d=0.6[hi];"
    "[3:a]lowpass=f=450,volume=0.15,flanger=delay=10:depth=4:regen=20:width=80[noise];"
    "[sub][mid][hi][noise]amix=inputs=4:duration=first:dropout_transition=3[mixed];"
    "[mixed]afade=t=in:ss=0:d=2.5,afade=t=out:st=70:d=3[out]",
    "-map", "[out]",
    "-b:a", "192k",
    out_path
]

res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0:
    print(f"Generated cinematic ambient audio at {out_path}")
else:
    print(f"Error generating audio: {res.stderr}")
