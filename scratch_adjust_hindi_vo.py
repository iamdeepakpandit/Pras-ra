import asyncio, edge_tts, subprocess, os

VOICE = 'hi-IN-MadhurNeural'
OUTPUT_DIR = 'assets/voice_hindi_kids'

scripts = [
    ('scene1.mp3', 'गांव के उस रहस्यमयी जंगल में, जहां सूरज की किरणें भी जाने से डरती थीं...', '+14%'),
    ('scene2.mp3', 'आरव ने पुराने बरगद की जड़ों में छिपा एक चमकता हुआ जादुई संदूक देखा।', '+12%'),
    ('scene3.mp3', "तभी हवा में फुसफुसाहट गूंजी—'इसे कभी मत खोलना!'", '+16%'),
    ('scene4.mp3', 'लेकिन आरव रुका नहीं... क्लिक! संदूक का ताला धीरे से खुल गया...', '+18%'),
    ('scene5.mp3', 'और बाहर निकला एक नन्हा जादुई जुगनू, जिसने पूरे जंगल को चमका दिया!', '+18%')
]

async def adjust():
    for filename, text, rate in scripts:
        path = os.path.join(OUTPUT_DIR, filename)
        comm = edge_tts.Communicate(text, VOICE, rate=rate)
        await comm.save(path)
        res = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        print(f'{filename}: {dur:.2f}s')

asyncio.run(adjust())
