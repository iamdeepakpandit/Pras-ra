#!/usr/bin/env python3
"""
Antigravity High-Speed Video & Educational Motion Orchestrator
Integrated with the Educational Motion Design Skill (15 distinct visual styles):
- Editorial Chapter Frame architecture
- 15 Educational & Storytelling Motion Styles
- Multi-chapter long-form video chunking & stitching (10+ min ready)
- Concurrent audio synthesis (Edge-TTS voiceover + NumPy sound beds)
- Headless OpenFilm rendering & hardware-accelerated upscaling
"""

import os
import sys
import json
import time
import shutil
import argparse
import asyncio
import subprocess
import wave
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT_DIR = Path(__file__).resolve().parent
FINAL_DIR = ROOT_DIR / "1.final content"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================================
# 1. AUDIO SYNTHESIS ENGINE
# =========================================================================

class AudioEngine:
    @staticmethod
    async def _synth_voice_clip(text: str, voice: str, rate: str, out_path: Path):
        import edge_tts
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_path))

    @classmethod
    def synthesize_voices(cls, scenes, voice: str, rate: str, out_dir: Path):
        out_dir.mkdir(parents=True, exist_ok=True)
        tasks = []
        for s in scenes:
            text = s.get("voiceover", "").strip()
            if text:
                p = out_dir / f"scene_{s['id']}.mp3"
                tasks.append(cls._synth_voice_clip(text, voice, rate, p))
        if tasks:
            async def _run_all():
                await asyncio.gather(*tasks)
            asyncio.run(_run_all())

    @staticmethod
    def generate_sound_bed(preset: str, total_duration: float, bpm: int, out_wav: Path):
        sr = 44100
        total_samples = int(total_duration * sr)
        t = np.linspace(0, total_duration, total_samples, endpoint=False)
        track = np.zeros(total_samples, dtype=np.float32)
        beat_len = 60.0 / bpm
        kick_times = np.arange(0, total_duration - 0.2, beat_len)

        if preset == "cyber_breakbeat":
            for kt in kick_times:
                k_idx = int(kt * sr)
                dur = 0.26
                k_samples = int(dur * sr)
                if k_idx + k_samples <= total_samples:
                    t_k = np.linspace(0, dur, k_samples, endpoint=False)
                    freq = 42.0 + 95.0 * np.exp(-t_k * 18.0)
                    track[k_idx:k_idx + k_samples] += 0.55 * np.sin(2 * np.pi * freq * t_k) * np.exp(-t_k * 13.0)

            for st in kick_times[1::2]:
                s_idx = int(st * sr)
                dur = 0.20
                s_samples = int(dur * sr)
                if s_idx + s_samples <= total_samples:
                    t_s = np.linspace(0, dur, s_samples, endpoint=False)
                    tone = 0.22 * np.sin(2 * np.pi * 185 * t_s) * np.exp(-t_s * 15.0)
                    noise = np.random.normal(0, 0.20, s_samples) * np.exp(-t_s * 18.0)
                    track[s_idx:s_idx + s_samples] += (tone + noise) * 0.65

        elif preset == "educational_ambient":
            # Warm, scholarly, unobtrusive background bed
            drone = 0.18 * np.sin(2 * np.pi * 65.0 * t) + 0.08 * np.sin(2 * np.pi * 130.0 * t)
            drone *= (1.0 + 0.10 * np.sin(2 * np.pi * 0.25 * t))
            # Gentle rhythmic wooden tick every second
            for sec in range(int(total_duration)):
                tick_idx = int(sec * sr)
                if tick_idx + 1000 <= total_samples:
                    t_tick = np.linspace(0, 0.03, 1000, endpoint=False)
                    track[tick_idx:tick_idx + 1000] += 0.08 * np.sin(2 * np.pi * 880 * t_tick) * np.exp(-t_tick * 80.0)
            track += drone

        else: # cinematic_drone
            drone = 0.22 * np.sin(2 * np.pi * 55.0 * t) + 0.12 * np.sin(2 * np.pi * 110.0 * t)
            track += drone + np.random.normal(0, 0.02, total_samples)

        peak = np.max(np.abs(track)) + 1e-6
        track = (track / peak) * 0.70
        out_wav.parent.mkdir(parents=True, exist_ok=True)
        int_samples = (track * 32767).astype(np.int16)
        with wave.open(str(out_wav), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(int_samples.tobytes())

    @staticmethod
    def mix_master_soundtrack(scenes, bed_wav: Path, voice_dir: Path, total_dur: float, out_mp3: Path):
        inputs = ["-i", str(bed_wav)]
        filters = []
        mix_inputs = ["[0:a]"]
        idx = 1
        current_time = 0.0
        for s in scenes:
            dur = float(s.get("duration", 4.0))
            v_file = voice_dir / f"scene_{s['id']}.mp3"
            if v_file.exists():
                inputs.extend(["-i", str(v_file)])
                delay_ms = int((current_time + 0.25) * 1000)
                filters.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms},volume=1.30[v{idx}];")
                mix_inputs.append(f"[v{idx}]")
                idx += 1
            current_time += dur

        filters.append("".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=0[out]")
        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", "".join(filters),
            "-map", "[out]",
            "-t", str(total_dur),
            "-c:a", "libmp3lame", "-b:a", "256k",
            str(out_mp3)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# =========================================================================
# 2. EDUCATIONAL MOTION DESIGN TEMPLATES (15 STYLES)
# =========================================================================

class ShotBuilder:
    @staticmethod
    def get_template_code(template: str, scene: dict, w: int, h: int) -> str:
        h1 = scene.get("headline", "EDUCATIONAL CONCEPT")
        sub = scene.get("subtitle", "EXPLANATION")
        copy = scene.get("copy", "Clear visual explanation focused on the primary learning objective.")
        ch_num = scene.get("chapter_num", "01")
        dur = float(scene.get("duration", 5.0))

        # --- 1. EDITORIAL CHAPTER FRAME (Reference Signature Layout) ---
        if template == "editorial_chapter":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#0f1015';
    ctx.fillRect(0, 0, W, H);

    // Vignette background
    const bg = ctx.createRadialGradient(W * 0.35, H * 0.45, 100, W / 2, H / 2, 900);
    bg.addColorStop(0, '#171922');
    bg.addColorStop(1, '#090a0e');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, W, H);

    // Left Column: Editorial Information
    const leftX = 100;
    // Orange chapter number
    ctx.fillStyle = '#ea580c';
    ctx.font = '900 36px "Inter", sans-serif';
    ctx.fillText('{ch_num}', leftX, 160);

    // Large Chapter Heading
    ctx.fillStyle = '#f8fafc';
    ctx.font = '800 58px "Inter", sans-serif';
    ctx.fillText('{h1}', leftX, 240);

    // Supporting Explanatory Copy
    ctx.fillStyle = '#94a3b8';
    ctx.font = '400 24px "Inter", sans-serif';
    ctx.fillText('{sub}', leftX, 290);

    ctx.fillStyle = '#64748b';
    ctx.font = '400 18px "Courier New", monospace';
    ctx.fillText('{copy[:60]}', leftX, 350);

    // Right Demonstration Window (The Showcase Inset)
    const winX = W * 0.42, winY = 120, winW = W * 0.52, winH = H - 240;
    ctx.save();
    ctx.fillStyle = '#05070a';
    ctx.shadowColor = 'rgba(0,0,0,0.8)';
    ctx.shadowBlur = 30;
    ctx.fillRect(winX, winY, winW, winH);
    ctx.shadowBlur = 0;

    // Window border
    ctx.strokeStyle = 'rgba(234, 88, 12, 0.4)';
    ctx.lineWidth = 2;
    ctx.strokeRect(winX, winY, winW, winH);

    // Demo Canvas Action inside window
    const cx = winX + winW / 2;
    const cy = winY + winH / 2;
    const rot = t * 1.4;
    ctx.strokeStyle = '#ea580c';
    ctx.lineWidth = 3;
    ctx.strokeRect(cx - 100, cy - 100, 200, 200);
    ctx.beginPath();
    ctx.arc(cx, cy, 70 + 20 * Math.sin(t * 3), 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }}
}};
"""

        # --- 2. SCALE COMPARISON (比例尺对比) ---
        elif template == "scale_comparison":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#060810';
    ctx.fillRect(0, 0, W, H);

    // Background cosmic star dust
    ctx.fillStyle = 'rgba(255,255,255,0.4)';
    for (let i = 0; i < 50; i++) {{
      const sx = (i * 137.5) % W;
      const sy = (i * 263.3) % H;
      ctx.fillRect(sx, sy, 2, 2);
    }}

    // Title & Scale Ratio
    ctx.fillStyle = '#ffffff';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 100, 130);
    ctx.fillStyle = '#ea580c';
    ctx.font = '700 24px "Courier New", monospace';
    ctx.fillText('RATIO 1 : 109 // PLANETARY MAGNITUDE', 100, 175);

    // Small reference object (e.g. Earth)
    const earthX = 350, earthY = H / 2 + 50;
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath(); ctx.arc(earthX, earthY, 14, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = '600 18px "Inter", sans-serif';
    ctx.fillText('OBJECT A (1x)', earthX - 45, earthY + 45);

    // Giant comparison object entering (e.g. Sun)
    const giantR = 480;
    const giantX = W - 350 + (1 - Math.min(t / 1.5, 1)) * 300;
    const giantY = H / 2 + 50;
    const sunGrad = ctx.createRadialGradient(giantX, giantY, 50, giantX, giantY, giantR);
    sunGrad.addColorStop(0, '#fef08a');
    sunGrad.addColorStop(0.5, '#f97316');
    sunGrad.addColorStop(1, '#9a3412');
    ctx.fillStyle = sunGrad;
    ctx.beginPath(); ctx.arc(giantX, giantY, giantR, 0, Math.PI * 2); ctx.fill();

    // Scale Ruler Line
    ctx.strokeStyle = '#ea580c';
    ctx.lineWidth = 2;
    ctx.setLineDash([8, 8]);
    ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(giantX, giantY); ctx.stroke();
    ctx.setLineDash([]);
  }}
}};
"""

        # --- 3. WHITEBOARD DRAWING (白板手绘) ---
        elif template == "whiteboard_drawing":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, W, H);

    // Hand-drawn sketch title
    ctx.fillStyle = '#1e293b';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 120, 140);
    ctx.font = '600 24px "Inter", sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText('{sub}', 120, 185);

    // Logic Deduction Boxes (animated stroke draw-on)
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 3;
    const boxW = 320, boxH = 180;
    
    // Box 1 (Cause)
    ctx.strokeRect(180, H / 2 - 90, boxW, boxH);
    ctx.fillStyle = '#0f172a';
    ctx.font = '700 26px "Inter", sans-serif';
    ctx.fillText('CAUSE / INPUT', 220, H / 2 - 10);

    // Arrow drawing
    if (t > 1.0) {{
      const arrowP = Math.min((t - 1.0) / 0.8, 1);
      ctx.strokeStyle = '#ea580c';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(520, H / 2);
      ctx.lineTo(520 + 260 * arrowP, H / 2);
      ctx.stroke();
    }}

    // Box 2 (Effect)
    if (t > 1.8) {{
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 3;
      ctx.strokeRect(800, H / 2 - 90, boxW, boxH);
      ctx.fillStyle = '#ea580c';
      ctx.font = '700 26px "Inter", sans-serif';
      ctx.fillText('OUTPUT / RESULT', 830, H / 2 - 10);
    }}
  }}
}};
"""

        # --- 4. 3D BREAKDOWN (3D拆解) ---
        elif template == "exploded_3d":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#111318';
    ctx.fillRect(0, 0, W, H);

    // Neutral studio spotlight
    const spot = ctx.createRadialGradient(W / 2, H / 2, 50, W / 2, H / 2, 650);
    spot.addColorStop(0, '#232733');
    spot.addColorStop(1, '#0e1014');
    ctx.fillStyle = spot;
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = '#ffffff';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 100, 130);
    ctx.fillStyle = '#ea580c';
    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillText('// 3D ANATOMICAL EXPLODED VIEW', 100, 175);

    // Exploded layers floating apart
    const spread = Math.min(t / 2.0, 1) * 160;
    const cx = W / 2 + 100, cy = H / 2 + 20;

    for (let i = -2; i <= 2; i++) {{
      const ly = cy + i * (50 + spread);
      ctx.save();
      ctx.fillStyle = i === 0 ? '#ea580c' : '#334155';
      ctx.shadowColor = 'rgba(0,0,0,0.6)';
      ctx.shadowBlur = 15;
      ctx.fillRect(cx - 240, ly - 20, 480, 40);

      // Callout annotation pointers
      if (t > 1.5) {{
        ctx.strokeStyle = '#ea580c';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx + 250, ly);
        ctx.lineTo(cx + 360, ly);
        ctx.stroke();

        ctx.fillStyle = '#f8fafc';
        ctx.font = '600 16px "Inter", sans-serif';
        ctx.fillText(`COMPONENT 0${{i + 3}}`, cx + 380, ly + 5);
      }}
      ctx.restore();
    }}
  }}
}};
"""

        # --- 5. DATA INFOGRAPHIC (数据信息图) ---
        elif template == "data_infographic":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#080d1a';
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = '#ffffff';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 100, 130);
    ctx.fillStyle = '#ea580c';
    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillText('QUANTITATIVE METRIC & DISTRIBUTION', 100, 175);

    // Bar chart growth
    const bars = [
      {{ label: 'CATEGORY A', val: 0.88, color: '#ea580c' }},
      {{ label: 'CATEGORY B', val: 0.65, color: '#38bdf8' }},
      {{ label: 'CATEGORY C', val: 0.42, color: '#a855f7' }},
      {{ label: 'CATEGORY D', val: 0.25, color: '#64748b' }}
    ];

    const startY = 280, barH = 50, gap = 80;
    bars.forEach((b, i) => {{
      const by = startY + i * gap;
      const bw = (W - 550) * b.val * Math.min(t / 1.5, 1.0);

      ctx.fillStyle = '#94a3b8';
      ctx.font = '700 20px "Inter", sans-serif';
      ctx.fillText(b.label, 100, by + 32);

      ctx.fillStyle = b.color;
      ctx.fillRect(320, by, bw, barH);

      // Percentage counter
      const currentPct = Math.round(b.val * 100 * Math.min(t / 1.5, 1.0));
      ctx.fillStyle = '#ffffff';
      ctx.font = '800 24px "Inter", sans-serif';
      ctx.fillText(`${{currentPct}}%`, 340 + bw, by + 35);
    }});
  }}
}};
"""

        # --- 6. TIMELINE (时间线) ---
        elif template == "timeline":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#0a0b0e';
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = '#ffffff';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 100, 130);
    ctx.fillStyle = '#ea580c';
    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillText('CHRONOLOGICAL MILESTONES', 100, 175);

    // Central Axis Line
    const lineY = H / 2 + 50;
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(100, lineY); ctx.lineTo(W - 100, lineY); ctx.stroke();

    // Progress line
    ctx.strokeStyle = '#ea580c';
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(100, lineY); ctx.lineTo(100 + (W - 200) * p, lineY); ctx.stroke();

    // Milestones
    const milestones = [
      {{ year: '1970', desc: 'FOUNDATION' }},
      {{ year: '1995', desc: 'EXPANSION' }},
      {{ year: '2010', desc: 'TRANSFORMATION' }},
      {{ year: '2026', desc: 'CURRENT HORIZON' }}
    ];

    milestones.forEach((m, i) => {{
      const mx = 200 + i * ((W - 400) / 3);
      if (p >= i * 0.25) {{
        ctx.fillStyle = '#ea580c';
        ctx.beginPath(); ctx.arc(mx, lineY, 12, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.font = '800 32px "Inter", sans-serif';
        ctx.fillText(m.year, mx - 40, lineY - 30);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '600 18px "Courier New", monospace';
        ctx.fillText(m.desc, mx - 60, lineY + 45);
      }}
    }});
  }}
}};
"""

        # --- 7. MAP ANIMATION (地图动画) ---
        elif template == "map_animation":
            return f"""
window.film = {{
  frame(t) {{
    const p = Math.min(Math.max(t / {dur}, 0), 1);
    ctx.fillStyle = '#1c1917';
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = '#f5f5f4';
    ctx.font = '800 52px "Inter", sans-serif';
    ctx.fillText('{h1}', 100, 130);
    ctx.fillStyle = '#ea580c';
    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillText('GEOGRAPHIC EXPEDITION ROUTE', 100, 175);

    // Route curve drawing
    const p0 = [250, H - 250], p1 = [600, 300], p2 = [W - 300, H - 200];
    ctx.strokeStyle = '#ea580c';
    ctx.lineWidth = 4;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(p0[0], p0[1]);
    ctx.quadraticCurveTo(p1[0], p1[1], p0[0] + (p2[0] - p0[0]) * p, p0[1] + (p2[1] - p0[1]) * p);
    ctx.stroke();
    ctx.setLineDash([]);

    // Destination Pin
    ctx.fillStyle = '#ea580c';
    ctx.beginPath(); ctx.arc(p0[0], p0[1], 10, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = '700 20px "Inter", sans-serif';
    ctx.fillText('POINT ALPHA', p0[0] - 60, p0[1] + 35);
  }}
}};
"""

        # --- 8. BEAT-SYNCED KEY PHRASE (卡点金句) ---
        elif template == "quote_card":
            return f"""
window.film = {{
  frame(t) {{
    ctx.fillStyle = '#0a0a0c';
    ctx.fillRect(0, 0, W, H);

    ctx.save();
    ctx.translate(W / 2, H / 2);

    // Orange highlight block behind key phrase
    ctx.fillStyle = '#ea580c';
    ctx.fillRect(-550, -40, 1100, 80);

    ctx.font = '900 68px "Inter", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('{h1.upper()}', 0, 0);

    ctx.font = '600 26px "Courier New", monospace';
    ctx.fillStyle = '#f8fafc';
    ctx.fillText('{sub}', 0, 90);
    ctx.restore();
  }}
}};
"""

        # Fallback to kinetic_type / standard
        else:
            return f"""
window.film = {{
  frame(t) {{
    ctx.fillStyle = '#07070a';
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#ffffff';
    ctx.font = '900 80px "Arial Black", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('{h1}', W / 2, H / 2);
    ctx.font = '600 24px "Courier New", monospace';
    ctx.fillStyle = '#ea580c';
    ctx.fillText('{sub}', W / 2, H / 2 + 70);
  }}
}};
"""

    @classmethod
    def generate_shot_file(cls, scene: dict, shot_path: Path, w: int, h: int):
        t_code = cls.get_template_code(scene.get("template", "editorial_chapter"), scene, w, h)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width={w}, height={h}">
  <title>Scene {scene['id']}: {scene.get('headline', '')}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ width: {w}px; height: {h}px; overflow: hidden; background: #07070a; font-family: 'Inter', sans-serif; }}
    canvas {{ position: absolute; inset: 0; width: {w}px; height: {h}px; }}
  </style>
</head>
<body>
  <canvas id="c" width="{w}" height="{h}"></canvas>
  <script>
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const W = {w}, H = {h};
    {t_code}
  </script>
</body>
</html>"""
        shot_path.parent.mkdir(parents=True, exist_ok=True)
        with open(shot_path, "w", encoding="utf-8") as f:
            f.write(html)

    @classmethod
    def build_project(cls, config: dict, project_dir: Path):
        shots_dir = project_dir / "shots"
        shots_dir.mkdir(parents=True, exist_ok=True)
        w, h = config.get("resolution", [1280, 720])
        scenes = config.get("scenes", [])
        sections = []
        current_time = 0.0

        for s in scenes:
            dur = float(s.get("duration", 5.0))
            shot_file = shots_dir / f"shot{s['id']}.html"
            cls.generate_shot_file(s, shot_file, w, h)
            sections.append(
                f'  <section>\n    <iframe src="shots/shot{s["id"]}.html#t=0,{dur}" at="{current_time}"></iframe>\n  </section>'
            )
            current_time += dur

        sections.append('  <section>\n    <audio src="assets/audio/soundtrack.mp3" at="0"></audio>\n  </section>')

        film_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width={w}, height={h}">
  <title>{config.get('project', 'Educational Film')}</title>
</head>
<body>
{chr(10).join(sections)}
</body>
</html>"""
        with open(project_dir / "film.html", "w", encoding="utf-8") as f:
            f.write(film_html)


# =========================================================================
# 3. RENDER, STITCH & UPSCALE ENGINE
# =========================================================================

class RenderEngine:
    @staticmethod
    def render(project_dir: Path, target_mp4: Path):
        cmd = ["npx.cmd" if sys.platform == "win32" else "npx", "-y", "openfilm@latest", "render"]
        subprocess.run(cmd, cwd=str(project_dir), check=True)
        candidates = list(project_dir.glob("*.mp4"))
        if candidates:
            shutil.copy2(candidates[0], target_mp4)
            print(f"[SUCCESS] Exported video to: {target_mp4}")
            return target_mp4
        else:
            raise RuntimeError("No rendered MP4 found.")

    @staticmethod
    def concatenate_chapters(chapter_mp4s: list, final_output: Path):
        list_txt = final_output.parent / "concat_chapters.txt"
        with open(list_txt, "w", encoding="utf-8") as f:
            for p in chapter_mp4s:
                f.write(f"file '{p.resolve()}'\n")

        print(f"[STITCH] Seamlessly stitching {len(chapter_mp4s)} chapters into master video...")
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_txt),
            "-c", "copy",
            str(final_output)
        ]
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Master Long-Form Video ready: {final_output}")
        if list_txt.exists():
            list_txt.unlink()
        return final_output

    @staticmethod
    def generate_contact_sheet(mp4_path: Path, out_png: Path):
        cmd = [
            "ffmpeg", "-y",
            "-i", str(mp4_path),
            "-vf", "select='not(mod(n\\,60))',scale=960:540,tile=2x2",
            "-frames:v", "1",
            str(out_png)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[SUCCESS] Contact sheet generated: {out_png}")


# =========================================================================
# 4. CLI INTERFACE & MAIN DISPATCH
# =========================================================================

def main():
    parser = argparse.ArgumentParser(description="Antigravity Educational & Video Orchestrator")
    parser.add_argument("--config", type=str, help="Path to config JSON")
    parser.add_argument("--render", action="store_true", help="Render video with OpenFilm")
    parser.add_argument("--look", action="store_true", help="Generate contact sheet preview")
    args = parser.parse_args()

    if not args.config:
        print("[ERROR] Please provide --config <file.json>")
        sys.exit(1)

    config_path = Path(args.config)
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    project_name = config.get("project", "educational_project")
    project_dir = ROOT_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    scenes = config.get("scenes", [])
    total_dur = sum(float(s.get("duration", 5.0)) for s in scenes)
    print(f"\n=======================================================")
    print(f"  EDUCATIONAL MOTION ORCHESTRATOR: {project_name.upper()}")
    print(f"  Duration: {total_dur:.2f}s | Scenes: {len(scenes)}")
    print(f"=======================================================\n")

    audio_cfg = config.get("audio", {})
    voice = audio_cfg.get("voice", "en-US-BrianNeural")
    rate = audio_cfg.get("rate", "+22%")
    preset = audio_cfg.get("preset", "educational_ambient")
    bpm = audio_cfg.get("bpm", 110)

    voice_dir = project_dir / "assets" / "voice"
    audio_dir = project_dir / "assets" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    bed_wav = audio_dir / "bed.wav"
    soundtrack_mp3 = audio_dir / "soundtrack.mp3"

    print("[STAGE 1] Concurrently synthesizing educational audio & scaffolding shots...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_voice = executor.submit(AudioEngine.synthesize_voices, scenes, voice, rate, voice_dir)
        f_bed = executor.submit(AudioEngine.generate_sound_bed, preset, total_dur, bpm, bed_wav)
        f_scaffold = executor.submit(ShotBuilder.build_project, config, project_dir)
        f_voice.result()
        f_bed.result()
        f_scaffold.result()

    print("[STAGE 2] Mixing master educational soundtrack...")
    AudioEngine.mix_master_soundtrack(scenes, bed_wav, voice_dir, total_dur, soundtrack_mp3)

    if args.render:
        print("[STAGE 3] Rendering through OpenFilm Headless Engine...")
        master_mp4 = FINAL_DIR / f"{project_name}_master.mp4"
        RenderEngine.render(project_dir, master_mp4)
        if args.look:
            contact_sheet = FINAL_DIR / f"{project_name}_contact_sheet.png"
            RenderEngine.generate_contact_sheet(master_mp4, contact_sheet)

    print("\n[COMPLETE] Educational Video Orchestration Finished.")

if __name__ == "__main__":
    main()
