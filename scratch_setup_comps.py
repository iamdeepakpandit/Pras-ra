import os

def create_comp(num, start, dur):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WWE Scene {num}</title>
  <link rel="stylesheet" href="../node_modules/hyperframes/dist/hyperframes.css">
  <style>
    body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      margin: 0;
      background: #000;
    }}
    .clip {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
    }}
    iframe {{
      border: none;
      width: 100%;
      height: 100%;
    }}
  </style>
</head>
<body>
  <div data-composition-id="wwe-scene-{num}" data-width="1080" data-height="1920" data-duration="{dur}" data-fps="30">
    <div class="clip" data-start="0" data-duration="{dur}">
      <iframe src="../openfilm_wwe/shots/shot{num}.html" data-layout-allow-overflow="true"></iframe>
    </div>
  </div>
  <script src="../node_modules/gsap/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["wwe-scene-{num}"] = tl;
  </script>
</body>
</html>"""

for i in range(1, 6):
    content = create_comp(i, (i - 1) * 6, 6)
    with open(f"compositions/wwe_scene{i}.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created compositions/wwe_scene{i}.html")

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>How WWE Became The Biggest Wrestling Company In The World</title>
  <link rel="stylesheet" href="node_modules/hyperframes/dist/hyperframes.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1920px;
      background: #000;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .clip {
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
    }
  </style>
</head>
<body>
  <div data-composition-id="main-root" data-width="1080" data-height="1920" data-duration="30" data-fps="30">
    <!-- Scene 1: 0 - 6s -->
    <div class="clip" data-start="0" data-duration="6" data-composition-src="compositions/wwe_scene1.html"></div>

    <!-- Scene 2: 6 - 12s -->
    <div class="clip" data-start="6" data-duration="6" data-composition-src="compositions/wwe_scene2.html"></div>

    <!-- Scene 3: 12 - 18s -->
    <div class="clip" data-start="12" data-duration="6" data-composition-src="compositions/wwe_scene3.html"></div>

    <!-- Scene 4: 18 - 24s -->
    <div class="clip" data-start="18" data-duration="6" data-composition-src="compositions/wwe_scene4.html"></div>

    <!-- Scene 5: 24 - 30s -->
    <div class="clip" data-start="24" data-duration="6" data-composition-src="compositions/wwe_scene5.html"></div>

    <!-- Master Audio Track -->
    <audio src="assets/audio/wwe_soundtrack.mp3" data-start="0" data-duration="30" preload="auto"></audio>
  </div>

  <script src="node_modules/gsap/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    window.__timelines["main-root"] = gsap.timeline({ paused: true });
  </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("Updated index.html to 30.0s WWE master timeline.")
