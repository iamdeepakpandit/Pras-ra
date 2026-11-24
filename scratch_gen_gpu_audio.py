import asyncio, edge_tts, subprocess, os, numpy as np, wave

VOICE = 'en-US-BrianNeural'
OUTPUT_DIR = 'assets/voice_gpu'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Regenerate scene 1 and scene 4 for perfect timing (< 5.5s)
async def fix_clips():
    comm1 = edge_tts.Communicate('A commercial jet has three million parts. But a single AI chip has over eighty billion components.', VOICE, rate='+22%')
    await comm1.save(os.path.join(OUTPUT_DIR, 'scene1.mp3'))
    
    comm4 = edge_tts.Communicate('One speck of dust destroys the wafer. Cleanrooms must be ten thousand times cleaner than surgical wards.', VOICE, rate='+25%')
    await comm4.save(os.path.join(OUTPUT_DIR, 'scene4.mp3'))

asyncio.run(fix_clips())

# Check all 5 clips
for i in range(1, 6):
    f = os.path.join(OUTPUT_DIR, f'scene{i}.mp3')
    res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f], capture_output=True, text=True)
    print(f'scene{i}.mp3: {float(res.stdout.strip()):.2f}s')

# 2. Synthesize Cinematic Audio Mix (30.00s total duration)
sr = 44100
total_dur = 30.0
total_samples = int(total_dur * sr)
t = np.linspace(0, total_dur, total_samples, endpoint=False)

# Deep analog drone (50 Hz + 100 Hz high-tech hum)
drone = 0.16 * np.sin(2 * np.pi * 50 * t) + 0.08 * np.sin(2 * np.pi * 100 * t)
drone *= (1.0 + 0.12 * np.sin(2 * np.pi * 0.5 * t))

# Precision laser / electronic pulse clicks every 6s scene change
impacts = np.zeros(total_samples)
for hit_t in [0.0, 6.0, 12.0, 18.0, 24.0]:
    hit_idx = int(hit_t * sr)
    decay_dur = 1.8
    decay_samples = int(decay_dur * sr)
    end_idx = min(total_samples, hit_idx + decay_samples)
    actual = end_idx - hit_idx
    if actual > 0:
        t_hit = np.linspace(0, decay_dur, decay_samples)[:actual]
        freq_env = 42 + 65 * np.exp(-t_hit * 5.0)
        hit_wave = 0.38 * np.sin(2 * np.pi * freq_env * t_hit) * np.exp(-t_hit * 3.0)
        impacts[hit_idx:end_idx] += hit_wave

# High-tech cleanroom airflow whisper
noise = np.random.normal(0, 0.03, total_samples)
bed = drone + impacts + noise
bed = bed / (np.max(np.abs(bed)) + 1e-6) * 0.40

wav_path = 'assets/audio/gpu_bed.wav'
int_samples = (bed * 32767).astype(np.int16)
with wave.open(wav_path, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(int_samples.tobytes())

# Mix master soundtrack using FFmpeg
out_mp3 = 'assets/audio/gpu_soundtrack.mp3'
cmd = [
    'ffmpeg', '-y',
    '-i', wav_path,
    '-i', 'assets/voice_gpu/scene1.mp3',
    '-i', 'assets/voice_gpu/scene2.mp3',
    '-i', 'assets/voice_gpu/scene3.mp3',
    '-i', 'assets/voice_gpu/scene4.mp3',
    '-i', 'assets/voice_gpu/scene5.mp3',
    '-filter_complex',
    '[1:a]adelay=100|100,volume=1.35[v1];'
    '[2:a]adelay=6100|6100,volume=1.35[v2];'
    '[3:a]adelay=12100|12100,volume=1.35[v3];'
    '[4:a]adelay=18100|18100,volume=1.35[v4];'
    '[5:a]adelay=24100|24100,volume=1.35[v5];'
    '[0:a]volume=0.65[ambient];'
    '[ambient][v1][v2][v3][v4][v5]amix=inputs=6:duration=first:dropout_transition=0[out]',
    '-map', '[out]',
    '-t', '30.0',
    '-c:a', 'libmp3lame', '-b:a', '192k',
    out_mp3
]

subprocess.run(cmd, check=True)
print(f'Master audio created: {out_mp3} (30.0s exact)')
