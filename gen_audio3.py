"""
Parallel audio generation for 5 new reading games.
Voice: en-US-AvaNeural.
Usage: python3 gen_audio3.py
"""
import asyncio
from pathlib import Path
import edge_tts

VOICE = "en-US-AvaNeural"
BASE = Path(__file__).parent / "v2" / "reading-zone" / "audio"

# ── Shared banner-style clips every game uses ──
def base_clips(start_text, complete_text):
    return {
        "start": start_text,
        "complete": complete_text,
        "correct1": "Yes!",
        "correct2": "Well done!",
        "correct3": "Brilliant!",
        "wrong1": "Try again!",
        "wrong2": "Almost!",
    }

# ── Game 1: First Sound ──
first_sound = {
    **base_clips(
        "Listen to the word. Tap the letter it starts with!",
        "Amazing! You found every first sound!"
    ),
    "what_starts": "What does it start with?",
    "great_ear":   "You have a great ear!",
    "super":       "Super listener!",
    # 10 words + their first letters
    "word_cat": "Cat", "word_dog": "Dog", "word_sun": "Sun",
    "word_hat": "Hat", "word_bus": "Bus", "word_pig": "Pig",
    "word_fox": "Fox", "word_mom": "Mom", "word_web": "Web",
    "word_top": "Top",
    # phoneme sounds — quick repeated sound
    "snd_c": "Cuh, cuh",
    "snd_d": "Duh, duh",
    "snd_s": "Sss, sss",
    "snd_h": "Huh, huh",
    "snd_b": "Buh, buh",
    "snd_p": "Puh, puh",
    "snd_f": "Fuh, fuh",
    "snd_m": "Mmm, mmm",
    "snd_w": "Wuh, wuh",
    "snd_t": "Tuh, tuh",
}

# ── Game 2: Last Sound ──
last_sound = {
    **base_clips(
        "Listen to the word. Tap the letter it ends with!",
        "Fantastic! You got every last sound!"
    ),
    "what_ends":   "What does it end with?",
    "sharp_ears":  "Sharp ears!",
    "super":       "You rock!",
    # 10 words, varied ending letters
    "word_cat": "Cat", "word_dog": "Dog", "word_sun": "Sun",
    "word_bus": "Bus", "word_pig": "Pig", "word_fox": "Fox",
    "word_pen": "Pen", "word_top": "Top", "word_web": "Web",
    "word_bug": "Bug",
    # ending sounds
    "snd_t": "Tuh",
    "snd_g": "Guh",
    "snd_n": "Nnn",
    "snd_s": "Sss",
    "snd_x": "Ksss",
    "snd_p": "Puh",
    "snd_b": "Buh",
}

# ── Game 3: Match Case ──
match_case = {
    **base_clips(
        "Find the partner letter! Match big and small.",
        "Wonderful! Every letter found its partner!"
    ),
    "find_partner": "Find the partner!",
    "match_them":   "Match them up!",
    "excellent":    "Excellent matching!",
    # 12 letters — named (voice says the letter name)
    "let_a": "A", "let_b": "B", "let_d": "D", "let_e": "E",
    "let_g": "G", "let_k": "K", "let_m": "M", "let_p": "P",
    "let_r": "R", "let_s": "S", "let_t": "T", "let_n": "N",
}

# ── Game 4: Alphabet Ladder ──
alphabet_ladder = {
    **base_clips(
        "Climb the alphabet ladder! Tap what comes next.",
        "You climbed all the way to the top!"
    ),
    "what_next":    "What comes next?",
    "climb_up":     "Keep climbing!",
    "almost_top":   "Almost to the top!",
    "to_the_top":   "All the way to the top!",
    # letters A through L (11 rungs, pick from these)
    "let_a": "A", "let_b": "B", "let_c": "C", "let_d": "D",
    "let_e": "E", "let_f": "F", "let_g": "G", "let_h": "H",
    "let_i": "I", "let_j": "J", "let_k": "K", "let_l": "L",
    # prompt variations
    "after_a": "What comes after A?",
    "after_b": "What comes after B?",
    "after_c": "What comes after C?",
    "after_d": "What comes after D?",
    "after_e": "What comes after E?",
    "after_f": "What comes after F?",
    "after_g": "What comes after G?",
    "after_h": "What comes after H?",
    "after_i": "What comes after I?",
    "after_j": "What comes after J?",
    "after_k": "What comes after K?",
}

# ── Game 5: Spot the Word ──
spot_the_word = {
    **base_clips(
        "Spot the word you hear! Listen and find.",
        "Brilliant reading! You spotted every word!"
    ),
    "find_the_word":  "Find the word!",
    "super_reader":   "Super reader!",
    "eagle_eye":      "Eagle eye!",
    # CVC words
    "word_cat": "Cat", "word_mat": "Mat", "word_sat": "Sat",
    "word_bat": "Bat", "word_pan": "Pan", "word_man": "Man",
    "word_fan": "Fan", "word_pig": "Pig", "word_big": "Big",
    "word_dig": "Dig", "word_sun": "Sun", "word_fun": "Fun",
    "word_run": "Run", "word_dog": "Dog", "word_log": "Log",
    "word_hop": "Hop", "word_top": "Top", "word_mop": "Mop",
}

GAMES = {
    "first-sound":     first_sound,
    "last-sound":      last_sound,
    "match-case":      match_case,
    "alphabet-ladder": alphabet_ladder,
    "spot-the-word":   spot_the_word,
}

async def gen_one(sem, game, name, text):
    out = BASE / game / f"{name}.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0:
        return ("skip", out)
    async with sem:
        try:
            comm = edge_tts.Communicate(text, VOICE)
            await comm.save(str(out))
            return ("ok", out)
        except Exception as e:
            return ("err", f"{out}: {e}")

async def main():
    sem = asyncio.Semaphore(10)
    tasks = []
    for game, clips in GAMES.items():
        for name, text in clips.items():
            tasks.append(gen_one(sem, game, name, text))
    results = await asyncio.gather(*tasks)
    ok = sum(1 for r in results if r[0] == "ok")
    sk = sum(1 for r in results if r[0] == "skip")
    er = [r for r in results if r[0] == "err"]
    print(f"Finished: {ok}/{len(results)}, skipped {sk}, failures {len(er)}")
    for e in er[:5]:
        print("ERR:", e[1])

if __name__ == "__main__":
    asyncio.run(main())
