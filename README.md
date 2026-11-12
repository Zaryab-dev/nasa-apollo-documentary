# 🚀 NASA Apollo Documentary: Automated Voice Production Pipeline

A complete cinematic documentary narration suite powered by **Breeze-TTS-2** running on **Kaggle GPU T4**.

---

## 🎙️ Official Channel Voice: "Zaryab-Voice"

- **Voice Name:** `Zaryab-Voice`
- **Archetype:** Cinematic Investigative Storyteller (Deliberate Suspense)
- **Vocal Persona:** Warm, grounded 30-year-old American male baritone, delivering dramatic history with subtle suspense, razor-sharp diction, and spacious, atmospheric pauses (Lemmino / MagnatesMedia documentary feel).
- **Pacing:** `0.94x` Deliberate Suspense (~19.1s for 56 words).
- **Engine Specs:** Breeze-TTS-2 Voice Design (Seed: 101, CFG: 4.5).
- **Mastering:** Broadcast EBU R128 loudness normalization (`-16 LUFS`, true peak `-1.5 dBTP`).
- **Sample Rate:** 24 kHz 16-bit Mono PCM WAV.

### Permanent Voice Profile Assets
Saved permanently in [`voice_profiles/zaryab_voice/`](voice_profiles/zaryab_voice/):
- `zaryab_voice_reference.wav`: Clean reference master of Zaryab-Voice (Apollo 11 narration).
- `zaryab_voice_reference.txt`: Exact reference transcript.
- `voice_preset.json`: Full configuration, seed, CFG, and mastering parameters.

---

## ⚡ Generating Narration for Any Video with Zaryab-Voice

Whenever you have a new video script, run one simple command:

### Option 1: Quick Line or Paragraph from Terminal
```bash
python render_video_narration.py \
  --text "Your new documentary script here..." \
  --output episode_1.wav
```

### Option 2: Full Script from a Text File
```bash
python render_video_narration.py \
  --file scripts/apollo_part1.txt \
  --output apollo_part1_master.wav
```

### Customizing Pacing on the Fly
- **Official Zaryab-Voice Default (Deliberate Suspense):** `--tempo 0.94` *(default)*
- **Natural Neural Cadence:** `--tempo 1.00`
- **Nuanced Brisk Cut:** `--tempo 1.08`
- **Fast-Paced YouTube Shorts / Hooks:** `--tempo 1.25`

---

## 📁 Flagship Output Audio
- **Flagship Track:** [`outputs/Zaryab-Voice-Apollo-Narration.wav`](outputs/Zaryab-Voice-Apollo-Narration.wav) (19.1s, -16 LUFS broadcast master).
- **Profile Preset:** [`voice_profiles/zaryab_voice/`](voice_profiles/zaryab_voice/)
- **Kaggle Kernel:** [`zaryabofficial/breeze-tts-2-documentary-voice-generation`](https://www.kaggle.com/code/zaryabofficial/breeze-tts-2-documentary-voice-generation)
