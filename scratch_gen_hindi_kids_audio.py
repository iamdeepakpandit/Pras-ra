import asyncio, edge_tts, subprocess, os, numpy as np, wave

VOICE = 'hi-IN-MadhurNeural'
OUTPUT_DIR = 'assets/voice_hindi_kids'
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def fix_s4():
    comm = edge_tts.Communicate('लेकिन आरव रुका नहीं... और संदूक का ताला धीरे से खुल गया!', VOICE, rate='+22%')
    await comm.save(os.path.join(OUTPUT_DIR, 'scene4.mp3'))

asyncio.run(fix_s4())

# Check all clips
for i in range(1, 6):
    p = os.path.join(OUTPUT_DIR, f'scene{i}.mp3')
    res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', p], capture_output=True, text=True)
    print(f'scene{i}.mp3: {float(res.stdout.strip()):.2f}s')

# Synthesize fairy-tale suspense ambient bed (30.00s)
sr = 44100
dur = 30.0
total_samples = int(dur * sr)
t = np.linspace(0, dur, total_samples, endpoint=False)

# 1. Mystical forest drone (65 Hz + 130 Hz gentle cello hum)
drone = 0.14 * np.sin(2 * np.pi * 65 * t) + 0.07 * np.sin(2 * np.pi * 130 * t)
drone *= (1.0 + 0.1 * np.sin(2 * np.pi * 0.3 * t))

# 2. Suspense heartbeat pulse accelerating slightly (from 0s to 24s)
heartbeat = np.zeros(total_samples)
beat_times = [0.8, 2.0, 3.2, 4.4, 5.6, 7.0, 8.2, 9.4, 10.6, 11.8, 13.0, 14.2, 15.4, 16.6, 17.8, 19.0, 20.0, 21.0, 22.0, 22.8, 23.5]
for bt in beat_times:
    b_idx = int(bt * sr)
    decay = int(0.35 * sr)
    end = min(total_samples, b_idx + decay)
    actual = end - b_idx
    if actual > 0:
        tb = np.linspace(0, 0.35, decay)[:actual]
        pulse = 0.28 * np.sin(2 * np.pi * 48 * tb) * np.exp(-tb * 8.0)
        heartbeat[b_idx:end] += pulse

# 3. Magical bell chime sparkle at 24s (The Happy Reveal!)
chime = np.zeros(total_samples)
rev_idx = int(24.0 * sr)
rev_dur = int(5.5 * sr)
rev_end = min(total_samples, rev_idx + rev_dur)
actual_rev = rev_end - rev_idx
if actual_rev > 0:
    tr = np.linspace(0, 5.5, rev_dur)[:actual_rev]
    # Major chord sparkle (C6, E6, G6, C7 frequencies: 1046, 1318, 1568, 2093 Hz)
    bell = (0.12 * np.sin(2 * np.pi * 1046 * tr) +
            0.10 * np.sin(2 * np.pi * 1318 * tr) +
            0.10 * np.sin(2 * np.pi * 1568 * tr) +
            0.08 * np.sin(2 * np.pi * 2093 * tr)) * np.exp(-tr * 0.8)
    chime[rev_idx:rev_end] += bell

# 4. Subtle forest night breeze whisper
noise = np.random.normal(0, 0.02, total_samples)

bed = drone + heartbeat + chime + noise
bed = bed / (np.max(np.abs(bed)) + 1e-6) * 0.42

wav_path = 'assets/audio/kids_suspense_bed.wav'
int_samples = (bed * 32767).astype(np.int16)
with wave.open(wav_path, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(int_samples.tobytes())

# Mix master soundtrack
out_mp3 = 'assets/audio/kids_hindi_soundtrack.mp3'
cmd = [
    'ffmpeg', '-y',
    '-i', wav_path,
    '-i', 'assets/voice_hindi_kids/scene1.mp3',
    '-i', 'assets/voice_hindi_kids/scene2.mp3',
    '-i', 'assets/voice_hindi_kids/scene3.mp3',
    '-i', 'assets/voice_hindi_kids/scene4.mp3',
    '-i', 'assets/voice_hindi_kids/scene5.mp3',
    '-filter_complex',
    '[1:a]adelay=100|100,volume=1.35[v1];'
    '[2:a]adelay=6100|6100,volume=1.35[v2];'
    '[3:a]adelay=12100|12100,volume=1.35[v3];'
    '[4:a]adelay=18100|18100,volume=1.35[v4];'
    '[5:a]adelay=24100|24100,volume=1.35[v5];'
    '[0:a]volume=0.7[ambient];'
    '[ambient][v1][v2][v3][v4][v5]amix=inputs=6:duration=first:dropout_transition=0[out]',
    '-map', '[out]',
    '-t', '30.0',
    '-c:a', 'libmp3lame', '-b:a', '192k',
    out_mp3
]

subprocess.run(cmd, check=True)
print(f'Master soundtrack generated: {out_mp3} (30.0s exact)')
