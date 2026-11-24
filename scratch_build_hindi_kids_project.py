import os, shutil

os.makedirs('openfilm_kids/shots', exist_ok=True)
os.makedirs('openfilm_kids/assets/audio', exist_ok=True)

# Copy the master audio track into openfilm_kids/assets/audio
shutil.copy('assets/audio/kids_hindi_soundtrack.mp3', 'openfilm_kids/assets/audio/kids_hindi_soundtrack.mp3')
print('Copied audio track to openfilm_kids/assets/audio/kids_hindi_soundtrack.mp3')

def make_shot_template(shot_num, title, badge_text, sub_line, canvas_draw_js):
    return """<!DOCTYPE html>
<html lang="hi">
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
      background: #04030a;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif;
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
      background: rgba(245, 158, 11, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.7);
      color: #fbbf24;
      padding: 10px 26px;
      border-radius: 999px;
      font-size: 26px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      box-shadow: 0 0 24px rgba(245, 158, 11, 0.4);
    }
    .scene-title {
      color: #ffffff;
      font-size: 46px;
      font-weight: 900;
      text-shadow: 0 4px 20px rgba(0,0,0,0.95);
    }
    .subtitle-box {
      background: linear-gradient(180deg, rgba(10,8,22,0.8) 0%, rgba(10,8,22,0.98) 100%);
      border: 1px solid rgba(255,255,255,0.15);
      border-left: 6px solid #fbbf24;
      padding: 24px 34px;
      border-radius: 16px;
      backdrop-filter: blur(16px);
      box-shadow: 0 16px 36px rgba(0,0,0,0.85);
    }
    .subtitle-text {
      color: #f8fafc;
      font-size: 36px;
      line-height: 1.45;
      font-weight: 700;
    }
    .fairy-dust {
      position: absolute;
      inset: 0;
      opacity: 0.05;
      pointer-events: none;
      background-image: radial-gradient(#fbbf24 1px, transparent 1px);
      background-size: 5px 5px;
      z-index: 5;
    }
  </style>
</head>
<body>
  <canvas id="cv" width="1080" height="1920"></canvas>
  <div class="fairy-dust"></div>
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

# Shot 1: The Whispering Enchanted Forest (घने जंगल की दास्तान)
s1_js = """
function drawFrame(t) {
  // Deep twilight night sky with purple mystical mist
  const skyGrad = ctx.createLinearGradient(0, 0, 0, 1920);
  skyGrad.addColorStop(0, '#0a0618');
  skyGrad.addColorStop(0.5, '#120b29');
  skyGrad.addColorStop(1, '#05030d');
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Twinkling stars in sky
  const rand = sfc32(101, 202, 303, 404);
  for (let i = 0; i < 90; i++) {
    const sx = rand() * 1080;
    const sy = rand() * 700;
    const twinkle = 0.3 + 0.7 * Math.sin(t * 3 + i * 2);
    ctx.beginPath();
    ctx.arc(sx, sy, 1.5 + rand() * 2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(254, 240, 138, ' + twinkle + ')';
    ctx.fill();
  }

  // Giant Full Moon with soft silver-amber rim
  ctx.save();
  ctx.beginPath();
  ctx.arc(820, 420, 140, 0, Math.PI * 2);
  const moonGrad = ctx.createRadialGradient(820, 420, 40, 820, 420, 140);
  moonGrad.addColorStop(0, '#fef9c3');
  moonGrad.addColorStop(0.8, '#fde047');
  moonGrad.addColorStop(1, 'rgba(253, 224, 71, 0)');
  ctx.fillStyle = moonGrad;
  ctx.shadowColor = '#fde047';
  ctx.shadowBlur = 60;
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Ancient Spooky Tree Trunk Silhouette
  ctx.fillStyle = '#080514';
  ctx.beginPath();
  ctx.moveTo(340, 1920);
  ctx.bezierCurveTo(380, 1300, 240, 900, 360, 600);
  ctx.bezierCurveTo(460, 350, 720, 250, 920, 180);
  ctx.lineTo(960, 260);
  ctx.bezierCurveTo(740, 360, 540, 500, 460, 760);
  ctx.bezierCurveTo(400, 1020, 580, 1380, 620, 1920);
  ctx.closePath();
  ctx.fill();

  // Glowing spiral runes on the tree bark
  ctx.save();
  ctx.strokeStyle = 'rgba(168, 85, 247, ' + (0.4 + 0.3 * Math.sin(t * 3)) + ')';
  ctx.lineWidth = 4;
  ctx.shadowColor = '#c084fc';
  ctx.shadowBlur = 18;
  ctx.beginPath();
  ctx.arc(420, 1100, 60 + Math.sin(t * 2) * 8, 0, 1.8 * Math.PI);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(420, 1100, 35, 0.4 * Math.PI, 2.2 * Math.PI);
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Floating magical fireflies (35 particles with sine movement)
  for (let f = 0; f < 35; f++) {
    const fx = (f * 32 + Math.sin(t * 2 + f) * 60) % 1080;
    const fy = 800 + (f * 26 + Math.cos(t * 1.5 + f) * 70) % 950;
    const glow = 0.4 + 0.6 * Math.sin(t * 4 + f * 3);
    ctx.beginPath();
    ctx.arc(fx, fy, 4 + Math.sin(t + f) * 2, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(52, 211, 153, ' + glow + ')';
    ctx.shadowColor = '#34d399';
    ctx.shadowBlur = 16;
    ctx.fill();
    ctx.shadowBlur = 0;
  }

  // Boy Silhouette (Aarav) holding glowing lantern on bottom left
  ctx.save();
  ctx.translate(220, 1540);
  // Aarav silhouette
  ctx.fillStyle = '#060411';
  ctx.beginPath();
  ctx.arc(0, -110, 38, 0, Math.PI * 2); // Head
  ctx.fill();
  ctx.fillRect(-26, -70, 52, 110); // Body
  // Lantern held in hand
  ctx.beginPath();
  ctx.moveTo(35, -30);
  ctx.lineTo(85, -20);
  ctx.strokeStyle = '#060411';
  ctx.lineWidth = 8;
  ctx.stroke();
  // Glowing warm lantern
  ctx.beginPath();
  ctx.arc(85, -5, 24, 0, Math.PI * 2);
  ctx.fillStyle = '#f59e0b';
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 40;
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();
}
"""

# Shot 2: Discovery of the Golden Chest (चमकता संदूक)
s2_js = """
function drawFrame(t) {
  ctx.fillStyle = '#060410';
  ctx.fillRect(0, 0, 1080, 1920);

  // Volumetric beam from above pointing to the chest
  ctx.save();
  ctx.translate(540, 300);
  const beam = ctx.createLinearGradient(0, 0, 0, 1200);
  beam.addColorStop(0, 'rgba(251, 191, 36, 0.35)');
  beam.addColorStop(0.6, 'rgba(251, 191, 36, 0.08)');
  beam.addColorStop(1, 'rgba(6, 4, 16, 0)');
  ctx.fillStyle = beam;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-380, 1200);
  ctx.lineTo(380, 1200);
  ctx.closePath();
  ctx.fill();
  ctx.restore();

  // Twisted roots wrapping around the chest
  ctx.fillStyle = '#0e081e';
  ctx.beginPath();
  ctx.moveTo(100, 1600);
  ctx.bezierCurveTo(240, 1300, 320, 1100, 380, 1050);
  ctx.lineTo(440, 1120);
  ctx.bezierCurveTo(360, 1220, 260, 1450, 180, 1680);
  ctx.fill();

  ctx.beginPath();
  ctx.moveTo(980, 1600);
  ctx.bezierCurveTo(840, 1300, 760, 1100, 700, 1050);
  ctx.lineTo(640, 1120);
  ctx.bezierCurveTo(720, 1220, 820, 1450, 900, 1680);
  ctx.fill();

  // The Antique Golden Chest
  ctx.save();
  ctx.translate(540, 1050);
  ctx.scale(1.0 + Math.sin(t * 1.5) * 0.02, 1.0 + Math.sin(t * 1.5) * 0.02);

  // Chest Base Body (Dark rich teakwood + gold trims)
  ctx.fillStyle = '#451a03';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 8;
  ctx.fillRect(-260, -60, 520, 240);
  ctx.strokeRect(-260, -60, 520, 240);

  // Chest Arched Lid
  ctx.beginPath();
  ctx.arc(0, -60, 260, Math.PI, 0, false);
  ctx.fillStyle = '#78350f';
  ctx.fill();
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 10;
  ctx.stroke();

  // Gold Straps and Rivets
  ctx.fillStyle = '#f59e0b';
  ctx.fillRect(-180, -180, 40, 360);
  ctx.fillRect(140, -180, 40, 360);

  // Glowing magical keyhole in center
  const keyPulse = 16 + 8 * Math.sin(t * 6);
  ctx.beginPath();
  ctx.arc(0, 30, keyPulse, 0, Math.PI * 2);
  ctx.fillStyle = '#fef08a';
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 50;
  ctx.fill();

  ctx.beginPath();
  ctx.moveTo(-10, 30);
  ctx.lineTo(10, 30);
  ctx.lineTo(16, 75);
  ctx.lineTo(-16, 75);
  ctx.closePath();
  ctx.fillStyle = '#f59e0b';
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Floating golden stardust particles rising from chest
  for (let p = 0; p < 25; p++) {
    const py = 1200 - ((t * 260 + p * 38) % 600);
    const px = 540 + Math.sin(p * 5 + t * 2) * 220;
    ctx.beginPath();
    ctx.arc(px, py, 3 + Math.sin(t * 4 + p) * 2, 0, Math.PI * 2);
    ctx.fillStyle = '#fef08a';
    ctx.shadowColor = '#fbbf24';
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.shadowBlur = 0;
  }
}
"""

# Shot 3: The Whispering Warning (हवा की फुसफुसाहट)
s3_js = """
function drawFrame(t) {
  ctx.fillStyle = '#050209';
  ctx.fillRect(0, 0, 1080, 1920);

  // Swirling dark violet & crimson wind vortex
  ctx.save();
  ctx.translate(540, 960);
  const vortexAngle = t * 1.8;
  ctx.rotate(vortexAngle);

  for (let arm = 0; arm < 4; arm++) {
    ctx.beginPath();
    ctx.arc(0, 0, 360, arm * 0.5 * Math.PI, (arm * 0.5 + 0.3) * Math.PI);
    ctx.strokeStyle = 'rgba(239, 68, 68, ' + (0.35 + 0.25 * Math.sin(t * 4 + arm)) + ')';
    ctx.lineWidth = 14;
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur = 30;
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
  ctx.restore();

  // Swirling autumn warning leaves
  for (let l = 0; l < 30; l++) {
    const angle = t * 2 + l * 0.4;
    const dist = 180 + (l * 20) % 350;
    const lx = 540 + Math.cos(angle) * dist;
    const ly = 960 + Math.sin(angle) * (dist * 1.3);

    ctx.save();
    ctx.translate(lx, ly);
    ctx.rotate(angle * 2);
    ctx.fillStyle = (l % 2 === 0) ? '#dc2626' : '#a855f7';
    ctx.beginPath();
    ctx.ellipse(0, 0, 18, 9, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  // Whispering Spirit Eyes in dark shadows above
  const eyeAlpha = 0.4 + 0.5 * Math.sin(t * 5);
  ctx.save();
  ctx.translate(540, 620);
  // Left eye
  ctx.beginPath();
  ctx.ellipse(-140, 0, 45, 20, -0.15, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(192, 132, 252, ' + eyeAlpha + ')';
  ctx.shadowColor = '#c084fc';
  ctx.shadowBlur = 35;
  ctx.fill();
  // Right eye
  ctx.beginPath();
  ctx.ellipse(140, 0, 45, 20, 0.15, 0, Math.PI * 2);
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Warning text banner in Hindi
  ctx.save();
  ctx.translate(540, 1340);
  ctx.fillStyle = 'rgba(20, 8, 28, 0.9)';
  ctx.strokeStyle = '#ef4444';
  ctx.lineWidth = 4;
  ctx.fillRect(-380, -60, 760, 120);
  ctx.strokeRect(-380, -60, 760, 120);

  ctx.fillStyle = '#f87171';
  ctx.font = '900 48px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('‘इसे कभी मत खोलना!’', 0, 16);
  ctx.restore();
}
"""

# Shot 4: Turning the Key (सस्पेंस का चरम - चाबी घूमी)
s4_js = """
function drawFrame(t) {
  ctx.fillStyle = '#06030c';
  ctx.fillRect(0, 0, 1080, 1920);

  // Intense focal spotlight on the antique keyhole
  const spot = ctx.createRadialGradient(540, 920, 60, 540, 920, 500);
  spot.addColorStop(0, 'rgba(251, 191, 36, 0.35)');
  spot.addColorStop(0.7, 'rgba(147, 51, 234, 0.1)');
  spot.addColorStop(1, 'rgba(6, 3, 12, 0)');
  ctx.fillStyle = spot;
  ctx.fillRect(0, 0, 1080, 1920);

  // Giant Antique Keyhole Plate (Close-up Macro)
  ctx.save();
  ctx.translate(540, 920);

  // Heavy sculpted brass plate
  ctx.fillStyle = '#78350f';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 14;
  ctx.beginPath();
  ctx.arc(0, 0, 320, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Inner lock chamber
  ctx.beginPath();
  ctx.arc(0, -30, 70, 0, Math.PI * 2);
  ctx.fillStyle = '#020105';
  ctx.fill();

  ctx.beginPath();
  ctx.moveTo(-35, -30);
  ctx.lineTo(35, -30);
  ctx.lineTo(50, 120);
  ctx.lineTo(-50, 120);
  ctx.closePath();
  ctx.fill();

  // The Golden Antique Key turning smoothly
  // At t=2.0s the key rotates 90 degrees ("CLICK!")
  const keyRot = (t < 2.0) ? (t / 2.0) * 0.4 : 0.4 + Math.min(1.57, (t - 2.0) * 3.0);
  ctx.save();
  ctx.rotate(keyRot);

  // Key handle & shaft
  ctx.strokeStyle = '#fef08a';
  ctx.lineWidth = 22;
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 40;
  ctx.beginPath();
  ctx.arc(0, -180, 55, 0, Math.PI * 2);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(0, -125);
  ctx.lineTo(0, 40);
  ctx.stroke();

  // Key teeth
  ctx.beginPath();
  ctx.moveTo(0, 10);
  ctx.lineTo(35, 10);
  ctx.moveTo(0, 35);
  ctx.lineTo(45, 35);
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Expanding "CLICK!" shockwave ring after t=2.5s
  if (t > 2.5) {
    const clickAge = t - 2.5;
    ctx.beginPath();
    ctx.arc(0, 0, clickAge * 450, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(254, 240, 138, ' + Math.max(0, 1 - clickAge * 0.7) + ')';
    ctx.lineWidth = 8;
    ctx.stroke();

    // Radiant light rays breaking through
    for (let ray = 0; ray < 12; ray++) {
      const rayAngle = ray * (Math.PI / 6) + t;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(Math.cos(rayAngle) * 550, Math.sin(rayAngle) * 550);
      ctx.strokeStyle = 'rgba(251, 191, 36, 0.4)';
      ctx.lineWidth = 4;
      ctx.stroke();
    }
  }

  ctx.restore();

  // Sound Effect Text
  if (t > 2.2 && t < 4.5) {
    ctx.save();
    ctx.translate(540, 1420);
    ctx.fillStyle = '#fbbf24';
    ctx.font = '900 68px sans-serif';
    ctx.textAlign = 'center';
    ctx.shadowColor = '#f59e0b';
    ctx.shadowBlur = 30;
    ctx.fillText('* CLICK! *', 0, 0);
    ctx.shadowBlur = 0;
    ctx.restore();
  }
}
"""

# Shot 5: The Magical Reveal (रोशनी का चमत्कार)
s5_js = """
function drawFrame(t) {
  // Radiant Golden & Celestial Blue Wonderland
  const burstGrad = ctx.createRadialGradient(540, 880, 80, 540, 880, 750);
  burstGrad.addColorStop(0, '#fef9c3');
  burstGrad.addColorStop(0.3, '#fde047');
  burstGrad.addColorStop(0.7, '#38bdf8');
  burstGrad.addColorStop(1, '#0c1a3b');
  ctx.fillStyle = burstGrad;
  ctx.fillRect(0, 0, 1080, 1920);

  // Rotating celestial sunburst rays from chest
  ctx.save();
  ctx.translate(540, 880);
  ctx.rotate(t * 0.4);
  for (let r = 0; r < 24; r++) {
    ctx.beginPath();
    ctx.moveTo(0, 0);
    const angle = r * (Math.PI / 12);
    ctx.lineTo(Math.cos(angle) * 1100, Math.sin(angle) * 1100);
    ctx.strokeStyle = (r % 2 === 0) ? 'rgba(254, 240, 138, 0.35)' : 'rgba(56, 189, 248, 0.25)';
    ctx.lineWidth = 18;
    ctx.stroke();
  }
  ctx.restore();

  // Open Chest at bottom center
  ctx.save();
  ctx.translate(540, 1350);
  ctx.fillStyle = '#78350f';
  ctx.fillRect(-220, 0, 440, 180);
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 8;
  ctx.strokeRect(-220, 0, 440, 180);
  // Chest open lid flipped back
  ctx.beginPath();
  ctx.ellipse(0, -30, 240, 50, 0, 0, Math.PI * 2);
  ctx.fillStyle = '#fef08a';
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 60;
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // The Cute Giant Magical Star Firefly rising into air
  const spriteY = 920 - Math.min(220, t * 75) + Math.sin(t * 5) * 20;
  const spriteX = 540 + Math.sin(t * 3) * 60;
  ctx.save();
  ctx.translate(spriteX, spriteY);

  // Shimmering translucent fairy wings (flapping)
  const flap = Math.sin(t * 22) * 0.4;
  ctx.save();
  ctx.scale(1.0, 1.0 + flap);
  // Left wing
  ctx.beginPath();
  ctx.ellipse(-90, -40, 80, 40, -0.3, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
  ctx.shadowColor = '#67e8f9';
  ctx.shadowBlur = 25;
  ctx.fill();
  // Right wing
  ctx.beginPath();
  ctx.ellipse(90, -40, 80, 40, 0.3, 0, Math.PI * 2);
  ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Glowing glowing body (Golden orb)
  ctx.beginPath();
  ctx.arc(0, 0, 75, 0, Math.PI * 2);
  ctx.fillStyle = '#fef08a';
  ctx.shadowColor = '#f59e0b';
  ctx.shadowBlur = 50;
  ctx.fill();
  ctx.shadowBlur = 0;

  // Cute Big Cartoon Eyes
  ctx.fillStyle = '#0f172a';
  // Left eye
  ctx.beginPath();
  ctx.arc(-24, -10, 14, 0, Math.PI * 2);
  ctx.fill();
  // Right eye
  ctx.beginPath();
  ctx.arc(24, -10, 14, 0, Math.PI * 2);
  ctx.fill();

  // Eye sparkle highlights
  ctx.fillStyle = '#ffffff';
  ctx.beginPath(); ctx.arc(-20, -14, 5, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(28, -14, 5, 0, Math.PI * 2); ctx.fill();

  // Cute Smiling Mouth
  ctx.beginPath();
  ctx.arc(0, 14, 20, 0, Math.PI, false);
  ctx.strokeStyle = '#0f172a';
  ctx.lineWidth = 5;
  ctx.stroke();

  // Rosy cheeks
  ctx.fillStyle = 'rgba(251, 113, 133, 0.6)';
  ctx.beginPath(); ctx.arc(-42, 10, 12, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(42, 10, 12, 0, Math.PI * 2); ctx.fill();

  ctx.restore();

  // Floating sparkling stars trail
  for (let s = 0; s < 30; s++) {
    const spX = (spriteX - 150 + (s * 35) % 300) + Math.sin(t * 3 + s) * 30;
    const spY = (spriteY + 80 + (s * 25) % 350) + Math.cos(t * 2 + s) * 20;
    ctx.beginPath();
    ctx.arc(spX, spY, 3 + Math.sin(t * 4 + s) * 2, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = '#fef08a';
    ctx.shadowBlur = 10;
    ctx.fill();
    ctx.shadowBlur = 0;
  }
}
"""

shots = [
    (1, 'घने जंगल की दास्तान', '*अनोखा रहस्य*', 'गांव के उस रहस्यमयी जंगल में, जहां सूरज की किरणें भी जाने से डरती थीं...', s1_js),
    (2, 'चमकता जादुई संदूक', '*छिपा हुआ खजाना*', 'आरव ने पुराने बरगद की जड़ों में छिपा एक चमकता हुआ जादुई संदूक देखा।', s2_js),
    (3, 'हवा की फुसफुसाहट', '*चेतावनी*', 'तभी हवा में फुसफुसाहट गूंजी—‘इसे कभी मत खोलना!’', s3_js),
    (4, 'चाबी घूमी...', '*सस्पेंस का चरम*', 'लेकिन आरव रुका नहीं... और संदूक का ताला धीरे से खुल गया!', s4_js),
    (5, 'रोशनी का जादुई संसार', '*चमत्कारी अंत*', 'और बाहर निकला एक नन्हा जादुई जुगनू, जिसने पूरे जंगल को चमका दिया!', s5_js)
]

for num, title, badge, sub, js in shots:
    content = make_shot_template(num, title, badge, sub, js)
    path = f'openfilm_kids/shots/shot{num}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Wrote {path}')

# 3. Create openfilm_kids/film.html
film_html = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>जादुई संदूक का रहस्य - Animated Hindi Suspense Story</title>
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
    <audio src="assets/audio/kids_hindi_soundtrack.mp3" at="0"></audio>
  </section>
</body>
</html>
"""

with open('openfilm_kids/film.html', 'w', encoding='utf-8') as f:
    f.write(film_html)
print('Wrote openfilm_kids/film.html successfully.')
