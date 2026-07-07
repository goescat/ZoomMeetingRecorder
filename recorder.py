import os
import signal
import subprocess
import datetime

process = None

FFMPEG = "/opt/homebrew/bin/ffmpeg"


def is_recording():
    global process
    return process is not None and process.poll() is None


def start():
    global process

    if is_recording():
        return

    os.makedirs("recordings", exist_ok=True)

    filename = datetime.datetime.now().strftime(
        "recordings/%Y-%m-%d_%H-%M-%S.mp4"
    )

    cmd = [
        FFMPEG,

        "-hide_banner",
        "-loglevel", "warning",

        "-y",

        "-thread_queue_size", "2048",

        "-f", "avfoundation",
        "-framerate", "30",
        "-pixel_format", "bgr0",
        "-capture_cursor", "1",
        "-i", "2:1",

        "-vf", "scale=1920:-2",

        "-c:v", "h264_videotoolbox",

        "-b:v", "3000k",
        "-maxrate", "3500k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-realtime", "1",

        "-c:a", "aac_at",
        "-ar", "48000",
        "-b:a", "192k",

        filename,
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    print(f"開始錄影：{filename}")


def stop():
    global process

    if process is None:
        return

    if process.poll() is not None:
        print("ffmpeg 已經結束")
        process = None
        return

    print("停止錄影")

    try:

        print("Sending q...")
        process.stdin.write("q\n")
        process.stdin.flush()

        print("Waiting ffmpeg...")
        process.wait()

        print(f"ffmpeg exited: {process.returncode}")

        if process.stderr:
            err = process.stderr.read()
            if err.strip():
                print("===== ffmpeg stderr =====")
                print(err)
                print("=========================")

    except Exception as e:

        print("Error while stopping:", e)

        try:
            process.send_signal(signal.SIGINT)
            process.wait(timeout=5)

        except Exception:

            process.kill()

    finally:

        process = None
