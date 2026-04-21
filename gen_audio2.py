#!/usr/bin/env python3
"""Generate pre-rendered TTS clips for the five new fun-zone games.

Voice: en-US-AvaNeural (same as previous batch).
Run: python3 gen_audio2.py
Safe to re-run — skips any file that already exists.
"""
import asyncio
import os
import sys
import edge_tts

VOICE = "en-US-AvaNeural"
ROOT = os.path.join("v2", "fun-zone", "audio")

# ----- GAME 1: Alphabet Train -----
# 3 rounds of 5 letters each: A-E, F-J, K-O
TRAIN_LETTERS = list("ABCDEFGHIJKLMNO")
alphabet_train = {
    "start": "Choo choo! Let's build the Alphabet Train!",
    "complete": "Amazing! You built the whole train!",
    "correct1": "Yes! All aboard!",
    "correct2": "Choo choo! Nice one!",
    "correct3": "That's it! Keep going!",
    "wrong1": "Oops, try a different letter!",
    "wrong2": "Listen again and try!",
    "trip1": "First trip! Letters A to E.",
    "trip2": "Second trip! Letters F to J.",
    "trip3": "Last trip! Letters K to O.",
    "what_next": "What letter comes next?",
    "all_aboard": "All aboard!",
}
for L in TRAIN_LETTERS:
    alphabet_train[f"add_{L.lower()}"] = f"Add the letter {L}!"
    alphabet_train[f"let_{L.lower()}"] = f"{L}!"

# ----- GAME 2: Letter Hunt -----
# 10 rounds across letters s,a,t,p,i,n,m,d,b,f
HUNT_LETTERS = list("satpinmdbf")
letter_hunt = {
    "start": "Grab your magnifying glass! Let's hunt for letters!",
    "complete": "Super Spotter! You found every letter!",
    "correct1": "You found it!",
    "correct2": "Great spotting!",
    "correct3": "Eagle eyes!",
    "wrong1": "Keep looking!",
    "wrong2": "Try another one!",
    "where_is_it": "Where is it hiding?",
    "super_detective": "Super detective!",
}
for L in HUNT_LETTERS:
    letter_hunt[f"find_{L}"] = f"Find the letter {L.upper()}!"
    letter_hunt[f"let_{L}"] = f"{L.upper()}!"

# ----- GAME 3: Rocket Countdown -----
# 3 flights: Moon (5→0), Mars (8→0), Stars (10→0)
rocket_countdown = {
    "start": "Get ready for takeoff, astronaut!",
    "complete": "You are an amazing astronaut!",
    "correct1": "Yes!",
    "correct2": "Good job!",
    "correct3": "Keep counting down!",
    "wrong1": "Look for the next number!",
    "wrong2": "Try again, astronaut!",
    "moon_flight": "First flight! To the Moon!",
    "mars_flight": "Next stop, the red planet Mars!",
    "stars_flight": "Last flight! To the stars!",
    "blast_off": "Blast off!",
    "three_two_one": "Three, two, one!",
}
for n in range(11):
    rocket_countdown[f"tap_{n}"] = f"Tap {n}!"
    rocket_countdown[f"num_{n}"] = f"{n}!"

# ----- GAME 4: Dino Eggs -----
# 10 rounds counting eggs 1-10
dino_eggs = {
    "start": "Mama dino needs help counting her eggs!",
    "complete": "You helped every baby dino hatch!",
    "correct1": "Yes!",
    "correct2": "That's right!",
    "correct3": "Good counting!",
    "wrong1": "Count them one more time!",
    "wrong2": "Try again, little helper!",
    "how_many": "How many eggs in the nest?",
    "count_with_me": "Count with me!",
    "hatching": "They're hatching!",
    "baby_dino": "A baby dino!",
}
for n in range(1, 11):
    dino_eggs[f"num_{n}"] = f"{n}!"
    dino_eggs[f"yes_{n}"] = f"Yes! {n} eggs!"

# ----- GAME 5: Shape Party -----
SHAPES = ["circle", "square", "triangle", "star", "heart"]
shape_party = {
    "start": "It's a Shape Party! Let's dance!",
    "complete": "What a party! Every shape is grooving!",
    "correct1": "Boogie!",
    "correct2": "Groovy!",
    "correct3": "Yes! Dance!",
    "wrong1": "Look for the matching shape!",
    "wrong2": "Try another bin!",
    "where_goes": "Where does this shape go?",
    "party_time": "Party time!",
    "dance_dance": "Dance dance dance!",
    "round1": "Round one!",
    "round2": "Round two!",
    "round3": "Last round!",
}
for s in SHAPES:
    shape_party[f"tap_{s}"] = f"Tap the {s}!"
    shape_party[f"shape_{s}"] = f"{s.capitalize()}!"

GAMES = {
    "alphabet-train": alphabet_train,
    "letter-hunt": letter_hunt,
    "rocket-countdown": rocket_countdown,
    "dino-eggs": dino_eggs,
    "shape-party": shape_party,
}

SEM = asyncio.Semaphore(10)


async def gen_one(game, name, text):
    path = os.path.join(ROOT, game, f"{name}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return (game, name, "skip")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    async with SEM:
        try:
            comm = edge_tts.Communicate(text, VOICE)
            await comm.save(path)
            return (game, name, "ok")
        except Exception as e:
            return (game, name, f"ERR {e}")


async def main():
    jobs = []
    for game, clips in GAMES.items():
        for name, text in clips.items():
            jobs.append(gen_one(game, name, text))
    print(f"Generating {len(jobs)} clips...", flush=True)
    done = 0
    fails = 0
    skips = 0
    for coro in asyncio.as_completed(jobs):
        game, name, status = await coro
        done += 1
        if status == "skip":
            skips += 1
        elif status != "ok":
            fails += 1
            print(f"  ✗ {game}/{name}: {status}")
        if done % 25 == 0:
            print(f"  progress: {done}/{len(jobs)} (skipped {skips}, failed {fails})", flush=True)
    print(f"\nFinished: {done}/{len(jobs)}, skipped {skips}, failures {fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
