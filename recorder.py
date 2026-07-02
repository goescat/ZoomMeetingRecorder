import os
import subprocess
import datetime

process = None

# 如果 `which ffmpeg` 不是這個路徑，請改成你的路徑
FFMPEG = "/opt/homebrew/bin/ffmpeg"


def start():
    global process

    if process is not None and process.poll() is None:
        return

    os.makedirs("recordings", exist_ok=True)

    filename = datetime.datetime.now().strftime(
        "recordings/%Y-%m-%d_%H-%M-%S.mp4"
    )

    process = subprocess.Popen([
        FFMPEG,
        "-y",

        "-f", "avfoundation",
        "-framerate", "30",
        "-pixel_format", "bgr0",
        "-i", "2:1",

        "-vf", "scale=1920:-2",

        "-c:v", "h264_videotoolbox",
        "-b:v", "6M",

        "-c:a", "aac",
        "-b:a", "192k",

        filename
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.PIPE)

    print(f"開始錄影：{filename}")


def stop():
    global process

    if process is None:
        return

    try:
        # 正常通知 ffmpeg 結束，避免 MP4 損毀
        process.stdin.write(b"q\n")
        process.stdin.flush()

        process.wait(timeout=10)

    except Exception:
        process.kill()

    finally:
        process = None

    print("停止錄影")