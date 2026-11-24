import urllib.request
import json
from collections import Counter

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))

moves_data = fetch_json('https://motionvideo.xyz/api/moves')
moves = moves_data.get('moves', [])
families = {}
for m in moves:
    fam = m.get('family', 'general')
    families.setdefault(fam, []).append(m.get('name'))

print("=== MOVES FAMILIES (Total Moves: {}) ===".format(len(moves)))
for fam, names in families.items():
    print(f"[{fam.upper()}] ({len(names)} moves): {', '.join(names[:5])}...")

catalog_data = fetch_json('https://motionvideo.xyz/api/catalog')
videos = catalog_data if isinstance(catalog_data, list) else catalog_data.get('videos', [])
print(f"\n=== CATALOG (Total Videos: {len(videos)}) ===")

models = Counter([v.get('model', 'Unknown') for v in videos])
print("Top Models used:")
for model, count in models.most_common(5):
    print(f" - {model}: {count} videos")

print("\nSample High-Impact Video Prompts:")
for i, v in enumerate(videos[:3], 1):
    print(f"\n{i}. {v.get('title')} ({v.get('model')})")
    print(f"   URL: https://motionvideo.xyz/videos/{v.get('slug')}")
    print(f"   Prompt: {v.get('prompt')[:220]}...")
