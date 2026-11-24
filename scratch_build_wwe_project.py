import os

os.makedirs('openfilm_wwe/shots', exist_ok=True)
os.makedirs('compositions', exist_ok=True)

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
      background: #030305;
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
      padding: 140px 60px 180px 60px;
      z-index: 10;
    }
    .badge-wrap {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .tag-badge {
      align-self: flex-start;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.6);
      color: #fbbf24;
      padding: 10px 24px;
      border-radius: 999px;
      font-size: 26px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
    }
    .scene-title {
      color: #fff;
      font-size: 42px;
      font-weight: 900;
      letter-spacing: -0.5px;
      text-shadow: 0 4px 16px rgba(0,0,0,0.8);
    }
    .subtitle-box {
      background: linear-gradient(180deg, rgba(5,5,8,0.7) 0%, rgba(5,5,8,0.95) 100%);
      border: 1px solid rgba(255,255,255,0.12);
      border-left: 6px solid #f59e0b;
      padding: 24px 32px;
      border-radius: 12px;
      backdrop-filter: blur(16px);
      box-shadow: 0 12px 32px rgba(0,0,0,0.7);
    }
    .subtitle-text {
      color: #f1f5f9;
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

s1_js = """
function drawFrame(t) {
  ctx.fillStyle = '#05070c';
  ctx.fillRect(0, 0, 1080, 1920);

  ctx.strokeStyle = 'rgba(245, 158, 11, 0.08)';
  ctx.lineWidth = 1;
  const gridSize = 80;
  for (let x = 0; x < 1080; x += gridSize) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1920); ctx.stroke();
  }
  for (let y = 0; y < 1920; y += gridSize) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1080, y); ctx.stroke();
  }

  const grad = ctx.createRadialGradient(540, 960, 100, 540, 960, 700);
  grad.addColorStop(0, 'rgba(245, 158, 11, 0.15)');
  grad.addColorStop(0.6, 'rgba(14, 21, 38, 0.4)');
  grad.addColorStop(1, 'rgba(5, 7, 12, 0.95)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 1080, 1920);

  const hubs = [
    { name: 'NEW YORK (WWF)', x: 780, y: 720 },
    { name: 'ATLANTA (NWA/WCW)', x: 700, y: 1100 },
    { name: 'MINNEAPOLIS (AWA)', x: 520, y: 640 },
    { name: 'DALLAS (WCCW)', x: 480, y: 1180 },
    { name: 'CALGARY (STAMPEDE)', x: 300, y: 520 },
    { name: 'MEMPHIS (CWA)', x: 620, y: 1020 },
    { name: 'SAN FRANCISCO', x: 180, y: 840 },
    { name: 'FLORIDA (CWF)', x: 740, y: 1320 }
  ];

  const ny = hubs[0];
  const progress = Math.min(1, t / 4.5);

  hubs.slice(1).forEach((hub, idx) => {
    ctx.beginPath();
    ctx.moveTo(ny.x, ny.y);
    const currX = ny.x + (hub.x - ny.x) * progress;
    const currY = ny.y + (hub.y - ny.y) * progress;
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = 'rgba(251, 191, 36, ' + (0.3 + 0.4 * Math.sin(t * 3 + idx)) + ')';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(hub.x, hub.y, 16 + 8 * Math.sin(t * 4 + idx), 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.5)';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(hub.x, hub.y, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#ef4444';
    ctx.fill();

    ctx.fillStyle = 'rgba(241, 245, 249, 0.75)';
    ctx.font = '600 20px sans-serif';
    ctx.fillText(hub.name, hub.x + 18, hub.y + 6);
  });

  const nyPulse = 18 + 12 * Math.sin(t * 5);
  ctx.beginPath();
  ctx.arc(ny.x, ny.y, nyPulse * 2, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(245, 158, 11, 0.2)';
  ctx.fill();

  ctx.beginPath();
  ctx.arc(ny.x, ny.y, nyPulse, 0, Math.PI * 2);
  ctx.fillStyle = '#f59e0b';
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 30;
  ctx.fill();
  ctx.shadowBlur = 0;

  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 28px sans-serif';
  ctx.fillText('WWF HEADQUARTERS', ny.x - 220, ny.y - 30);
}
"""

s2_js = """
function drawFrame(t) {
  ctx.fillStyle = '#040407';
  ctx.fillRect(0, 0, 1080, 1920);

  const beamAngle = Math.sin(t * 0.8) * 0.15;
  ctx.save();
  ctx.translate(540, 100);
  ctx.rotate(beamAngle);
  const spotGrad = ctx.createLinearGradient(0, 0, 0, 1500);
  spotGrad.addColorStop(0, 'rgba(251, 191, 36, 0.35)');
  spotGrad.addColorStop(0.5, 'rgba(251, 191, 36, 0.1)');
  spotGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = spotGrad;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-380, 1600);
  ctx.lineTo(380, 1600);
  ctx.closePath();
  ctx.fill();
  ctx.restore();

  const rand = sfc32(1985, 3, 31, Math.floor(t * 24));
  for (let i = 0; i < 40; i++) {
    const fx = rand() * 1080;
    const fy = 400 + rand() * 900;
    const brightness = rand();
    if (brightness > 0.65) {
      const radius = 4 + rand() * 14;
      ctx.beginPath();
      ctx.arc(fx, fy, radius, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255, 255, 255, ' + (rand() * 0.9) + ')';
      ctx.shadowColor = '#fff';
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  ctx.strokeStyle = '#dc2626';
  ctx.lineWidth = 14;
  for (let r = 0; r < 3; r++) {
    const ry = 1180 + r * 60;
    ctx.beginPath();
    ctx.moveTo(100, ry);
    ctx.lineTo(980, ry);
    ctx.stroke();
  }

  ctx.fillStyle = '#1e293b';
  ctx.fillRect(160, 1080, 50, 400);

  const beltY = 780 + Math.sin(t * 2) * 15;
  ctx.save();
  ctx.translate(540, beltY);
  ctx.scale(1.0 + t * 0.02, 1.0 + t * 0.02);

  ctx.fillStyle = '#f59e0b';
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 40;
  ctx.beginPath();
  ctx.ellipse(0, 0, 140, 85, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.shadowBlur = 0;

  ctx.strokeStyle = '#78350f';
  ctx.lineWidth = 5;
  ctx.stroke();

  ctx.fillStyle = '#78350f';
  ctx.font = 'bold 22px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('WORLD CHAMPION', 0, 8);
  ctx.restore();

  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.font = '800 36px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('MADISON SQUARE GARDEN • MARCH 31, 1985', 540, 500);
}
"""

s3_js = """
function drawFrame(t) {
  ctx.fillStyle = '#060609';
  ctx.fillRect(0, 0, 1080, 1920);

  ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
  for (let y = 0; y < 1920; y += 8) {
    ctx.fillRect(0, y, 1080, 4);
  }

  ctx.fillStyle = 'rgba(220, 38, 38, 0.12)';
  ctx.fillRect(80, 420, 920, 480);
  ctx.strokeStyle = '#dc2626';
  ctx.lineWidth = 4;
  ctx.strokeRect(80, 420, 920, 480);

  ctx.fillStyle = '#ef4444';
  ctx.font = '900 48px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('WWF RAW IS WAR', 120, 490);

  ctx.beginPath();
  ctx.moveTo(120, 820);
  for (let x = 120; x <= 960; x += 30) {
    const prog = (x - 120) / 840;
    const curve = Math.sin(prog * 6 + t * 4) * 40 - prog * 180;
    ctx.lineTo(x, 780 + curve);
  }
  ctx.strokeStyle = '#f87171';
  ctx.lineWidth = 6;
  ctx.stroke();

  ctx.fillStyle = 'rgba(6, 182, 212, 0.10)';
  ctx.fillRect(80, 960, 920, 480);
  ctx.strokeStyle = '#06b6d4';
  ctx.lineWidth = 4;
  ctx.strokeRect(80, 960, 920, 480);

  ctx.fillStyle = '#22d3ee';
  ctx.font = '900 48px sans-serif';
  ctx.fillText('WCW MONDAY NITRO', 120, 1030);

  ctx.beginPath();
  ctx.moveTo(120, 1150);
  for (let x = 120; x <= 960; x += 30) {
    const prog = (x - 120) / 840;
    const curve = Math.cos(prog * 5 + t * 3) * 35 + prog * 160;
    ctx.lineTo(x, 1180 + curve);
  }
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 6;
  ctx.stroke();

  if (t > 3.0) {
    ctx.save();
    ctx.translate(540, 1200);
    ctx.rotate(-0.15);
    ctx.strokeStyle = '#dc2626';
    ctx.lineWidth = 8;
    ctx.strokeRect(-260, -50, 520, 100);
    ctx.fillStyle = '#ef4444';
    ctx.font = '900 52px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('ACQUIRED BY WWF', 0, 18);
    ctx.restore();
  }
}
"""

s4_js = """
function drawFrame(t) {
  ctx.fillStyle = '#020408';
  ctx.fillRect(0, 0, 1080, 1920);

  const rand = sfc32(2024, 4, 7, 42);
  for (let i = 0; i < 280; i++) {
    const sx = rand() * 1080;
    const sy = 400 + rand() * 1050;
    const p = Math.sin(t * 3 + i) * 0.4 + 0.6;
    ctx.beginPath();
    ctx.arc(sx, sy, 2 + rand() * 3, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 255, 255, ' + p + ')';
    ctx.fill();
  }

  const rampWidth = 640;
  const rampGrad = ctx.createLinearGradient(0, 480, 0, 1400);
  rampGrad.addColorStop(0, '#f59e0b');
  rampGrad.addColorStop(0.5, '#dc2626');
  rampGrad.addColorStop(1, '#0f172a');

  ctx.fillStyle = rampGrad;
  ctx.beginPath();
  ctx.moveTo(540 - rampWidth/2, 480);
  ctx.lineTo(540 + rampWidth/2, 480);
  ctx.lineTo(540 + 200, 1400);
  ctx.lineTo(540 - 200, 1400);
  ctx.closePath();
  ctx.fill();

  for (let p = 0; p < 50; p++) {
    const py = 1200 - ((t * 800 + p * 40) % 800);
    const px = 540 + Math.sin(p * 7) * 260;
    ctx.beginPath();
    ctx.arc(px, py, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#fde047';
    ctx.fill();
  }

  ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 3;
  ctx.fillRect(140, 750, 800, 180);
  ctx.strokeRect(140, 750, 800, 180);

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 64px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('1,000,000,000+', 540, 825);

  ctx.fillStyle = '#cbd5e1';
  ctx.font = '700 28px sans-serif';
  ctx.fillText('GLOBAL HOUSEHOLDS REACHED', 540, 885);

  ctx.fillStyle = 'rgba(220, 38, 38, 0.85)';
  ctx.fillRect(360, 1000, 360, 70);
  ctx.fillStyle = '#fff';
  ctx.font = '800 32px sans-serif';
  ctx.fillText('180 COUNTRIES', 540, 1048);
}
"""

s5_js = """
function drawFrame(t) {
  ctx.fillStyle = '#040508';
  ctx.fillRect(0, 0, 1080, 1920);

  const auraGrad = ctx.createRadialGradient(540, 960, 150, 540, 960, 520);
  auraGrad.addColorStop(0, 'rgba(245, 158, 11, 0.25)');
  auraGrad.addColorStop(0.7, 'rgba(180, 83, 9, 0.08)');
  auraGrad.addColorStop(1, 'rgba(4, 5, 8, 0)');
  ctx.fillStyle = auraGrad;
  ctx.fillRect(0, 0, 1080, 1920);

  ctx.save();
  ctx.translate(540, 920);
  const rot = Math.sin(t * 0.8) * 0.04;
  ctx.rotate(rot);

  ctx.beginPath();
  ctx.arc(0, 0, 260, 0, Math.PI * 2);
  const goldGrad = ctx.createLinearGradient(-260, -260, 260, 260);
  goldGrad.addColorStop(0, '#fef08a');
  goldGrad.addColorStop(0.3, '#f59e0b');
  goldGrad.addColorStop(0.7, '#b45309');
  goldGrad.addColorStop(1, '#fef08a');
  ctx.fillStyle = goldGrad;
  ctx.shadowColor = '#fbbf24';
  ctx.shadowBlur = 50;
  ctx.fill();
  ctx.shadowBlur = 0;

  ctx.beginPath();
  ctx.arc(0, 0, 220, 0, Math.PI * 2);
  ctx.fillStyle = '#0f172a';
  ctx.fill();
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 8;
  ctx.stroke();

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 110px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('WWE', 0, 40);

  ctx.font = '800 24px sans-serif';
  ctx.fillStyle = '#e2e8f0';
  ctx.fillText('UNDISPUTED CHAMPION', 0, 100);

  ctx.restore();

  const sheenX = ((t * 600) % 2400) - 600;
  ctx.save();
  ctx.beginPath();
  ctx.rect(200, 600, 680, 680);
  ctx.clip();

  const sheenGrad = ctx.createLinearGradient(sheenX, 600, sheenX + 250, 1300);
  sheenGrad.addColorStop(0, 'rgba(255,255,255,0)');
  sheenGrad.addColorStop(0.5, 'rgba(255,255,255,0.4)');
  sheenGrad.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = sheenGrad;
  ctx.fillRect(sheenX - 200, 600, 600, 700);
  ctx.restore();

  ctx.fillStyle = 'rgba(245, 158, 11, 0.15)';
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 3;
  ctx.fillRect(240, 1340, 600, 100);
  ctx.strokeRect(240, 1340, 600, 100);

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 46px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('$21+ BILLION TKO', 540, 1405);
}
"""

shots_data = [
    (1, 'THE TERRITORY SYSTEM', '*1980: 50 REGIONAL TERRITORIES*', 'In the eighties, wrestling was divided into fifty small territories. Until one man chose to conquer them all.', s1_js),
    (2, 'WRESTLEMANIA I', '*1985: THE POP CULTURE EXPLOSION*', 'Vince McMahon bet the entire company on WrestleMania, fusing sports drama with pop culture and national TV.', s2_js),
    (3, 'THE MONDAY NIGHT WARS', '*1998: ATTITUDE ERA TAKEOVER*', 'Pushed to the brink of defeat by WCW, WWE fought back with raw Attitude—and bought out their rival.', s3_js),
    (4, 'THE GLOBAL JUGGERNAUT', '*1.0B+ HOMES IN 180 COUNTRIES*', 'They transformed into a media juggernaut, broadcasting to over a billion homes in one hundred eighty countries.', s4_js),
    (5, 'AN UNSTOPPABLE EMPIRE', '*GLOBAL POWERHOUSE*', 'Today, as a multi-billion dollar empire, WWE is an unstoppable global powerhouse.', s5_js)
]

for num, title, badge, sub, js in shots_data:
    content = make_shot_template(num, title, badge, sub, js)
    path = f'openfilm_wwe/shots/shot{num}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Wrote {path}')

film_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>How WWE Became The Biggest Wrestling Company In The World</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #000;
      position: relative;
    }
    section {
      position: absolute;
      inset: 0;
      display: none;
    }
    iframe {
      border: none;
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body>
  <section id="scene1">
    <iframe id="frame1" src="shots/shot1.html#t=0,6"></iframe>
  </section>

  <section id="scene2">
    <iframe id="frame2" src="shots/shot2.html#t=0,6"></iframe>
  </section>

  <section id="scene3">
    <iframe id="frame3" src="shots/shot3.html#t=0,6"></iframe>
  </section>

  <section id="scene4">
    <iframe id="frame4" src="shots/shot4.html#t=0,6"></iframe>
  </section>

  <section id="scene5">
    <iframe id="frame5" src="shots/shot5.html#t=0,6"></iframe>
  </section>

  <audio id="soundtrack" src="../assets/audio/wwe_soundtrack.mp3" preload="auto"></audio>

  <script>
    const sections = [
      { id: 'scene1', iframe: 'frame1', start: 0, end: 6 },
      { id: 'scene2', iframe: 'frame2', start: 6, end: 12 },
      { id: 'scene3', iframe: 'frame3', start: 12, end: 18 },
      { id: 'scene4', iframe: 'frame4', start: 18, end: 24 },
      { id: 'scene5', iframe: 'frame5', start: 24, end: 30 }
    ];

    window.film = {
      frame(t) {
        const time = Math.max(0, Math.min(30, t));
        sections.forEach(s => {
          const el = document.getElementById(s.id);
          const ifr = document.getElementById(s.iframe);
          if (time >= s.start && time < s.end) {
            el.style.display = 'block';
            if (ifr && ifr.contentWindow && ifr.contentWindow.film) {
              ifr.contentWindow.film.frame(time - s.start);
            }
          } else {
            el.style.display = 'none';
          }
        });
      }
    };
  </script>
</body>
</html>"""

with open('openfilm_wwe/film.html', 'w', encoding='utf-8') as f:
    f.write(film_html)
print('Wrote openfilm_wwe/film.html')
