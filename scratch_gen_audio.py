import asyncio
import edge_tts
import json
import os

VOICE = "en-US-ChristopherNeural"
RATE = "-10%"
PITCH = "-5Hz"

SCENES = [
    {
        "id": "scene1",
        "text": "Every creature on Earth belongs here. Except us.",
    },
    {
        "id": "scene2",
        "text": "We burn under the sun that feeds all other life. We suffer chronic back pain simply from standing upright.",
    },
    {
        "id": "scene3",
        "text": "Childbirth is uniquely lethal to our species. And strip away our clothes, tools, and fire... we freeze to death in hours.",
    },
    {
        "id": "scene4",
        "text": "In 2013, an unconventional hypothesis shocked researchers: what if humanity didn’t evolve on this planet, but arrived here?",
    },
    {
        "id": "scene5",
        "text": "Speculation suggested Earth was an alien colony—or worse, a penal planet with higher gravity than our native world.",
    },
    {
        "id": "scene6",
        "text": "But the truth uncovered by genetics is far more terrifying. We share ninety-nine percent of our DNA with chimpanzees. We are not cosmic castaways.",
    },
    {
        "id": "scene7",
        "text": "Our flaws are the scars of rapid, brutal evolution—bipedalism forced our spines upright long before our skeletons were ready.",
    },
    {
        "id": "scene8",
        "text": "We are genuine children of Earth. So why... do we still feel like strangers here?",
    }
]

out_dir = r"C:\Users\c-deepak.sharma\Desktop\content\assets\voice_humans"
os.makedirs(out_dir, exist_ok=True)

async def generate():
    manifest = []
    for sc in SCENES:
        mp3_path = os.path.join(out_dir, f"{sc['id']}.mp3")
        vtt_path = os.path.join(out_dir, f"{sc['id']}.vtt")
        communicate = edge_tts.Communicate(sc['text'], VOICE, rate=RATE, pitch=PITCH)
        submaker = edge_tts.SubMaker()
        
        with open(mp3_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)
                    
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write(submaker.get_srt())
            
        manifest.append({
            "id": sc["id"],
            "text": sc["text"],
            "mp3": mp3_path
        })
    print("Done generating voiceover lines!")

asyncio.run(generate())
