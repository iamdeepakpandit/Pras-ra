import asyncio
import edge_tts
import subprocess

async def gen_s1():
    text = "Nobody actually runs out of time. You just trade hours for things you won't remember by Friday."
    communicate = edge_tts.Communicate(text, 'en-US-ChristopherNeural', rate='+20%', pitch='-2Hz')
    mp3_path = r'C:\Users\c-deepak.sharma\Desktop\content\assets\voice_time\scene1.mp3'
    with open(mp3_path, 'wb') as f:
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                f.write(chunk['data'])
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', mp3_path]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    print('Scene 1 adjusted duration:', res.stdout.strip())

asyncio.run(gen_s1())
