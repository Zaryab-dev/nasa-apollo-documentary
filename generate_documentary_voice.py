#!/usr/bin/env python3
"""
Breeze-TTS-2 Documentary Voice CLI Generator
Supports zero-shot Voice Design and Reference Voice Cloning & Direction (Zack D. Films 1.20x Master).
Designed for Kaggle T4 GPU / Local GPU Linux environments.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DOCUMENTARY_PROFILES = {
    "zaryab_voice": {
        "type": "design",
        "description": "A compelling, charismatic 30-year-old male narrator with a warm, grounded baritone voice, delivering dramatic documentary history with fast, forward-moving momentum, articulate diction, sharp consonants, and subtle suspense.",
        "tempo": 0.94,
        "seed": 101,
        "cfg_scale": 4.5,
    },
    "zackd_studio_master": {
        "type": "clone",
        "description": "Zack D. Films crisp, articulate narrator with 1.25x pitch-preserved tempo boost and broadcast mastering",
        "ref_audio": "voice_profiles/zackd_studio_master/ref_audio.wav",
        "ref_text": "If Alcatraz had cold showers just like in a normal prison, the prisoners would slowly get used to the cold. And this meant they could jump into the water around the island, surviving the low temperatures and swimming to freedom.",
        "tempo": 1.25,
    },
    "classic_historian": {
        "type": "design",
        "description": "A mature, deep, resonant male baritone with calm, authoritative pacing, steady breath control, warm acoustic presence, and cinematic gravitas, speaking like a seasoned historical documentary narrator.",
        "tempo": 1.0,
    },
    "cosmic_wonder": {
        "type": "design",
        "description": "A warm, articulate, middle-aged male voice with an engaging, inquisitive cadence, clear enunciation, thoughtful pauses, and a subtle sense of wonder and reverence, ideal for a science and space exploration documentary.",
        "tempo": 1.0,
    },
    "investigative_alto": {
        "type": "design",
        "description": "A composed, articulate female narrator with a rich, velvety alto timbre, steady and deliberate cadence, restrained emotion, and crisp diction, conveying historical authority and depth.",
        "tempo": 1.0,
    },
    "mission_director": {
        "type": "design",
        "description": "A focused, middle-aged American male voice with calm discipline, firm clarity, measured cadence, and an urgent undercurrent, reminiscent of a 1960s NASA flight controller.",
        "tempo": 1.0,
    },
}

DEFAULT_APOLLO_SCRIPT = (
    "On July 16, 1969, three men sat atop a three-hundred-and-sixty-three-foot tower of steel and liquid fire. "
    "Behind them stood four hundred thousand engineers, technicians, and seamstresses who had built the machine "
    "that would carry humanity to the surface of the Moon. "
    "This was not merely a rocket. It was the greatest technological gamble in human history."
)


def apply_mastering(input_wav: str, output_wav: str, tempo: float = 1.20):
    """Applies pitch-preserved tempo acceleration and EBU R128 loudness normalization."""
    print(f"🎛️ Mastering audio: tempo={tempo}x, broadcast loudnorm (target LUFS: -16)...")
    filter_chain = f"atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=11" if tempo != 1.0 else "loudnorm=I=-16:TP=-1.5:LRA=11"
    temp_target = output_wav if input_wav != output_wav else output_wav.replace(".wav", "_mastered.wav")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_wav,
        "-filter:a", filter_chain,
        "-ar", "24000",
        "-ac", "1",
        temp_target,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if temp_target != output_wav:
        os.replace(temp_target, output_wav)
    print(f"✅ Mastered audio finalized at: {output_wav}")


def main():
    parser = argparse.ArgumentParser(description="Generate documentary voice narration with Breeze-TTS-2")
    parser.add_argument(
        "--model-dir",
        type=str,
        default="/kaggle/working/Breeze-TTS-2",
        help="Path to downloaded Breeze-TTS-2 weights",
    )
    parser.add_argument(
        "--breeze-repo",
        type=str,
        default="/kaggle/working/breeze-tts",
        help="Path to cloned breeze-tts inference repository",
    )
    parser.add_argument(
        "--profile",
        type=str,
        choices=list(DOCUMENTARY_PROFILES.keys()),
        default="zaryab_voice",
        help="Preset documentary voice persona (default: zaryab_voice)",
    )
    parser.add_argument(
        "--script-file",
        type=str,
        default=None,
        help="Path to a text file containing the narration script",
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="Inline documentary narration script (used if --script-file is not specified)",
    )
    parser.add_argument(
        "--tempo",
        type=float,
        default=None,
        help="Pacing tempo multiplier (default: 1.20 for zackd_studio_master)",
    )
    parser.add_argument(
        "--cfg-scale",
        type=float,
        default=4.0,
        help="Classifier-free guidance scale (recommended: 4.0 - 4.5)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for deterministic voice timbre generation",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="/kaggle/working/outputs/narration_output.wav",
        help="Output WAV destination path",
    )

    args = parser.parse_args()

    # Resolve narration text
    if args.script_file and os.path.exists(args.script_file):
        with open(args.script_file, "r", encoding="utf-8") as f:
            narration_text = f.read().strip()
    elif args.text:
        narration_text = args.text.strip()
    else:
        narration_text = DEFAULT_APOLLO_SCRIPT

    profile_cfg = DOCUMENTARY_PROFILES[args.profile]
    tempo = args.tempo if args.tempo is not None else profile_cfg.get("tempo", 1.0)

    print("=" * 60)
    print("🎙️ Breeze-TTS-2 Documentary Voice Production Engine")
    print("=" * 60)
    print(f"📌 Profile: {args.profile}")
    print(f"📝 Script Length: {len(narration_text)} characters ({len(narration_text.split())} words)")
    print(f"⚡ Target Tempo: {tempo}x (Pitch Preserved)")
    print(f"💾 Destination: {args.output}")

    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    infer_script = Path(args.breeze_repo) / "infer.py"
    if not infer_script.exists():
        print(f"❌ Error: infer.py not found at {infer_script}")
        sys.exit(1)

    raw_output = str(Path(args.output).with_name(f"raw_{Path(args.output).name}"))

    cmd = [
        sys.executable,
        str(infer_script),
        args.model_dir,
        "--text",
        narration_text,
        "--cfg-scale",
        str(args.cfg_scale),
        "--seed",
        str(args.seed),
        "--output",
        raw_output,
    ]

    # Handle voice cloning vs voice design
    if profile_cfg["type"] == "clone":
        ref_path = profile_cfg["ref_audio"]
        if not os.path.exists(ref_path) and os.path.exists("/kaggle/working/reference_alcatraz.wav"):
            ref_path = "/kaggle/working/reference_alcatraz.wav"
        cmd.extend([
            "--ref-audio", str(ref_path),
            "--ref-text", profile_cfg["ref_text"],
        ])
    else:
        cmd.extend(["--instruction", profile_cfg["description"]])

    print(f"\n🚀 Running TTS Synthesis on GPU...")
    proc = subprocess.run(cmd, cwd=args.breeze_repo)

    if proc.returncode != 0 or not os.path.exists(raw_output):
        print(f"\n❌ Synthesis failed with exit code {proc.returncode}")
        sys.exit(1)

    # Apply 1.20x tempo & studio mastering
    apply_mastering(raw_output, args.output, tempo=tempo)
    if os.path.exists(raw_output) and raw_output != args.output:
        os.remove(raw_output)

    file_size_kb = os.path.getsize(args.output) / 1024
    print(f"\n🎉 Production Narration Ready: {args.output} ({file_size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
