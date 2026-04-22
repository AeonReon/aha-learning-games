#!/usr/bin/env python3
"""
Generate audio clips for 10 math-zone games.
Voice: en-US-AnaNeural (Voice A — cute energetic American, our numbers voice).
Number pronunciations use existing ../../audio/numbers/N.mp3 — not regenerated here.
"""
import asyncio
import edge_tts
from pathlib import Path

VOICE = "en-US-AnaNeural"
BASE = Path(__file__).parent / "v2" / "math-zone" / "audio"

def shared_ops():
    return {
        "plus": "plus",
        "minus": "minus",
        "equals": "equals",
    }

def base_clips(start_text, complete_text,
               correct1="Yes! That's right!",
               correct2="Brilliant!",
               correct3="Super counting!",
               wrong1="Try again!",
               wrong2="Almost! Count again."):
    d = {
        "start": start_text,
        "complete": complete_text,
        "correct1": correct1,
        "correct2": correct2,
        "correct3": correct3,
        "wrong1": wrong1,
        "wrong2": wrong2,
    }
    d.update(shared_ops())
    return d

GAMES = {
    "apple-tree": base_clips(
        "Welcome to the Apple Tree! Let's count the apples!",
        "You counted every apple! Well done!"
    ),
    "cookie-jar": base_clips(
        "Hi there! Cookie Monster wants some cookies. Help me count how many are left!",
        "You saved all the cookies! Amazing!",
        correct3="Yummy counting!"
    ),
    "ladybug-dots": base_clips(
        "Hello! Count the spots on the ladybugs with me!",
        "You counted all the spots! Buggy brilliant!"
    ),
    "balloon-math": base_clips(
        "Balloon time! Some will pop. Count the ones that are left!",
        "You popped your way to a win! Woohoo!",
        correct1="Pop-tastic!",
        wrong1="Oopsie! Try again!"
    ),
    "counting-sheep": base_clips(
        "Watch the sheep jump! Count them all together!",
        "All the sheep are sleepy and happy! Lovely counting!",
        correct1="Baa-rilliant!"
    ),
    "piggy-bank": base_clips(
        "Let's fill the piggy bank! Count the coins!",
        "Piggy is so happy! You filled the bank!",
        correct1="Cha-ching!"
    ),
    "fish-tank": base_clips(
        "Some fish are swimming away. Count the ones that stay!",
        "What a fishy finish! You counted them all!",
        correct1="Splashy!"
    ),
    "frog-hop": base_clips(
        "Help Froggy hop! Count the hops together!",
        "Froggy is happy! You counted every hop!",
        correct1="Hop-tastic!"
    ),
    "rocket-fuel": base_clips(
        "Blast off! Count the fuel that's left!",
        "You got the rocket flying! Out of this world!",
        correct1="Stellar!"
    ),
    "snack-bar": base_clips(
        "Welcome to the snack bar! Let's do some yummy math!",
        "What a tasty finish! You're a math chef!",
        correct1="Delicious!"
    ),
}

async def gen_one(sem, path: Path, text: str):
    if path.exists():
        return "skip"
    async with sem:
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(str(path))
            return "ok"
        except Exception as e:
            print(f"FAIL {path}: {e}")
            return "fail"

async def main():
    BASE.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(10)
    tasks = []
    paths = []
    for game, clips in GAMES.items():
        d = BASE / game
        d.mkdir(parents=True, exist_ok=True)
        for name, text in clips.items():
            p = d / f"{name}.mp3"
            paths.append(p)
            tasks.append(gen_one(sem, p, text))
    results = await asyncio.gather(*tasks)
    ok = sum(1 for r in results if r == "ok")
    sk = sum(1 for r in results if r == "skip")
    fa = sum(1 for r in results if r == "fail")
    print(f"Finished: {ok}/{len(tasks)} generated, skipped {sk}, failures {fa}")

if __name__ == "__main__":
    asyncio.run(main())
