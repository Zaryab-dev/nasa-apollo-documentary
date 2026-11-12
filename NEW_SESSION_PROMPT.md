# 📋 Copy-Paste Prompt for New Sessions

Copy and paste the entire block below into a new chat session to instantly resume your documentary narration workflow:

```markdown
Hi! I want to generate narration for my documentary video using my custom voice **"Zaryab-Voice"** powered by Breeze-TTS-2 on Kaggle GPU T4.

### 🔑 Credentials & Environment Setup
Please ensure Kaggle CLI is authenticated using:
- **Kaggle Username:** `zaryabofficial`
- **Kaggle API Key:** `KGAT_9b26adaadb1b25daea372d8ebe7ac191`
Ensure `~/.kaggle/kaggle.json` exists with permissions `600`:
`{"username":"zaryabofficial","key":"KGAT_9b26adaadb1b25daea372d8ebe7ac191"}`

### 📁 Workspace & Voice DNA
- **Project Directory:** `/home/antigravity/Zaryab-dev/nasa-apollo-documentary`
- **Voice Name:** `Zaryab-Voice` (Cinematic Investigative Storyteller)
- **Voice Profile Path:** `/home/antigravity/Zaryab-dev/nasa-apollo-documentary/voice_profiles/zaryab_voice/`
- **Vocal Persona:** 30yo charismatic American male baritone, subtle suspense, razor-sharp diction, spacious atmospheric pauses (Lemmino / MagnatesMedia documentary feel).
- **Core Parameters:** Seed `101`, CFG Scale `4.5`, Tempo `0.94x` (Deliberate Suspense), Sample Rate `24000Hz` Mono, Broadcast Loudness `-16 LUFS`.
- **Kaggle Kernel ID:** `zaryabofficial/breeze-tts-2-documentary-voice-generation`
- **Automated Runner Script:** `/home/antigravity/Zaryab-dev/nasa-apollo-documentary/render_video_narration.py`

---

### 📝 My New Video Script / Task:
[PASTE YOUR NEW SCRIPT OR INSTRUCTIONS HERE, e.g.:]
"Three miles below the surface of the Pacific Ocean lies a secret that naval engineers spent fifty years trying to hide..."

Please run `render_video_narration.py` to synthesize this on Kaggle GPU T4 using Zaryab-Voice, download the resulting audio to `outputs/`, make sure the GPU session terminates, and embed an in-memory Base64 audio player so I can listen to and download the final master take.
```
