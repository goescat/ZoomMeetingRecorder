import subprocess

def in_meeting():
    script = '''
    tell application "System Events"
        if exists process "zoom.us" then
            tell process "zoom.us"
                return name of every window
            end tell
        end if
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )

    windows = result.stdout.lower()

    keywords = [
        "meeting",
        "zoom meeting",
    ]

    return any(k in windows for k in keywords)