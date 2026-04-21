#!/usr/bin/env python3
"""
Generate Monster Mixer audio clips using edge-tts (en-US-AvaNeural).

Run from the repo root:
  python3 audio/fun-zone/monster-mixer/generate.py

Requires:  pip install edge-tts
"""

import asyncio, os, sys
try:
    import edge_tts
except ImportError:
    sys.exit("Please install edge-tts:  pip install edge-tts")

VOICE = "en-US-AvaNeural"
OUT   = os.path.dirname(__file__)

CLIPS = [
    # Gameplay phrases
    ("mix-it-up",       "Mix it up!"),
    ("meet-your-monster","Meet your monster!"),
    ("make-another",    "Make another!"),
    ("wow-look-at-that","Wow, look at that!"),
    ("so-silly",        "That is SO silly!"),
    ("i-love-it",       "I love it!"),
    ("what-a-monster",  "What a monster!"),
    ("tada",            "Ta-daa!"),
    # Monster names (10 pre-generated examples)
    ("snorglefuzz",     "Snorgle fuzz!"),
    ("blobzozorp",      "Blobzo zorp!"),
    ("wiggleplop",      "Wiggle plop!"),
    ("fumblekins",      "Fumble kins!"),
    ("grumblewump",     "Grumble wump!"),
    ("zippityblorp",    "Zippity blorp!"),
    ("bumblegrant",     "Bumble grunt!"),
    ("drizzysnoot",     "Drizzy snoot!"),
    ("squigglefizz",    "Squiggle fizz!"),
    ("wackydoodle",     "Wacky doodle!"),
]

async def gen(name, text):
    out = os.path.join(OUT, name + ".mp3")
    communicate = edge_tts.Communicate(text, VOICE, rate="-5%", pitch="+10Hz")
    await communicate.save(out)
    print(f"  ✓  {name}.mp3")

async def main():
    print(f"Generating {len(CLIPS)} clips with voice {VOICE}…")
    for name, text in CLIPS:
        await gen(name, text)
    print("Done!")

asyncio.run(main())
