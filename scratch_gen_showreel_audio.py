import os, sys, asyncio, subprocess, numpy as np, wave
import edge_tts

os.makedirs('openfilm_showreel/assets/audio', exist_ok=True)
os.makedirs('assets/audio', exist_ok=True)
os.makedirs('assets/voice_showreel', exist_ok=True)

VOICE = 'en-US-BrianNeural'

async def gen_voices():
    lines = [
        ("v1.mp3", "Showreel initialized. Kinetic typography online."),
        ("v2.mp3", "Parametric geometry and 3D wireframe."),
        ("v3.mp3", "Deterministic curves. 120 frames per second."),
        ("v4.mp3", "Antigravity motion. Open for production.")
    ]
    for filename, text in lines:
        path = os.path.join('assets/voice_showreel', filename)
        comm = edge_tts.Communicate(text, VOICE, rate='+25%', pitch='+5Hz')
        await comm.save(path)
        print(f"Generated {path}")

asyncio.run(gen_voices())

# Synthesize 15-second electronic beat & synth bed
sr = 44100
total_dur = 15.0
total_samples = int(total_dur * sr)
t = np.linspace(0, total_dur, total_samples, endpoint=False)

bpm = 128
beat_len = 60.0 / bpm
beat_samples = int(beat_len * sr)

master_track = np.zeros(total_samples, dtype=np.float32)

# 1. Sub-bass Kicks on every beat
kick_times = np.arange(0, total_dur - 0.2, beat_len)
for kt in kick_times:
    k_idx = int(kt * sr)
    dur = 0.28
    k_samples = int(dur * sr)
    if k_idx + k_samples <= total_samples:
        t_k = np.linspace(0, dur, k_samples, endpoint=False)
        # Pitch drop from 140Hz to 40Hz
        freq = 40.0 + 100.0 * np.exp(-t_k * 18.0)
        kick_env = np.exp(-t_k * 12.0)
        kick = 0.55 * np.sin(2 * np.pi * freq * t_k) * kick_env
        master_track[k_idx:k_idx + k_samples] += kick

# 2. Snares / Claps on off-beats (beats 1, 3, 5...)
snare_times = kick_times[1::2]
for st in snare_times:
    s_idx = int(st * sr)
    dur = 0.22
    s_samples = int(dur * sr)
    if s_idx + s_samples <= total_samples:
        t_s = np.linspace(0, dur, s_samples, endpoint=False)
        tone = 0.25 * np.sin(2 * np.pi * 180 * t_s) * np.exp(-t_s * 15.0)
        snare_noise = np.random.normal(0, 0.22, s_samples) * np.exp(-t_s * 18.0)
        snare = (tone + snare_noise) * 0.65
        master_track[s_idx:s_idx + s_samples] += snare

# 3. Hi-hats on 16th notes
hat_times = np.arange(beat_len / 2.0, total_dur, beat_len / 2.0)
for ht in hat_times:
    h_idx = int(ht * sr)
    dur = 0.05
    h_samples = int(dur * sr)
    if h_idx + h_samples <= total_samples:
        t_h = np.linspace(0, dur, h_samples, endpoint=False)
        hat = np.random.normal(0, 0.12, h_samples) * np.exp(-t_h * 60.0)
        master_track[h_idx:h_idx + h_samples] += hat

# 4. Synthesizer Arpeggiator (Cyberpunk synth bassline in D minor)
# Notes: D2 (73.4Hz), F2 (87.3Hz), A2 (110.0Hz), C3 (130.8Hz)
notes = [73.42, 87.31, 110.00, 130.81, 146.83, 130.81, 110.00, 87.31]
step_len = beat_len / 2.0
num_steps = int(total_dur / step_len)

for step in range(num_steps):
    note_freq = notes[step % len(notes)]
    st_time = step * step_len
    st_idx = int(st_time * sr)
    s_samples = int(step_len * sr)
    if st_idx + s_samples <= total_samples:
        t_step = np.linspace(0, step_len, s_samples, endpoint=False)
        # Sawtooth harmonic sum
        synth_wave = np.zeros(s_samples)
        for harmonic in range(1, 5):
            synth_wave += (1.0 / harmonic) * np.sin(2 * np.pi * note_freq * harmonic * t_step)
        env = np.exp(-t_step * 8.0)
        synth = 0.18 * synth_wave * env
        master_track[st_idx:st_idx + s_samples] += synth

# 5. Scene Transition Risers & Sub-Drops (0.0s, 3.75s, 7.5s, 11.25s)
scene_cuts = [0.0, 3.75, 7.5, 11.25]
for cut_t in scene_cuts:
    c_idx = int(cut_t * sr)
    # Impact explosion
    imp_dur = 1.2
    imp_samples = int(imp_dur * sr)
    end_idx = min(total_samples, c_idx + imp_samples)
    act_len = end_idx - c_idx
    if act_len > 0:
        t_imp = np.linspace(0, imp_dur, imp_samples)[:act_len]
        sub = 0.45 * np.sin(2 * np.pi * 50.0 * np.exp(-t_imp * 2.0) * t_imp) * np.exp(-t_imp * 3.5)
        crash = np.random.normal(0, 0.18, act_len) * np.exp(-t_imp * 5.0)
        master_track[c_idx:end_idx] += (sub + crash)

    # Riser before cut (except first)
    if cut_t > 0:
        rise_dur = 0.8
        rise_samples = int(rise_dur * sr)
        start_rise = max(0, c_idx - rise_samples)
        act_rise = c_idx - start_rise
        if act_rise > 0:
            t_rise = np.linspace(0, rise_dur, rise_samples)[-act_rise:]
            pitch = 100.0 + 600.0 * ((t_rise / rise_dur) ** 2)
            riser = 0.16 * np.sin(2 * np.pi * pitch * t_rise) * (t_rise / rise_dur)
            master_track[start_rise:c_idx] += riser

# Normalize music bed
peak = np.max(np.abs(master_track)) + 1e-6
master_track = (master_track / peak) * 0.75

wav_bed_path = 'openfilm_showreel/assets/audio/showreel_bed.wav'
int_samples = (master_track * 32767).astype(np.int16)
with wave.open(wav_bed_path, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(int_samples.tobytes())

print(f"Synthesized bed to {wav_bed_path}")

# Mix master soundtrack using FFmpeg with voice ducking & positioning
out_mp3 = 'openfilm_showreel/assets/audio/showreel_soundtrack.mp3'
cmd = [
    'ffmpeg', '-y',
    '-i', wav_bed_path,
    '-i', 'assets/voice_showreel/v1.mp3',
    '-i', 'assets/voice_showreel/v2.mp3',
    '-i', 'assets/voice_showreel/v3.mp3',
    '-i', 'assets/voice_showreel/v4.mp3',
    '-filter_complex',
    '[1:a]adelay=300|300,volume=1.25[v1];'
    '[2:a]adelay=4000|4000,volume=1.25[v2];'
    '[3:a]adelay=7800|7800,volume=1.25[v3];'
    '[4:a]adelay=11500|11500,volume=1.25[v4];'
    '[0:a]volume=0.85[bed];'
    '[bed][v1][v2][v3][v4]amix=inputs=5:duration=first:dropout_transition=0[out]',
    '-map', '[out]',
    '-t', '15.0',
    '-c:a', 'libmp3lame', '-b:a', '256k',
    out_mp3
]
subprocess.run(cmd, check=True)
print(f"Master showreel soundtrack generated: {out_mp3}")
