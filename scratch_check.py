import wave, os
files = ['assets/voice/scene1.wav','assets/voice/scene2.wav','assets/voice/scene3.wav','assets/voice/scene4.wav','assets/voice/scene5.wav']
os.chdir(r'C:\Users\c-deepak.sharma\Desktop\content')
for f in files:
    if os.path.exists(f):
        with wave.open(f) as w:
            dur = w.getnframes() / w.getframerate()
            print(f'{f}: {dur:.2f}s')
    else:
        print(f'{f}: NOT FOUND')
