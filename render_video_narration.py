#!/usr/bin/env python3
"""
🚀 Automated Video Narration Production Runner: Zaryab-Voice
Generates broadcast-ready documentary voiceover using the official "Zaryab-Voice":
Cinematic Investigative Storyteller (Deliberate Suspense, 0.94x tempo).
Powered by Breeze-TTS-2 on Kaggle GPU T4.

Usage:
  python render_video_narration.py --text "Your documentary script here..." --output episode_1.wav
  python render_video_narration.py --file script.txt --output episode_1_full.wav
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent
KERNEL_DIR = Path("/home/antigravity/kaggle_kernel")
OUTPUTS_DIR = WORKSPACE_DIR / "outputs"
VOICE_PROFILE_DIR = WORKSPACE_DIR / "voice_profiles" / "zaryab_voice"

KAGGLE_BIN = Path("/home/antigravity/.local/bin/kaggle")
KERNEL_ID = "zaryabofficial/breeze-tts-2-documentary-voice-generation"

ZARYAB_VOICE_INSTRUCTION = (
    "A compelling, charismatic 30-year-old male narrator with a warm, grounded baritone voice, "
    "delivering dramatic documentary history with fast, forward-moving momentum, articulate diction, "
    "sharp consonants, and subtle suspense."
)


def build_kaggle_notebook(script_text: str, tempo: float = 0.94, seed: int = 101, cfg_scale: float = 4.5) -> Path:
    """Builds a self-contained Kaggle notebook configured with the user's script and Zaryab-Voice."""

    def make_cell(cell_type, text):
        lines = [line + "\n" for line in text.split("\n")]
        if lines:
            lines[-1] = lines[-1].rstrip("\n")
        cell = {"cell_type": cell_type, "metadata": {}, "source": lines}
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        return cell

    c1 = """# Step 1: Dependencies
import os, subprocess, sys
os.makedirs("/kaggle/working", exist_ok=True)
if not os.path.exists("/content"):
    try: os.symlink("/kaggle/working", "/content")
    except Exception: pass
subprocess.run(["apt-get", "update", "-qq"], check=False)
subprocess.run(["apt-get", "install", "-y", "-qq", "sox", "libsox-fmt-all", "aria2", "ffmpeg"], check=False)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "uv"], check=True)
breeze_repo = "/kaggle/working/breeze-tts"
if not os.path.exists(breeze_repo):
    subprocess.run(["git", "clone", "-q", "https://github.com/breezeblue-ai/breeze-tts.git", breeze_repo], check=True)
subprocess.run(["uv", "pip", "install", "--system", "--quiet", "sox", "flask", "flask-cors", "pydub", "huggingface_hub", "soundfile", "openai-whisper", "qwen-tts", "einops"], check=True)
subprocess.run(["pip", "uninstall", "-y", "-q", "torchvision"], check=False)
print("✅ Dependencies ready!")"""

    c2 = """# Step 2: Download Model & Compatibility Shim
import os, sys, re
from huggingface_hub import snapshot_download

MODEL_DIR = "/kaggle/working/Breeze-TTS-2"
OUTPUT_DIR = "/kaggle/working/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

infer_path = "/kaggle/working/breeze-tts/infer.py"
if os.path.exists(infer_path):
    with open(infer_path, "r") as f: content = f.read()
    if "no_init_weights" not in content:
        shim = "\\n".join([
            "import transformers.modeling_utils",
            "try:",
            "    from transformers.initialization import no_init_weights",
            "    transformers.modeling_utils.no_init_weights = no_init_weights",
            "except ImportError:",
            "    from contextlib import contextmanager",
            "    @contextmanager",
            "    def _dummy(*a, **k): yield",
            "    transformers.modeling_utils.no_init_weights = _dummy",
            ""
        ])
        if "from __future__ import annotations" in content:
            content = content.replace("from __future__ import annotations", "from __future__ import annotations\\n" + shim, 1)
        else:
            content = shim + "\\n" + content
        with open(infer_path, "w") as f: f.write(content)

cfg_path = "/kaggle/working/breeze-tts/models/breeze_config.py"
if os.path.exists(cfg_path):
    with open(cfg_path, "r") as f: cfg = f.read()
    cfg = re.sub(r"AutoConfig\\.register\\((.*?)\\)", lambda m: m.group(0) if "exist_ok" in m.group(1) else f"AutoConfig.register({m.group(1)}, exist_ok=True)", cfg)
    with open(cfg_path, "w") as f: f.write(cfg)

print("📥 Checking/Downloading Breeze-TTS-2 weights...")
snapshot_download(repo_id="BreezeBlue/Breeze-TTS-2", local_dir=MODEL_DIR)
print("✅ Model weights ready!")"""

    safe_script = json.dumps(script_text)
    safe_instruction = json.dumps(ZARYAB_VOICE_INSTRUCTION)

    c3 = f"""# Step 3: Synthesize Zaryab-Voice & Apply Studio Mastering
import os, subprocess, sys

SCRIPT_TEXT = {safe_script}
INSTRUCTION = {safe_instruction}

breeze_repo = "/kaggle/working/breeze-tts"
model_dir = "/kaggle/working/Breeze-TTS-2"
raw_wav = "/kaggle/working/outputs/raw_narration.wav"
master_wav = "/kaggle/working/outputs/zaryab_voice_master.wav"

cmd = [
    sys.executable, "infer.py", model_dir,
    "--text", SCRIPT_TEXT,
    "--instruction", INSTRUCTION,
    "--cfg-scale", "{cfg_scale}",
    "--seed", "{seed}",
    "--output", raw_wav,
]

print("🚀 Synthesizing narration with Zaryab-Voice on GPU...")
subprocess.run(cmd, cwd=breeze_repo, check=True)

print("🎛️ Mastering audio: {tempo}x deliberate suspense + broadcast loudness normalization...")
subprocess.run([
    "ffmpeg", "-y", "-i", raw_wav,
    "-filter:a", "atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11",
    "-ar", "24000", "-ac", "1",
    master_wav
], check=True)

if os.path.exists(raw_wav):
    os.remove(raw_wav)

print("🎉 Zaryab-Voice Master complete:", master_wav)
"""

    nb = {
        "cells": [
            make_cell("markdown", "# 🎙️ Zaryab-Voice Documentary Production Runner"),
            make_cell("code", c1),
            make_cell("code", c2),
            make_cell("code", c3),
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.12"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    target = KERNEL_DIR / "Breeze_TTS_2_Kaggle_Documentary.ipynb"
    with open(target, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)

    return target


def main():
    parser = argparse.ArgumentParser(description="Render documentary narration using official Zaryab-Voice")
    parser.add_argument("--text", type=str, default=None, help="Documentary script text string")
    parser.add_argument("--file", type=str, default=None, help="Path to text file containing documentary script")
    parser.add_argument("--tempo", type=float, default=0.94, help="Tempo multiplier (default: 0.94 Deliberate Suspense)")
    parser.add_argument("--seed", type=int, default=101, help="Seed for Zaryab-Voice (default: 101)")
    parser.add_argument("--output", type=str, default="zaryab_voice_narration.wav", help="Output filename inside outputs/")

    args = parser.parse_args()

    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            script_text = f.read().strip()
    elif args.text:
        script_text = args.text.strip()
    else:
        print("❌ Error: Please provide --text \"...\" or --file script.txt")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("🎬 ZARYAB-VOICE DOCUMENTARY PRODUCTION PIPELINE")
    print("=" * 65)
    print(f"🎙️ Official Voice: Zaryab-Voice (Cinematic Investigative Storyteller)")
    print(f"📝 Script Preview: \"{script_text[:100]}...\" ({len(script_text.split())} words)")
    print(f"⚡ Pacing: {args.tempo}x Deliberate Suspense (Pitch Preserved, -16 LUFS)")
    print(f"📁 Destination: {OUTPUTS_DIR / args.output}\n")

    # 1. Build notebook
    print("1️⃣ Packaging notebook with script and Zaryab-Voice preset...")
    build_kaggle_notebook(script_text, tempo=args.tempo, seed=args.seed)

    # 2. Push to Kaggle GPU
    print("2️⃣ Pushing to Kaggle GPU T4...")
    subprocess.run([str(KAGGLE_BIN), "kernels", "push", "-p", str(KERNEL_DIR)], check=True)

    # 3. Monitor
    print("3️⃣ Waiting for Kaggle GPU synthesis to complete...")
    start_time = time.time()
    while True:
        res = subprocess.run([str(KAGGLE_BIN), "kernels", "status", KERNEL_ID], capture_output=True, text=True)
        status_line = res.stdout.strip()
        elapsed = int(time.time() - start_time)
        print(f"   [{elapsed}s] {status_line}")
        if "COMPLETE" in status_line:
            break
        if "ERROR" in status_line or "CANCEL" in status_line:
            print("\n❌ Kernel encountered an error on Kaggle.")
            sys.exit(1)
        time.sleep(20)

    # 4. Download outputs
    print("\n4️⃣ Downloading Zaryab-Voice master audio from Kaggle...")
    dl_dir = OUTPUTS_DIR / "temp_dl"
    dl_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        str(KAGGLE_BIN), "kernels", "output", KERNEL_ID,
        "-p", str(dl_dir),
        "--file-pattern", ".*zaryab_voice_master\\.wav"
    ], check=True)

    final_src = dl_dir / "outputs" / "zaryab_voice_master.wav"
    if not final_src.exists():
        final_src = dl_dir / "zaryab_voice_master.wav"

    final_dest = OUTPUTS_DIR / args.output
    if final_src.exists():
        os.replace(final_src, final_dest)
        subprocess.run(["rm", "-rf", str(dl_dir)], check=False)
        print("\n" + "=" * 65)
        print(f"🎉 SUCCESS! Zaryab-Voice audio ready: {final_dest}")
        print(f"📦 File Size: {os.path.getsize(final_dest)/1024:.1f} KB")
        print("=" * 65)
    else:
        print("❌ Could not find downloaded zaryab_voice_master.wav")


if __name__ == "__main__":
    main()
