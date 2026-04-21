#!/usr/bin/env python3
"""Generate audio files for 5 new Fun Zone games using edge-tts (en-US-AvaNeural)."""
import asyncio
import os
import sys
from pathlib import Path
import edge_tts

VOICE = "en-US-AvaNeural"
ROOT = Path(__file__).resolve().parents[3] / "v2" / "fun-zone" / "audio"
print(f"Audio root: {ROOT}")

# Phonemes: use short punchy sounds that edge-tts can render intelligibly
PHONEME = {
    'a': 'ahh', 'b': 'buh', 'c': 'kuh', 'd': 'duh', 'e': 'eh',
    'f': 'fff', 'g': 'guh', 'h': 'huh', 'i': 'ih', 'j': 'juh',
    'k': 'kuh', 'l': 'lll', 'm': 'mmm', 'n': 'nnn', 'o': 'aww',
    'p': 'puh', 'q': 'kwuh', 'r': 'rrr', 's': 'sss', 't': 'tuh',
    'u': 'uh', 'v': 'vvv', 'w': 'wuh', 'x': 'ks', 'y': 'yuh', 'z': 'zzz',
}

def game_plan():
    # Common phrase set per game
    common = {
        'start': "Let's play!",
        'complete': "You did it!",
        'correct1': "Yes!",
        'correct2': "Great job!",
        'correct3': "Brilliant!",
        'wrong1': "Try again!",
        'wrong2': "Have another go!",
    }

    # ── Word Builder ──
    wb_words = ['sat', 'sit', 'sip', 'tin', 'tan', 'tip', 'pin', 'pan', 'pit', 'nap']
    wb_letters = ['s', 'a', 't', 'p', 'i', 'n']
    wb = dict(common)
    wb['start'] = "Let's build words!"
    wb['complete'] = "You built them all!"
    for w in wb_words:
        wb[f'word_{w}'] = w.upper() + "!"
    for l in wb_letters:
        wb[f'snd_{l}'] = PHONEME[l]
    wb['tap_the_letter'] = "Tap the right letter!"
    wb['well_done'] = "Well done!"

    # ── Sound Match ──
    sm_letters = ['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'b', 'f']
    sm_pics = {
        'sun':'sun', 'snake':'snake', 'apple':'apple', 'ant':'ant',
        'tree':'tree', 'train':'train', 'pig':'pig', 'penguin':'penguin',
        'insect':'insect', 'igloo':'igloo', 'nose':'nose', 'net':'net',
        'moon':'moon', 'mouse':'mouse', 'dog':'dog', 'duck':'duck',
        'ball':'ball', 'boat':'boat', 'fish':'fish', 'flower':'flower',
    }
    sm = dict(common)
    sm['start'] = "Listen for the sound!"
    for l in sm_letters:
        sm[f'snd_{l}'] = PHONEME[l]
        sm[f'starts_{l}'] = f"That starts with {l.upper()}!"
    for name in sm_pics:
        sm[f'pic_{name}'] = name
    sm['good_listening'] = "Good listening!"
    sm['which_one'] = "Which picture starts with this sound?"

    # ── Rhyme Time ──
    rt_words = ['cat','hat','dog','log','fish','dish','cake','lake','star','car','bee','tree','ball','wall','pig','wig']
    rt_pairs = [('cat','hat'),('dog','log'),('fish','dish'),('cake','lake'),
                ('star','car'),('bee','tree'),('ball','wall'),('pig','wig')]
    rt = dict(common)
    rt['start'] = "Let's find rhymes!"
    rt['complete'] = "You're a rhyme star!"
    rt['great_rhyming'] = "Great rhyming!"
    rt['listen_again'] = "Listen again..."
    for w in rt_words:
        rt[f'word_{w}'] = w
        rt[f'which_{w}'] = f"Which one rhymes with {w}?"
    for a, b in rt_pairs:
        rt[f'yes_{a}_{b}'] = f"Yes! {a} and {b} rhyme!"

    # ── Bubble Letters ──
    bl = dict(common)
    bl['start'] = "Find the letters!"
    bl['complete'] = "You popped them all!"
    bl['pop'] = "Pop!"
    bl['amazing'] = "Amazing!"
    bl['so_fast'] = "So fast!"
    bl['level_up'] = "Level up!"
    for l in 'abcdefghijklmnopqrstuvwxyz':
        bl[f'snd_{l}'] = PHONEME[l]
        bl[f'find_{l}'] = f"Find the letter {l.upper()}!"

    # ── Number Bonds ──
    nb_nums = list(range(1, 11))
    nb = dict(common)
    nb['start'] = "Let's count together!"
    nb['complete'] = "You're a number hero!"
    nb['count_dots'] = "Count the dots..."
    nb['incredible'] = "Incredible!"
    num_words = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten'}
    for n, w in num_words.items():
        nb[f'num_{n}'] = w
        nb[f'how_many_{n}'] = f"How many make {n}?"
    # Sum facts for feedback: "X and Y make Z" where X+Y=Z, Z in 2..10
    for z in range(2, 11):
        for x in range(1, z):
            y = z - x
            nb[f'make_{x}_{y}_{z}'] = f"Yes! {x} and {y} make {z}!"

    return {
        'word-builder': wb,
        'sound-match': sm,
        'rhyme-time': rt,
        'bubble-letters': bl,
        'number-bonds': nb,
    }

async def gen_one(folder: Path, name: str, text: str):
    out = folder / f"{name}.mp3"
    if out.exists() and out.stat().st_size > 200:
        return (name, True, "skip")
    try:
        comm = edge_tts.Communicate(text, VOICE)
        await comm.save(str(out))
        return (name, True, "ok")
    except Exception as e:
        return (name, False, str(e)[:80])

async def main():
    plan = game_plan()
    total = sum(len(v) for v in plan.values())
    print(f"Total clips: {total}")
    sem = asyncio.Semaphore(10)

    async def worker(folder, name, text):
        async with sem:
            return await gen_one(folder, name, text)

    tasks = []
    for game, items in plan.items():
        folder = ROOT / game
        folder.mkdir(parents=True, exist_ok=True)
        for name, text in items.items():
            tasks.append(worker(folder, name, text))

    done = 0
    failed = []
    for fut in asyncio.as_completed(tasks):
        name, ok, msg = await fut
        done += 1
        if not ok:
            failed.append((name, msg))
        if done % 25 == 0:
            print(f"  {done}/{total} done")
    print(f"Finished: {done}/{total}, failures: {len(failed)}")
    for n, m in failed[:10]:
        print(f"  FAIL {n}: {m}")

if __name__ == "__main__":
    asyncio.run(main())
