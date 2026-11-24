import os

os.makedirs('openfilm_showreel/shots', exist_ok=True)
os.makedirs('openfilm_showreel/assets/audio', exist_ok=True)

# Shared HTML Template generator for 1920x1080 widescreen showreel
def generate_shot_html(shot_index, shot_name, shot_subtitle, canvas_code, overlay_html=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080">
  <title>Shot {shot_index}: {shot_name}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: #07070a;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      position: relative;
    }}
    canvas {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1920px;
      height: 1080px;
      z-index: 1;
    }}
    .overlay {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 10;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 60px 80px;
    }}
    .hud-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(237, 73, 56, 0.3);
      padding-bottom: 18px;
    }}
    .hud-tag {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 15px;
      letter-spacing: 3px;
      color: #ed4938;
      text-transform: uppercase;
      font-weight: 700;
    }}
    .hud-dot {{
      width: 10px;
      height: 10px;
      background: #ed4938;
      border-radius: 50%;
      box-shadow: 0 0 12px #ed4938;
    }}
    .hud-metrics {{
      font-family: 'Courier New', Courier, monospace;
      font-size: 14px;
      letter-spacing: 2px;
      color: rgba(255, 255, 255, 0.7);
    }}
    .hud-footer {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 18px;
    }}
    .hud-info {{
      font-family: 'Courier New', Courier, monospace;
      font-size: 13px;
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 2px;
      line-height: 1.6;
    }}
    .accent-pill {{
      background: rgba(237, 73, 56, 0.15);
      border: 1px solid #ed4938;
      color: #fff;
      padding: 8px 20px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      box-shadow: 0 0 20px rgba(237, 73, 56, 0.4);
    }}
  </style>
</head>
<body>
  <canvas id="c" width="1920" height="1080"></canvas>
  
  <div class="overlay">
    <div class="hud-header">
      <div class="hud-tag">
        <div class="hud-dot"></div>
        <span>ANTIGRAVITY // REEL_2026 // SHOT_0{shot_index}</span>
      </div>
      <div class="hud-metrics">
        REC [00:00:15:00] &nbsp;|&nbsp; 120 FPS &nbsp;|&nbsp; 4K DCI &nbsp;|&nbsp; MASTER OUTPUT
      </div>
    </div>
    
    {overlay_html}

    <div class="hud-footer">
      <div class="hud-info">
        PIPELINE: DETERMINISTIC CODE CANVAS<br>
        RESOLUTION: 1920x1080 NATIVE // 16:9 CINEMA<br>
        TECHNIQUE: {shot_name.upper()}
      </div>
      <div class="accent-pill">
        {shot_subtitle.upper()}
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const W = 1920;
    const H = 1080;

    // Deterministic pseudo-random seed generator
    function pseudoRand(seed) {{
      const x = Math.sin(seed * 9999.123) * 10000;
      return x - Math.floor(x);
    }}

    {canvas_code}

    // Auto-loop preview for manual browser testing
    let startTime = null;
    function previewLoop(timestamp) {{
      if (!startTime) startTime = timestamp;
      const t = ((timestamp - startTime) / 1000) % 3.75;
      if (window.film && window.film.frame) {{
        window.film.frame(t);
      }}
      requestAnimationFrame(previewLoop);
    }}
    requestAnimationFrame(previewLoop);
  </script>
</body>
</html>
"""

# =========================================================================
# SHOT 1: KINETIC TYPOGRAPHY & SCRAMBLE DECODE (0.0s - 3.75s)
# =========================================================================
s1_canvas = """
window.film = {
  frame(t) {
    // Clamped progress 0 to 1
    const p = Math.min(Math.max(t / 3.75, 0), 1);

    // Clear background
    ctx.fillStyle = '#07070a';
    ctx.fillRect(0, 0, W, H);

    // 1. Perspective Horizon Grid
    ctx.save();
    ctx.strokeStyle = 'rgba(237, 73, 56, 0.12)';
    ctx.lineWidth = 1;
    const gridSpacing = 80;
    const gridOffset = (t * 120) % gridSpacing;
    for (let x = 0; x < W; x += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, H);
      ctx.stroke();
    }
    for (let y = gridOffset; y < H; y += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }
    ctx.restore();

    // 2. High-speed scanning laser beam
    const laserY = (t * 700) % H;
    const laserGrad = ctx.createLinearGradient(0, laserY - 40, 0, laserY + 40);
    laserGrad.addColorStop(0, 'rgba(237, 73, 56, 0)');
    laserGrad.addColorStop(0.5, 'rgba(237, 73, 56, 0.45)');
    laserGrad.addColorStop(1, 'rgba(237, 73, 56, 0)');
    ctx.fillStyle = laserGrad;
    ctx.fillRect(0, laserY - 40, W, 80);

    ctx.strokeStyle = '#ed4938';
    ctx.lineWidth = 2;
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.moveTo(0, laserY);
    ctx.lineTo(W, laserY);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // 3. Staggered Explosive Kinetic Typography
    const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!<>_—#*+';
    const targetText1 = "MOTION";
    const targetText2 = "DESIGNER";

    // Text Scramble Decode logic
    function getScrambled(target, lockTime, charDelay) {
      let res = '';
      for (let i = 0; i < target.length; i++) {
        const charLock = lockTime + i * charDelay;
        if (t >= charLock) {
          res += target[i];
        } else if (t < 0.2) {
          res += glyphs[Math.floor(pseudoRand(i * 13 + Math.floor(t * 30)) * glyphs.length)];
        } else {
          const scrambleIdx = Math.floor(pseudoRand(i * 47 + Math.floor(t * 24)) * glyphs.length);
          res += glyphs[scrambleIdx];
        }
      }
      return res;
    }

    const text1 = getScrambled(targetText1, 0.6, 0.08);
    const text2 = getScrambled(targetText2, 1.2, 0.06);

    // Camera push / scale overshoot
    let scale = 1.0;
    if (t < 0.5) {
      // Overshoot spring
      const st = t / 0.5;
      scale = 0.85 + 0.25 * Math.sin(st * Math.PI * 0.8);
    } else {
      scale = 1.0 + (t - 0.5) * 0.04;
    }

    ctx.save();
    ctx.translate(W / 2, H / 2 - 20);
    ctx.scale(scale, scale);

    // Ghost chromatic aberration echo
    ctx.font = '900 148px "Arial Black", Impact, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Cyan chromatic shift
    ctx.fillStyle = 'rgba(34, 211, 238, 0.35)';
    ctx.fillText(text1, -6 * (1 - p), -74);
    ctx.fillText(text2, 6 * (1 - p), 66);

    // Red chromatic shift
    ctx.fillStyle = 'rgba(237, 73, 56, 0.5)';
    ctx.fillText(text1, 6 * (1 - p), -74);
    ctx.fillText(text2, -6 * (1 - p), 66);

    // Crisp white foreground text
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 30;
    ctx.fillText(text1, 0, -74);
    ctx.shadowBlur = 40;
    ctx.fillText(text2, 0, 66);
    ctx.shadowBlur = 0;

    // Glowing border frame around text
    const boxW = 860;
    const boxH = 320;
    ctx.strokeStyle = 'rgba(237, 73, 56, 0.5)';
    ctx.lineWidth = 2;
    ctx.strokeRect(-boxW / 2, -boxH / 2, boxW, boxH);

    // Corner brackets
    const cLen = 30;
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 4;
    // Top-left
    ctx.beginPath(); ctx.moveTo(-boxW/2, -boxH/2 + cLen); ctx.lineTo(-boxW/2, -boxH/2); ctx.lineTo(-boxW/2 + cLen, -boxH/2); ctx.stroke();
    // Top-right
    ctx.beginPath(); ctx.moveTo(boxW/2 - cLen, -boxH/2); ctx.lineTo(boxW/2, -boxH/2); ctx.lineTo(boxW/2, -boxH/2 + cLen); ctx.stroke();
    // Bottom-left
    ctx.beginPath(); ctx.moveTo(-boxW/2, boxH/2 - cLen); ctx.lineTo(-boxW/2, boxH/2); ctx.lineTo(-boxW/2 + cLen, boxH/2); ctx.stroke();
    // Bottom-right
    ctx.beginPath(); ctx.moveTo(boxW/2 - cLen, boxH/2); ctx.lineTo(boxW/2, boxH/2); ctx.lineTo(boxW/2, boxH/2 - cLen); ctx.stroke();

    ctx.restore();

    // 4. Kinetic Subtitle banner & speed lines
    if (t > 1.8) {
      const subProg = Math.min((t - 1.8) / 0.4, 1);
      const subY = H / 2 + 220;
      ctx.save();
      ctx.globalAlpha = subProg;
      ctx.fillStyle = '#ed4938';
      ctx.font = '700 24px "Courier New", monospace';
      ctx.textAlign = 'center';
      ctx.letterSpacing = '8px';
      ctx.fillText('CRAFT OVER CODE // FRAME-PERFECT PRECISION', W / 2, subY);

      // Accent vector line
      const lineLen = 500 * subProg;
      ctx.strokeStyle = '#ed4938';
      ctx.lineWidth = 2;
      ctx.shadowColor = '#ed4938';
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.moveTo(W / 2 - lineLen / 2, subY + 20);
      ctx.lineTo(W / 2 + lineLen / 2, subY + 20);
      ctx.stroke();
      ctx.restore();
    }

    // 5. Digital Particle Sparks
    ctx.fillStyle = '#ed4938';
    for (let i = 0; i < 40; i++) {
      const px = (pseudoRand(i * 17) * W + t * (pseudoRand(i * 3) - 0.5) * 500) % W;
      const py = (pseudoRand(i * 29) * H + t * (pseudoRand(i * 7) - 0.5) * 300) % H;
      const size = pseudoRand(i * 5) * 4 + 1;
      ctx.fillRect(px, py, size, size);
    }
  }
};
"""

# =========================================================================
# SHOT 2: 3D PARAMETRIC WIREFRAME MORPH (3.75s - 7.50s)
# =========================================================================
s2_canvas = """
window.film = {
  frame(t) {
    const p = Math.min(Math.max(t / 3.75, 0), 1);

    ctx.fillStyle = '#07070a';
    ctx.fillRect(0, 0, W, H);

    // Deep radial glow in background
    const bgGlow = ctx.createRadialGradient(W / 2, H / 2, 50, W / 2, H / 2, 700);
    bgGlow.addColorStop(0, 'rgba(139, 7, 3, 0.4)');
    bgGlow.addColorStop(0.6, 'rgba(237, 73, 56, 0.08)');
    bgGlow.addColorStop(1, 'rgba(7, 7, 10, 0)');
    ctx.fillStyle = bgGlow;
    ctx.fillRect(0, 0, W, H);

    // 3D Polyhedron Math: Cube + Octahedron dual morph
    // Rotation angles as function of t
    const rx = t * 1.2;
    const ry = t * 1.8;
    const rz = t * 0.9;

    function rotX(x, y, z, a) {
      const cos = Math.cos(a), sin = Math.sin(a);
      return [x, y * cos - z * sin, y * sin + z * cos];
    }
    function rotY(x, y, z, a) {
      const cos = Math.cos(a), sin = Math.sin(a);
      return [x * cos + z * sin, y, -x * sin + z * cos];
    }
    function rotZ(x, y, z, a) {
      const cos = Math.cos(a), sin = Math.sin(a);
      return [x * cos - y * sin, x * sin + y * cos, z];
    }

    // 3D projection helper
    const fov = 850;
    function project(pt) {
      let [x, y, z] = pt;
      [x, y, z] = rotX(x, y, z, rx);
      [x, y, z] = rotY(x, y, z, ry);
      [x, y, z] = rotZ(x, y, z, rz);
      z += 600; // translate into screen
      const f = fov / z;
      return [W / 2 + x * f, H / 2 + y * f, z, f];
    }

    // Morph factor between Cube and Icosahedron/Octahedron
    const morph = 0.5 + 0.5 * Math.sin(t * 3.0);
    const size = 260 + 40 * Math.sin(t * 2.0);

    // 8 Cube Vertices
    const cubeVerts = [
      [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
      [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
    ];
    // 6 Octahedron Vertices
    const octaVerts = [
      [ 1.4, 0, 0], [-1.4, 0, 0],
      [0,  1.4, 0], [0, -1.4, 0],
      [0, 0,  1.4], [0, 0, -1.4]
    ];

    // Edges of Cube
    const cubeEdges = [
      [0,1],[1,2],[2,3],[3,0],
      [4,5],[5,6],[6,7],[7,4],
      [0,4],[1,5],[2,6],[3,7]
    ];

    // Draw connecting edges
    ctx.save();
    ctx.lineWidth = 3;
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 18;

    for (let e of cubeEdges) {
      const p1 = project(cubeVerts[e[0]].map(c => c * size));
      const p2 = project(cubeVerts[e[1]].map(c => c * size));

      // Depth gradient for 3D realism
      const grad = ctx.createLinearGradient(p1[0], p1[1], p2[0], p2[1]);
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.5, '#ed4938');
      grad.addColorStop(1, '#8b0703');
      ctx.strokeStyle = grad;

      ctx.beginPath();
      ctx.moveTo(p1[0], p1[1]);
      ctx.lineTo(p2[0], p2[1]);
      ctx.stroke();
    }

    // Draw secondary inner octahedron
    for (let i = 0; i < octaVerts.length; i++) {
      for (let j = i + 1; j < octaVerts.length; j++) {
        // connect if not opposite
        if ((i === 0 && j === 1) || (i === 2 && j === 3) || (i === 4 && j === 5)) continue;
        const p1 = project(octaVerts[i].map(c => c * size * 0.7));
        const p2 = project(octaVerts[j].map(c => c * size * 0.7));
        ctx.strokeStyle = 'rgba(34, 211, 238, 0.4)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(p1[0], p1[1]);
        ctx.lineTo(p2[0], p2[1]);
        ctx.stroke();
      }
    }

    // Draw Vertex Nodes
    for (let v of cubeVerts) {
      const p = project(v.map(c => c * size));
      const radius = 7 * p[3];
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = '#22d3ee';
      ctx.shadowBlur = 20;
      ctx.beginPath();
      ctx.arc(p[0], p[1], radius, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // Concentric orbital compass rings
    ctx.save();
    ctx.translate(W / 2, H / 2);
    ctx.rotate(t * 0.4);
    ctx.strokeStyle = 'rgba(237, 73, 56, 0.25)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([12, 18]);
    ctx.beginPath();
    ctx.arc(0, 0, 480, 0, Math.PI * 2);
    ctx.stroke();
    ctx.setLineDash([40, 10]);
    ctx.beginPath();
    ctx.arc(0, 0, 520, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();

    // Bold Typography Overlays
    ctx.save();
    ctx.fillStyle = '#ffffff';
    ctx.font = '900 64px "Arial Black", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('PARAMETRIC', 120, H / 2 - 20);
    ctx.fillStyle = '#ed4938';
    ctx.fillText('3D MORPH', 120, H / 2 + 50);

    ctx.font = '600 20px "Courier New", monospace';
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    ctx.letterSpacing = '3px';
    ctx.fillText('POLYGON RIG // DUAL OCTAHEDRAL MESH', 120, H / 2 + 95);
    ctx.fillText('DETERMINISTIC MATRIX ROTATION', 120, H / 2 + 125);
    ctx.restore();
  }
};
"""

# =========================================================================
# SHOT 3: KINETIC UI, BÉZIER CURVES & AUDIO EQUALIZER (7.50s - 11.25s)
# =========================================================================
s3_canvas = """
window.film = {
  frame(t) {
    const p = Math.min(Math.max(t / 3.75, 0), 1);

    ctx.fillStyle = '#07070a';
    ctx.fillRect(0, 0, W, H);

    // 1. Audio Frequency Equalizer Bars (32 bands)
    const numBars = 36;
    const barW = 24;
    const barGap = 16;
    const totalBarsW = numBars * (barW + barGap);
    const startX = (W - totalBarsW) / 2;
    const baseLineY = H - 180;

    ctx.save();
    for (let i = 0; i < numBars; i++) {
      // Deterministic pulsing height using harmonic sin waves
      const freqHarmonic = (i + 1) * 0.4;
      const pulse1 = Math.sin(t * 14.0 + freqHarmonic);
      const pulse2 = Math.cos(t * 8.0 + i * 0.6);
      const intensity = Math.abs(pulse1 * 0.6 + pulse2 * 0.4);
      const barH = 40 + intensity * 260;

      const bx = startX + i * (barW + barGap);
      const by = baseLineY - barH;

      const barGrad = ctx.createLinearGradient(0, by, 0, baseLineY);
      barGrad.addColorStop(0, '#ffffff');
      barGrad.addColorStop(0.3, '#ed4938');
      barGrad.addColorStop(1, '#8b0703');

      ctx.fillStyle = barGrad;
      ctx.shadowColor = '#ed4938';
      ctx.shadowBlur = intensity > 0.7 ? 16 : 6;
      ctx.fillRect(bx, by, barW, barH);
    }
    ctx.restore();

    // 2. Animated Bézier Speed Curve Editor UI
    const graphX = 240;
    const graphY = 180;
    const graphW = 1440;
    const graphH = 420;

    // Grid behind curve
    ctx.save();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 1;
    for (let x = graphX; x <= graphX + graphW; x += 120) {
      ctx.beginPath(); ctx.moveTo(x, graphY); ctx.lineTo(x, graphY + graphH); ctx.stroke();
    }
    for (let y = graphY; y <= graphY + graphH; y += 70) {
      ctx.beginPath(); ctx.moveTo(graphX, y); ctx.lineTo(graphX + graphW, y); ctx.stroke();
    }

    // Dynamic Bézier Control Points
    const p0 = [graphX, graphY + graphH];
    const p3 = [graphX + graphW, graphY];
    // Animated control handles flexing
    const p1 = [graphX + graphW * 0.25 + 60 * Math.sin(t * 4), graphY + graphH - 40 - 280 * (0.5 + 0.5 * Math.sin(t * 3))];
    const p2 = [graphX + graphW * 0.75 - 60 * Math.cos(t * 4), graphY + 40 + 200 * (0.5 + 0.5 * Math.cos(t * 3))];

    // Tangent Handles
    ctx.strokeStyle = '#22d3ee';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(p3[0], p3[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke();

    // Handle circles
    ctx.fillStyle = '#22d3ee';
    ctx.shadowColor = '#22d3ee';
    ctx.shadowBlur = 12;
    ctx.beginPath(); ctx.arc(p1[0], p1[1], 8, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(p2[0], p2[1], 8, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;

    // Draw Cubic Bézier Curve
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 6;
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 24;
    ctx.beginPath();
    ctx.moveTo(p0[0], p0[1]);
    ctx.bezierCurveTo(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Scrubber moving along Bézier
    const u = (t * 0.9) % 1.0;
    // Cubic bezier formula for u
    const bx = Math.pow(1 - u, 3) * p0[0] + 3 * Math.pow(1 - u, 2) * u * p1[0] + 3 * (1 - u) * u * u * p2[0] + Math.pow(u, 3) * p3[0];
    const by = Math.pow(1 - u, 3) * p0[1] + 3 * Math.pow(1 - u, 2) * u * p1[1] + 3 * (1 - u) * u * u * p2[1] + Math.pow(u, 3) * p3[1];

    ctx.fillStyle = '#ed4938';
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 30;
    ctx.beginPath(); ctx.arc(bx, by, 14, 0, Math.PI * 2); ctx.fill();

    // Vertical cursor line
    ctx.strokeStyle = 'rgba(237, 73, 56, 0.6)';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 6]);
    ctx.beginPath(); ctx.moveTo(bx, graphY); ctx.lineTo(bx, graphY + graphH); ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();

    // 3. Telemetry HUD Counters
    ctx.save();
    const fpsVal = (60.0 + 60.0 * Math.min(t / 2.0, 1.0)).toFixed(2);
    ctx.fillStyle = '#ffffff';
    ctx.font = '900 48px "Arial Black", sans-serif';
    ctx.fillText(`${fpsVal} FPS`, graphX, graphY - 30);

    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillStyle = '#ed4938';
    ctx.fillText('// CUBIC-BEZIER(0.16, 1, 0.3, 1) // REALTIME EASING', graphX + 320, graphY - 34);
    ctx.restore();
  }
};
"""

# =========================================================================
# SHOT 4: GRAND FINALE: REACTOR IRIS & ANTIGRAVITY MONOLITH (11.25s - 15.00s)
# =========================================================================
s4_canvas = """
window.film = {
  frame(t) {
    const p = Math.min(Math.max(t / 3.75, 0), 1);

    ctx.fillStyle = '#07070a';
    ctx.fillRect(0, 0, W, H);

    // 1. Concentric Reactor Iris rings
    ctx.save();
    ctx.translate(W / 2, H / 2);
    const numRings = 8;
    for (let r = 1; r <= numRings; r++) {
      const radius = r * 85 + (t * 120) % 85;
      const alpha = Math.max(0, 1 - radius / 750);
      ctx.strokeStyle = `rgba(237, 73, 56, ${alpha * 0.4})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, 0, radius, 0, Math.PI * 2);
      ctx.stroke();

      // Mechanical gear notch marks
      const notches = 12 * r;
      for (let n = 0; n < notches; n++) {
        const angle = (n / notches) * Math.PI * 2 + (r % 2 === 0 ? t * 0.3 : -t * 0.3);
        const nx = Math.cos(angle) * radius;
        const ny = Math.sin(angle) * radius;
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha * 0.6})`;
        ctx.fillRect(nx - 2, ny - 2, 4, 4);
      }
    }
    ctx.restore();

    // 2. Shockwave Burst at Start of shot
    if (t < 1.2) {
      const swR = (t / 1.2) * 900;
      const swAlpha = 1 - t / 1.2;
      ctx.save();
      ctx.strokeStyle = `rgba(255, 255, 255, ${swAlpha})`;
      ctx.lineWidth = 14 * swAlpha;
      ctx.shadowColor = '#ed4938';
      ctx.shadowBlur = 40;
      ctx.beginPath();
      ctx.arc(W / 2, H / 2, swR, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    // 3. Central Brand Monolith
    ctx.save();
    ctx.translate(W / 2, H / 2);

    // Background glow behind text
    const textGlow = ctx.createRadialGradient(0, 0, 50, 0, 0, 400);
    textGlow.addColorStop(0, 'rgba(237, 73, 56, 0.45)');
    textGlow.addColorStop(0.7, 'rgba(139, 7, 3, 0.15)');
    textGlow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = textGlow;
    ctx.fillRect(-600, -300, 1200, 600);

    // Sub-title badge
    ctx.font = '700 20px "Courier New", monospace';
    ctx.fillStyle = '#22d3ee';
    ctx.letterSpacing = '8px';
    ctx.textAlign = 'center';
    ctx.fillText('--- AI & CREATIVE CODE AGENT ---', 0, -110);

    // Giant Main Title: ANTIGRAVITY
    ctx.font = '900 138px "Arial Black", Impact, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#ed4938';
    ctx.shadowBlur = 40;
    ctx.fillText('ANTIGRAVITY', 0, 10);
    ctx.shadowBlur = 0;

    // Tagline
    ctx.font = '700 32px "Inter", sans-serif';
    ctx.fillStyle = '#ed4938';
    ctx.letterSpacing = '12px';
    ctx.fillText('SHOWREEL // 2026', 0, 90);

    // Call to Action Box
    ctx.font = '600 18px "Courier New", monospace';
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    ctx.fillText('[ AVAILABLE FOR COMMISSIONS & FULL VIDEO PRODUCTION ]', 0, 150);

    ctx.restore();

    // 4. Clean Blackout Fadeout in final 0.3s (t: 3.45 -> 3.75)
    if (t > 3.4) {
      const fade = Math.min((t - 3.4) / 0.35, 1.0);
      ctx.fillStyle = `rgba(7, 7, 10, ${fade})`;
      ctx.fillRect(0, 0, W, H);
    }
  }
};
"""

# Write all 4 shot HTML files
shots_def = [
    (1, "Kinetic Typography & Scramble Decode", "Text Scramble • 120 FPS", s1_canvas),
    (2, "Parametric 3D Wireframe & Morph", "Polyhedron Rigs • Spatial Math", s2_canvas),
    (3, "Kinetic UI, Bézier Curves & Equalizer", "Dynamic Easing • Audio React", s3_canvas),
    (4, "Reactor Iris & Identity Lockup", "Antigravity // Showreel 2026", s4_canvas)
]

for idx, name, sub, canvas_js in shots_def:
    html = generate_shot_html(idx, name, sub, canvas_js)
    path = f'openfilm_showreel/shots/shot{idx}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {path}")

# Write openfilm_showreel/film.html
film_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080">
  <title>Motion Designer Showreel - Antigravity</title>
</head>
<body>
  <section>
    <iframe src="shots/shot1.html#t=0,3.75" at="0"></iframe>
  </section>
  <section>
    <iframe src="shots/shot2.html#t=0,3.75" at="3.75"></iframe>
  </section>
  <section>
    <iframe src="shots/shot3.html#t=0,3.75" at="7.5"></iframe>
  </section>
  <section>
    <iframe src="shots/shot4.html#t=0,3.75" at="11.25"></iframe>
  </section>
  <section>
    <audio src="assets/audio/showreel_soundtrack.mp3" at="0"></audio>
  </section>
</body>
</html>
"""

with open('openfilm_showreel/film.html', 'w', encoding='utf-8') as f:
    f.write(film_html)
print("Generated openfilm_showreel/film.html")
