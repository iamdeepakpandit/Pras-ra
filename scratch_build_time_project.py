import os

scenes_data = [
    {
        "id": "time_scene1",
        "file": "compositions/time_scene1.html",
        "dur": 6.00,
        "image": "../assets/images/time/scene1_hourglass_up.jpg",
        "audio": "../assets/voice_time/scene1.mp3",
        "audio_dur": 5.81,
        "pill": "*NOT RUNNING OUT OF TIME*",
        "meta": "SCENE 1: GRAVITY DEFIED",
        "text": "Nobody actually runs out of time.<br><span class=\"hl-emerald\">You just trade hours for things you won't remember by Friday.</span>",
        "motion": "tl.to('#bg-img', { scale: 1.12, duration: 6.00, ease: 'power1.inOut' }, 0); tl.to('#glow-overlay', { opacity: 0.4, duration: 1.5, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 0);"
    },
    {
        "id": "time_scene2",
        "file": "compositions/time_scene2.html",
        "dur": 9.00,
        "image": "../assets/images/time/scene2_silhouette_rain.jpg",
        "audio": "../assets/voice_time/scene2.mp3",
        "audio_dur": 8.16,
        "pill": "*LOCKING IN (FEB EDITION)*",
        "meta": "SCENE 2: THE SHADOW",
        "text": "Every January we swear this is the year we lock in.<br><span class=\"hl-cyan\">By February we're optimizing our 'recovery' from planning.</span>",
        "motion": "tl.to('#bg-img', { scale: 1.08, duration: 9.00, ease: 'none' }, 0);"
    },
    {
        "id": "time_scene3",
        "file": "compositions/time_scene3.html",
        "dur": 11.00,
        "image": "../assets/images/time/scene3_split_screen.jpg",
        "audio": "../assets/voice_time/scene3.mp3",
        "audio_dur": 9.10,
        "pill": "*NOISE ≠ MOMENTUM*",
        "meta": "SCENE 3: BUSYNESS VS. MOMENTUM",
        "text": "Busyness feels like progress because your brain confuses noise with momentum.<br><span class=\"hl-emerald\">Checking ten boxes doesn't mean you moved an inch.</span>",
        "motion": "tl.to('#bg-img', { scale: 1.07, y: -20, duration: 11.00, ease: 'none' }, 0);"
    },
    {
        "id": "time_scene4",
        "file": "compositions/time_scene4.html",
        "dur": 9.00,
        "image": "../assets/images/time/scene4_hourglass_tilt.jpg",
        "audio": "../assets/voice_time/scene4.mp3",
        "audio_dur": 7.92,
        "pill": "*THREE YEARS LATER...*",
        "meta": "SCENE 4: THE FREEZE",
        "text": "The scariest part isn't failing.<br><span class=\"hl-cyan\">It's waking up three years later with a clean feed and zero proof you lived.</span>",
        "motion": "tl.to('#bg-img', { scale: 1.10, rotation: 1.5, duration: 9.00, ease: 'power1.out' }, 0);"
    },
    {
        "id": "time_scene5",
        "file": "compositions/time_scene5.html",
        "dur": 7.00,
        "image": "../assets/images/time/scene5_final_grain.jpg",
        "audio": "../assets/voice_time/scene5.mp3",
        "audio_dur": 4.90,
        "pill": "*UNTIL WE MEET AGAIN*",
        "meta": "SCENE 5: THE FINAL GRAIN",
        "text": "Anyway... see you tomorrow.<br><span class=\"hl-emerald\">Until we meet again.</span>",
        "motion": "tl.to('#bg-img', { scale: 1.06, duration: 7.00, ease: 'none' }, 0);"
    }
]

SCENE_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --emerald: #10b981;
        --cyan: #38bdf8;
        --ink: #ffffff;
      }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#020817; font-family:'Poppins', sans-serif; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
      .clip {{ position:absolute; }}
      .full-frame {{ top:0; left:0; width:1080px; height:1920px; }}
      #bg-img {{
        width:1160px; height:2060px; object-fit:cover; object-position:center; display:block;
        transform-origin:center center; margin-left:-40px; margin-top:-70px;
      }}
      .grad-bot {{
        bottom:0; left:0; width:1080px; height:750px;
        background:linear-gradient(to top, rgba(2,8,23,0.96) 0%, rgba(2,8,23,0.75) 50%, transparent 100%);
        pointer-events:none; z-index:10;
      }}
      .grad-top {{
        top:0; left:0; width:1080px; height:450px;
        background:linear-gradient(to bottom, rgba(2,8,23,0.85) 0%, transparent 100%);
        pointer-events:none; z-index:10;
      }}
      .grain {{
        top:0; left:0; width:1080px; height:1920px;
        background-image:url('../assets/images/lyric/film_grain.png');
        background-repeat:repeat; mix-blend-mode:overlay; opacity:0.38;
        pointer-events:none; z-index:20;
      }}
      .tag-box {{
        top:160px; left:80px; width:920px; display:flex; align-items:center; gap:16px;
        pointer-events:none; z-index:30; opacity:0;
      }}
      .tag-pill {{
        background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.5);
        padding:8px 22px; border-radius:30px; font-size:28px; font-weight:700;
        letter-spacing:0.12em; text-transform:uppercase; color:var(--emerald);
        text-shadow:0 0 20px rgba(16,185,129,0.5);
      }}
      .tag-meta {{ font-size:28px; font-weight:600; letter-spacing:0.1em; color:rgba(255,255,255,0.7); text-transform:uppercase; }}
      .sub-box {{
        bottom:200px; left:80px; width:920px; min-height:220px;
        display:flex; flex-direction:column; justify-content:flex-end; pointer-events:none; z-index:30; opacity:0;
      }}
      .sub-text {{ font-size:50px; line-height:1.35; font-weight:700; color:#ffffff; text-shadow:0 4px 24px rgba(0,0,0,0.95); }}
      .hl-emerald {{ color:var(--emerald); text-shadow:0 0 30px rgba(16,185,129,0.7); }}
      .hl-cyan {{ color:var(--cyan); text-shadow:0 0 30px rgba(56,189,248,0.7); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{comp_id}" data-start="0" data-duration="{dur:.2f}" data-width="1080" data-height="1920">
      <img id="bg-img" class="clip full-frame" data-layout-allow-overflow="true" src="{image}" alt="" data-start="0" data-duration="{dur:.2f}" data-track-index="0" />
      <div id="grad-top-{idx}" class="clip grad-top" data-start="0" data-duration="{dur:.2f}" data-track-index="1"></div>
      <div id="grad-bot-{idx}" class="clip grad-bot" data-start="0" data-duration="{dur:.2f}" data-track-index="2"></div>
      <div id="grain-{idx}" class="clip grain" data-start="0" data-duration="{dur:.2f}" data-track-index="3"></div>

      <div id="tag-{idx}" class="clip tag-box" data-start="0" data-duration="{dur:.2f}" data-track-index="4">
        <span class="tag-pill">{pill}</span>
        <span class="tag-meta">{meta}</span>
      </div>

      <div id="sub-{idx}" class="clip sub-box" data-start="0" data-duration="{dur:.2f}" data-track-index="5">
        <p class="sub-text">{text}</p>
      </div>

      <audio id="vo-{idx}" src="{audio}" data-start="0.15" data-duration="{audio_dur:.2f}" data-hf-media-start-basis="local" data-has-audio="true"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {motion}
      tl.fromTo('#tag-{idx}', {{ opacity: 0, y: -15 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }}, 0.2);
      tl.fromTo('#sub-{idx}', {{ opacity: 0, y: 25 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }}, 0.35);
      window.__timelines['{comp_id}'] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

# 1. Write individual scene files
for idx, s in enumerate(scenes_data, 1):
    html = SCENE_HTML.format(
        comp_id=s["id"],
        dur=s["dur"],
        idx=idx,
        image=s["image"],
        audio=s["audio"],
        audio_dur=s["audio_dur"],
        pill=s["pill"],
        meta=s["meta"],
        text=s["text"],
        motion=s["motion"]
    )
    with open(s["file"], "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {s['file']}")

# 2. Write root index.html
ROOT_HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --ground: #020817;
        --ink: #ffffff;
      }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        margin: 0;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--ground);
        font-family: 'Poppins', sans-serif;
      }
      #root {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }
      .scene-slot {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
      }
    </style>
  </head>
  <body>
    <!-- Root composition: 42s Vertical Neo-Noir Short (1080x1920) -->
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="42.00"
      data-width="1080"
      data-height="1920"
    >
      <!-- Scene 1: Gravity Defied (0.00s - 6.00s) -->
      <div
        class="clip scene-slot"
        id="slot-time-scene1"
        data-composition-id="time_scene1"
        data-composition-src="compositions/time_scene1.html"
        data-start="0.00"
        data-duration="6.00"
        data-track-index="0"
      ></div>

      <!-- Scene 2: The Shadow (6.00s - 15.00s) -->
      <div
        class="clip scene-slot"
        id="slot-time-scene2"
        data-composition-id="time_scene2"
        data-composition-src="compositions/time_scene2.html"
        data-start="6.00"
        data-duration="9.00"
        data-track-index="0"
      ></div>

      <!-- Scene 3: Busyness vs. Momentum (15.00s - 26.00s) -->
      <div
        class="clip scene-slot"
        id="slot-time-scene3"
        data-composition-id="time_scene3"
        data-composition-src="compositions/time_scene3.html"
        data-start="15.00"
        data-duration="11.00"
        data-track-index="0"
      ></div>

      <!-- Scene 4: The Freeze (26.00s - 35.00s) -->
      <div
        class="clip scene-slot"
        id="slot-time-scene4"
        data-composition-id="time_scene4"
        data-composition-src="compositions/time_scene4.html"
        data-start="26.00"
        data-duration="9.00"
        data-track-index="0"
      ></div>

      <!-- Scene 5: The Final Grain (35.00s - 42.00s) -->
      <div
        class="clip scene-slot"
        id="slot-time-scene5"
        data-composition-id="time_scene5"
        data-composition-src="compositions/time_scene5.html"
        data-start="35.00"
        data-duration="7.00"
        data-track-index="0"
      ></div>

      <!-- Master Dark Ambient & SFX Soundtrack -->
      <audio
        id="soundtrack-audio"
        src="assets/audio/time_soundtrack.mp3"
        data-start="0"
        data-duration="42.00"
        data-has-audio="true"
      ></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(ROOT_HTML)
print("Wrote index.html (42.00s)")
