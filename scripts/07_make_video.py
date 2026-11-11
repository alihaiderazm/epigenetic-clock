"""Step 7: build the narrated progress-update video from video/slides.json.

Run:  .venv\\Scripts\\python.exe -I scripts\\07_make_video.py
Needs: ffmpeg on PATH, Windows (System.Speech text-to-speech).
Output: video/slides/*.png, video/narration_script.md, video/progress_update.mp4

To use your own voices instead: record one audio file per slide as video/_build/audio_XX.wav
(XX = 01, 02, ...) and run with --keep-audio.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import textwrap
import wave

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
VID = ROOT / "video"
SLIDES = VID / "slides"
BUILD = VID / "_build"
MAX_SECONDS = 300
PAUSE = 0.8
VOICE = "Microsoft Zira Desktop"

INK, INK2, MUTED, SURFACE, ACCENT, ACCENT2 = "#0b0b0b", "#52514e", "#898781", "#fcfcfb", "#2a78d6", "#eb6834"
plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]


def render_slide(i: int, n: int, s: dict, out: Path) -> None:
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=SURFACE)
    fig.add_artist(plt.Rectangle((0, 0.985), 1, 0.015, color=ACCENT, transform=fig.transFigure))
    fig.text(0.97, 0.03, f"Neural Ninjas · Phase I · {i}/{n}", ha="right", color=MUTED, fontsize=14)

    if s.get("kind") == "title":
        fig.text(0.06, 0.62, "\n".join(textwrap.wrap(s["title"], 40)), fontsize=54, fontweight="bold", color=INK, va="bottom")
        for k, b in enumerate(s["bullets"]):
            fig.text(0.06, 0.50 - k * 0.075, b, fontsize=26, color=INK2 if k > 1 else INK)
    else:
        fig.text(0.05, 0.89, s["title"], fontsize=40, fontweight="bold", color=INK)
        img = s.get("image")
        width = 34 if img else 70
        y = 0.78
        for b in s.get("bullets", []):
            lines = textwrap.wrap(b, width)
            color = ACCENT2 if b.startswith("TODO") else INK2
            fig.text(0.05, y, "•", fontsize=24, color=ACCENT, va="top", linespacing=1.35)
            fig.text(0.075, y, "\n".join(lines), fontsize=24, color=color, va="top", linespacing=1.35)
            y -= 0.055 * len(lines) + 0.035
        if img:
            ax = fig.add_axes([0.40, 0.07, 0.57, 0.78])
            im = mpimg.imread(ROOT / img)
            if "crop" in s:
                x0, y0, x1, y1 = s["crop"]
                im = im[y0:y1, x0:x1]
            ax.imshow(im)
            ax.axis("off")
    fig.savefig(out, dpi=100, facecolor=SURFACE)
    plt.close(fig)


def speak(text: str, wav: Path) -> None:
    txt = wav.with_suffix(".txt")
    txt.write_text(text, encoding="utf-8")
    ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.SelectVoice('{VOICE}'); $s.Rate = 0; $s.SetOutputToWaveFile('{wav}'); "
          f"$s.Speak([IO.File]::ReadAllText('{txt}')); $s.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def seconds(wav: Path) -> float:
    with wave.open(str(wav)) as w:
        return w.getnframes() / w.getframerate()


def main() -> None:
    ffmpeg = shutil.which("ffmpeg") or sys.exit("ffmpeg not found on PATH")
    keep_audio = "--keep-audio" in sys.argv
    slides = json.loads((VID / "slides.json").read_text(encoding="utf-8"))
    SLIDES.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)

    segments, total, script = [], 0.0, ["# Narration script\n", "Read aloud one paragraph per slide (generated from video/slides.json).\n"]
    for i, s in enumerate(slides, 1):
        png, wav, seg = SLIDES / f"slide_{i:02d}.png", BUILD / f"audio_{i:02d}.wav", BUILD / f"seg_{i:02d}.mp4"
        render_slide(i, len(slides), s, png)
        if not (keep_audio and wav.exists()):
            speak(s["narration"], wav)
        dur = seconds(wav) + PAUSE
        total += dur
        script.append(f"\n## Slide {i}: {s['title']}  (~{dur:.0f} s)\n\n{s['narration']}\n")
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-i", str(wav),
                        "-af", f"apad=pad_dur={PAUSE}", "-t", f"{dur:.3f}", "-r", "25",
                        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", str(seg)], check=True)
        segments.append(seg)
        print(f"slide {i:2d}: {dur:5.1f} s  {s['title']}")

    lst = BUILD / "segments.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
    out = VID / "progress_update.mp4"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], check=True)
    (VID / "narration_script.md").write_text("".join(script), encoding="utf-8")
    print(f"total {total:.0f} s ({total / 60:.1f} min) -> {out}")
    if total > MAX_SECONDS:
        print(f"WARNING: longer than the {MAX_SECONDS} s limit, shorten the narration")


if __name__ == "__main__":
    main()
