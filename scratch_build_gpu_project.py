import os, shutil

os.makedirs('openfilm_gpu/shots', exist_ok=True)
os.makedirs('openfilm_gpu/assets/audio', exist_ok=True)

# Copy the master audio track into openfilm_gpu/assets/audio
shutil.copy('assets/audio/gpu_soundtrack.mp3', 'openfilm_gpu/assets/audio/gpu_soundtrack.mp3')
print('Copied audio track to openfilm_gpu/assets/audio/gpu_soundtrack.mp3')

def make_shot_template(shot_num, title, badge_text, sub_line, canvas_draw_js):
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>Shot """ + str(shot_num) + """: """ + title + """</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #020306;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      position: relative;
    }
    canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 1080px;
      height: 1920px;
    }
    .overlay {
      position: absolute;
      inset: 0;
      pointer-events: none;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 130px 60px 170px 60px;
      z-index: 10;
    }
    .badge-wrap {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .tag-badge {
      align-self: flex-start;
      background: rgba(6, 182, 212, 0.15);
      border: 1px solid rgba(6, 182, 212, 0.6);
      color: #22d3ee;
      padding: 10px 24px;
      border-radius: 999px;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.35);
    }
    .scene-title {
      color: #ffffff;
      font-size: 42px;
      font-weight: 900;
      letter-spacing: -0.5px;
      text-shadow: 0 4px 20px rgba(0,0,0,0.9);
    }
    .subtitle-box {
      background: linear-gradient(180deg, rgba(3,7,18,0.75) 0%, rgba(3,7,18,0.96) 100%);
      border: 1px solid rgba(255,255,255,0.12);
      border-left: 6px solid #22d3ee;
      padding: 24px 32px;
      border-radius: 14px;
      backdrop-filter: blur(16px);
      box-shadow: 0 16px 36px rgba(0,0,0,0.8);
    }
    .subtitle-text {
      color: #f8fafc;
      font-size: 34px;
      line-height: 1.4;
      font-weight: 600;
    }
    .film-grain {
      position: absolute;
      inset: 0;
      opacity: 0.04;
      pointer-events: none;
      background-image: radial-gradient(#fff 1px, transparent 1px);
      background-size: 4px 4px;
      z-index: 5;
    }
  </style>
</head>
<body>
  <canvas id="cv" width="1080" height="1920"></canvas>
  <div class="film-grain"></div>
  <div class="overlay">
    <div class="badge-wrap">
      <div class="tag-badge">""" + badge_text + """</div>
      <div class="scene-title">""" + title + """</div>
    </div>
    <div class="subtitle-box">
      <p class="subtitle-text">""" + sub_line + """</p>
    </div>
  </div>

  <script>
    const cv = document.getElementById('cv');
    const ctx = cv.getContext('2d');

    function sfc32(a, b, c, d) {
      return function() {
        a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0; 
        var t = (a + b | 0) + d | 0;
        d = d + 1 | 0;
        a = b ^ b >>> 9;
        b = c + (c << 3) | 0;
        c = (c << 21 | c >>> 11);
        c = c + t | 0;
        return (t >>> 0) / 4294967296;
      }
    }

    """ + canvas_draw_js + """

    window.film = {
      frame(t) {
        drawFrame(t);
      }
    };

    window.film.frame(0);
  </script>
</body>
</html>"""

# Shot 1: 3 Million Parts vs 80 Billion Components (Scale Comparison)
s1_js = """
function drawFrame(t) {
  ctx.fillStyle = '#03050a';
  ctx.fillRect(0, 0, 1080, 1920);

  // Background tech grid
  ctx.strokeStyle = 'rgba(6, 182, 212, 0.07)';
  ctx.lineWidth = 1;
  for (let x = 0; x < 1080; x += 60) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1920); ctx.stroke();
  }
  for (let y = 0; y < 1920; y += 60) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1080, y); ctx.stroke();
  }

  // Top Card: Airplane Blueprint (3 Million Parts)
  ctx.save();
  ctx.translate(540, 560);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.35)';
  ctx.lineWidth = 3;
  ctx.strokeRect(-460, -180, 920, 360);
  ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
  ctx.fillRect(-460, -180, 920, 360);

  // Airplane schematic silhouette
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 4;
  ctx.beginPath();
  // Fuselage
  ctx.moveTo(0, -120);
  ctx.lineTo(30, 80);
  ctx.lineTo(80, 100);
  ctx.lineTo(0, 90);
  ctx.lineTo(-80, 100);
  ctx.lineTo(-30, 80);
  ctx.closePath();
  ctx.stroke();
  // Wings
  ctx.beginPath();
  ctx.moveTo(0, -30);
  ctx.lineTo(240, 40);
  ctx.lineTo(220, 60);
  ctx.lineTo(0, 20);
  ctx.lineTo(-220, 60);
  ctx.lineTo(-240, 40);
  ctx.closePath();
  ctx.stroke();

  // Airplane stats
  ctx.fillStyle = '#94a3b8';
  ctx.font = '700 24px monospace';
  ctx.textAlign = 'left';
  ctx.fillText('SYSTEM: COMMERCIAL JETLINER (BOEING 787)', -420, -135);
  ctx.fillStyle = '#38bdf8';
  ctx.font = '900 48px sans-serif';
  ctx.fillText('3,000,000 PARTS', -420, 140);
  ctx.restore();

  // VS Divider with electric pulse
  ctx.save();
  ctx.translate(540, 890);
  ctx.fillStyle = '#f59e0b';
  ctx.font = '900 36px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('VS', 0, 10);
  ctx.beginPath();
  ctx.arc(0, 0, 40 + Math.sin(t * 6) * 6, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.restore();

  // Bottom Card: Silicon Microprocessor (80 Billion Transistors)
  ctx.save();
  ctx.translate(540, 1220);
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
  ctx.lineWidth = 3;
  ctx.strokeRect(-460, -180, 920, 360);
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.fillRect(-460, -180, 920, 360);

  // Microscopic silicon matrix grid
  const cols = 12;
  const rows = 5;
  const startX = -320;
  const startY = -80;
  for (let c = 0; c < cols; c++) {
    for (let r = 0; r < rows; r++) {
      const px = startX + c * 55;
      const py = startY + r * 30;
      const lit = (Math.sin(t * 5 + c * 0.5 + r * 0.8) > 0);
      ctx.fillStyle = lit ? '#fbbf24' : 'rgba(245, 158, 11, 0.2)';
      ctx.fillRect(px, py, 45, 20);
    }
  }

  ctx.fillStyle = '#94a3b8';
  ctx.font = '700 24px monospace';
  ctx.textAlign = 'left';
  ctx.fillText('SYSTEM: MODERN AI PROCESSOR DIE (H100/B200)', -420, -135);
  ctx.fillStyle = '#f59e0b';
  ctx.font = '900 48px sans-serif';
  ctx.fillText('80,000,000,000+ TRANSISTORS', -420, 140);
  ctx.restore();
}
"""

# Shot 2: The Atomic Dimension (Nanometer Scale)
s2_js = """
function drawFrame(t) {
  ctx.fillStyle = '#020409';
  ctx.fillRect(0, 0, 1080, 1920);

  // Radial microscopic depth glow
  const rad = ctx.createRadialGradient(540, 960, 100, 540, 960, 600);
  rad.addColorStop(0, 'rgba(6, 182, 212, 0.2)');
  rad.addColorStop(1, 'rgba(2, 4, 9, 0)');
  ctx.fillStyle = rad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Comparative Scale Bars
  const scales = [
    { label: 'HUMAN HAIR', size: '80,000 nm', width: 880, color: '#64748b' },
    { label: 'RED BLOOD CELL', size: '7,000 nm', width: 540, color: '#ef4444' },
    { label: 'DNA DOUBLE HELIX', size: '2.5 nm', width: 220, color: '#10b981' },
    { label: 'GPU TRANSISTOR GATE', size: '3.0 nm', width: 250, color: '#f59e0b', highlight: true }
  ];

  ctx.save();
  ctx.translate(100, 480);
  scales.forEach((item, idx) => {
    const y = idx * 170;
    ctx.fillStyle = '#94a3b8';
    ctx.font = '700 24px monospace';
    ctx.fillText(item.label, 0, y);

    ctx.fillStyle = item.color;
    ctx.font = '900 32px sans-serif';
    ctx.fillText(item.size, 650, y);

    // Bar background
    ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.fillRect(0, y + 16, 880, 24);

    // Dynamic animated bar fill
    const fillW = Math.min(item.width, item.width * (t * 0.8 + 0.3));
    ctx.fillStyle = item.color;
    ctx.fillRect(0, y + 16, fillW, 24);

    if (item.highlight) {
      ctx.shadowColor = item.color;
      ctx.shadowBlur = 20;
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.strokeRect(0, y + 16, fillW, 24);
      ctx.shadowBlur = 0;
    }
  });
  ctx.restore();

  // Quantum Lattice Simulation at bottom
  ctx.save();
  ctx.translate(540, 1340);
  const latticeRows = 4;
  const latticeCols = 7;
  for (let r = 0; r < latticeRows; r++) {
    for (let c = 0; c < latticeCols; c++) {
      const lx = (c - 3) * 110;
      const ly = (r - 1.5) * 80;
      const wave = Math.sin(t * 4 + c * 0.7 + r * 1.1);

      ctx.beginPath();
      ctx.arc(lx, ly, 12 + wave * 4, 0, Math.PI * 2);
      ctx.fillStyle = wave > 0 ? '#22d3ee' : '#f59e0b';
      ctx.fill();

      // Electron bond lines
      if (c < latticeCols - 1) {
        ctx.beginPath();
        ctx.moveTo(lx, ly);
        ctx.lineTo(lx + 110, ly);
        ctx.strokeStyle = 'rgba(34, 211, 238, 0.25)';
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    }
  }

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '800 28px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('ATOMIC-SCALE SILICON TRANSISTOR ARRAY', 0, 160);
  ctx.restore();
}
"""

# Shot 3: The EUV Laser Crucible (ASML Tech)
s3_js = """
function drawFrame(t) {
  ctx.fillStyle = '#050203';
  ctx.fillRect(0, 0, 1080, 1920);

  // Laser chamber grid & vacuum shroud
  ctx.strokeStyle = 'rgba(239, 68, 68, 0.1)';
  ctx.lineWidth = 1;
  for (let y = 300; y < 1600; y += 80) {
    ctx.beginPath(); ctx.moveTo(80, y); ctx.lineTo(1000, y); ctx.stroke();
  }

  // Droplet Generator (Molten Tin Falling)
  const dropY = 400 + ((t * 900) % 550);
  ctx.save();
  ctx.translate(540, dropY);
  ctx.beginPath();
  ctx.arc(0, 0, 14, 0, Math.PI * 2);
  ctx.fillStyle = '#cbd5e1';
  ctx.shadowColor = '#fff';
  ctx.shadowBlur = 15;
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // High-Power CO2 Laser Pulse impacting the droplet
  const isPulse = (Math.sin(t * 18) > 0.4);
  if (isPulse) {
    // Laser beam from left
    ctx.beginPath();
    ctx.moveTo(0, dropY);
    ctx.lineTo(540, dropY);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 18;
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur = 40;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Laser beam from right
    ctx.beginPath();
    ctx.moveTo(1080, dropY);
    ctx.lineTo(540, dropY);
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 18;
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur = 40;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // EUV Plasma Flare (13.5nm extreme ultraviolet)
    ctx.beginPath();
    ctx.arc(540, dropY, 90, 0, Math.PI * 2);
    const flare = ctx.createRadialGradient(540, dropY, 10, 540, dropY, 90);
    flare.addColorStop(0, '#ffffff');
    flare.addColorStop(0.3, '#38bdf8');
    flare.addColorStop(0.7, '#818cf8');
    flare.addColorStop(1, 'rgba(99, 102, 241, 0)');
    ctx.fillStyle = flare;
    ctx.fill();
  }

  // Carl Zeiss Collector Mirror Schematic
  ctx.save();
  ctx.translate(540, 1260);
  ctx.beginPath();
  ctx.arc(0, 0, 320, 0.2 * Math.PI, 0.8 * Math.PI);
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 12;
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 30;
  ctx.stroke();
  ctx.shadowBlur = 0;

  // Reflected 13.5nm EUV Rays downward onto wafer
  for (let r = -240; r <= 240; r += 60) {
    ctx.beginPath();
    ctx.moveTo(r, 60);
    ctx.lineTo(r * 0.4, 260);
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.5)';
    ctx.lineWidth = 3;
    ctx.stroke();
  }
  ctx.restore();

  // Tech Specs Overlay Box
  ctx.save();
  ctx.translate(540, 1100);
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2;
  ctx.fillRect(-380, -70, 760, 140);
  ctx.strokeRect(-380, -70, 760, 140);

  ctx.fillStyle = '#38bdf8';
  ctx.font = '900 42px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('50,000 LASER BLASTS / SEC', 0, -10);

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '700 24px sans-serif';
  ctx.fillText('EXTREME ULTRAVIOLET (13.5nm WAVELENGTH)', 0, 36);
  ctx.restore();
}
"""

# Shot 4: The Zero-Tolerance Cleanroom (10,000x Surgical Sterility)
s4_js = """
function drawFrame(t) {
  ctx.fillStyle = '#05070a';
  ctx.fillRect(0, 0, 1080, 1920);

  // Sterile Yellow Photolithography Safelight Ambient
  const amberGrad = ctx.createLinearGradient(0, 0, 0, 1920);
  amberGrad.addColorStop(0, 'rgba(245, 158, 11, 0.18)');
  amberGrad.addColorStop(0.5, 'rgba(245, 158, 11, 0.05)');
  amberGrad.addColorStop(1, 'rgba(2, 6, 23, 0.95)');
  ctx.fillStyle = amberGrad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Rotating 300mm Silicon Wafer
  ctx.save();
  ctx.translate(540, 780);
  const rot = t * 0.15;
  ctx.rotate(rot);

  // Wafer disc
  ctx.beginPath();
  ctx.arc(0, 0, 300, 0, Math.PI * 2);
  const waferGrad = ctx.createRadialGradient(0, 0, 50, 0, 0, 300);
  waferGrad.addColorStop(0, '#334155');
  waferGrad.addColorStop(0.5, '#1e293b');
  waferGrad.addColorStop(0.9, '#0f172a');
  waferGrad.addColorStop(1, '#e2e8f0');
  ctx.fillStyle = waferGrad;
  ctx.fill();

  // Iridescent holographic diffraction lines on wafer
  for (let d = -260; d <= 260; d += 40) {
    ctx.beginPath();
    ctx.moveTo(d, -260);
    ctx.lineTo(d, 260);
    const rainbow = ctx.createLinearGradient(d, -260, d, 260);
    rainbow.addColorStop(0, 'rgba(6, 182, 212, 0.25)');
    rainbow.addColorStop(0.5, 'rgba(236, 72, 153, 0.25)');
    rainbow.addColorStop(1, 'rgba(245, 158, 11, 0.25)');
    ctx.strokeStyle = rainbow;
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Wafer alignment notch
  ctx.beginPath();
  ctx.arc(0, 298, 8, 0, Math.PI * 2);
  ctx.fillStyle = '#05070a';
  ctx.fill();
  ctx.restore();

  // Defect Comparison Card
  ctx.save();
  ctx.translate(540, 1340);
  ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
  ctx.strokeStyle = '#ef4444';
  ctx.lineWidth = 3;
  ctx.fillRect(-440, -150, 880, 300);
  ctx.strokeRect(-440, -150, 880, 300);

  // Dust Particle vs Transistor size comparison
  ctx.beginPath();
  ctx.arc(-260, -20, 60, 0, Math.PI * 2);
  ctx.fillStyle = '#ef4444';
  ctx.shadowColor = '#ef4444';
  ctx.shadowBlur = 25;
  ctx.fill();
  ctx.shadowBlur = 0;

  ctx.fillStyle = '#fff';
  ctx.font = '800 22px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('1 SPECK OF DUST', -260, 80);
  ctx.fillText('(10,000 nm)', -260, 110);

  // Tiny transistor dot
  ctx.beginPath();
  ctx.arc(180, -20, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#22d3ee';
  ctx.fill();

  ctx.fillStyle = '#22d3ee';
  ctx.fillText('TRANSISTOR (3 nm)', 180, 80);
  ctx.fillText('FATAL SHORT CIRCUIT', 180, 110);
  ctx.restore();
}
"""

# Shot 5: The Global Monopolies (The Hardest Object On Earth)
s5_js = """
function drawFrame(t) {
  ctx.fillStyle = '#030408';
  ctx.fillRect(0, 0, 1080, 1920);

  // Dark obsidian pedestal & golden rim light
  const rimGrad = ctx.createRadialGradient(540, 880, 100, 540, 880, 550);
  rimGrad.addColorStop(0, 'rgba(245, 158, 11, 0.22)');
  rimGrad.addColorStop(0.6, 'rgba(6, 182, 212, 0.08)');
  rimGrad.addColorStop(1, 'rgba(3, 4, 8, 0)');
  ctx.fillStyle = rimGrad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Complete GPU Package (Interposer + Logic Die + HBM3e stacks)
  ctx.save();
  ctx.translate(540, 840);
  ctx.scale(1.0 + t * 0.015, 1.0 + t * 0.015);

  // Substrate Package
  ctx.fillStyle = '#0f172a';
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 6;
  ctx.fillRect(-340, -340, 680, 680);
  ctx.strokeRect(-340, -340, 680, 680);

  // Central Dual-Compute Silicon Dies
  ctx.fillStyle = '#1e293b';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 4;
  ctx.fillRect(-170, -200, 340, 400);
  ctx.strokeRect(-170, -200, 340, 400);

  // HBM Memory stacks on left & right
  for (let m = 0; m < 4; m++) {
    const my = -190 + m * 105;
    // Left HBM
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(-310, my, 110, 85);
    // Right HBM
    ctx.fillRect(200, my, 110, 85);
  }

  // Specular golden light sweep across central die
  const sweep = ((t * 700) % 2600) - 1300;
  ctx.save();
  ctx.beginPath();
  ctx.rect(-170, -200, 340, 400);
  ctx.clip();
  const sheen = ctx.createLinearGradient(sweep, -200, sweep + 200, 200);
  sheen.addColorStop(0, 'rgba(255,255,255,0)');
  sheen.addColorStop(0.5, 'rgba(251, 191, 36, 0.7)');
  sheen.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = sheen;
  ctx.fillRect(sweep - 100, -200, 400, 400);
  ctx.restore();

  // Chip text
  ctx.fillStyle = '#ffffff';
  ctx.font = '900 44px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('NVIDIA B200', 0, -20);
  ctx.fillStyle = '#38bdf8';
  ctx.font = '700 22px monospace';
  ctx.fillText('208B TRANSISTORS • TSMC 4NP', 0, 40);
  ctx.restore();

  // Monopoly Chokepoints Banner
  ctx.save();
  ctx.translate(540, 1360);
  ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 3;
  ctx.fillRect(-440, -110, 880, 220);
  ctx.strokeRect(-440, -110, 880, 220);

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 36px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('THE CRITICAL BOTTLENECK', 0, -45);

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '700 28px monospace';
  ctx.fillText('EUV LITHOGRAPHY: ASML (100%)', 0, 10);
  ctx.fillText('ADVANCED FOUNDRY: TSMC (90%+)', 0, 60);
  ctx.restore();
}
"""

shots = [
    (1, '3 MILLION VS 80 BILLION', '*THE IMPOSSIBLE SCALE*', 'A commercial jet has three million parts. But a single AI chip has over eighty billion components.', s1_js),
    (2, 'SMALLER THAN HUMAN DNA', '*NANOMETER PRECISION*', 'Each transistor is three nanometers wide. That is smaller than a single strand of human DNA.', s2_js),
    (3, 'THE EUV LASER CRUCIBLE', '*EXTREME ULTRAVIOLET*', 'To print them, lasers vaporize molten tin fifty thousand times a second, creating EUV light.', s3_js),
    (4, '10,000x SURGICAL STERILITY', '*ZERO MARGIN OF ERROR*', 'One speck of dust ruins the entire wafer. Cleanrooms must be ten thousand times cleaner than surgical wards.', s4_js),
    (5, 'THE HARDEST OBJECT ON EARTH', '*THE CHOKEPOINT OF HUMANITY*', 'Dozens of nations can build jetliners. But only one company on Earth can print modern AI chips.', s5_js)
]

for num, title, badge, sub, js in shots:
    content = make_shot_template(num, title, badge, sub, js)
    path = f'openfilm_gpu/shots/shot{num}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Wrote {path}')

# 3. Create openfilm_gpu/film.html
film_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>Why GPUs Are Harder To Make Than Airplanes</title>
</head>
<body>
  <section>
    <iframe src="shots/shot1.html#t=0,6" at="0"></iframe>
  </section>
  <section>
    <iframe src="shots/shot2.html#t=0,6" at="6"></iframe>
  </section>
  <section>
    <iframe src="shots/shot3.html#t=0,6" at="12"></iframe>
  </section>
  <section>
    <iframe src="shots/shot4.html#t=0,6" at="18"></iframe>
  </section>
  <section>
    <iframe src="shots/shot5.html#t=0,6" at="24"></iframe>
  </section>
  <section>
    <audio src="assets/audio/gpu_soundtrack.mp3" at="0"></audio>
  </section>
</body>
</html>
"""

with open('openfilm_gpu/film.html', 'w', encoding='utf-8') as f:
    f.write(film_html)
print('Wrote openfilm_gpu/film.html successfully.')
