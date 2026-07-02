import subprocess


def in_meeting():
    script = r'''
    tell application "System Events"
        if not (exists process "zoom.us") then
            return false
        end if

        tell process "zoom.us"
            try
                exists menu bar item "Meeting" of menu bar 1
            on error
                false
            end try
        end tell
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip().lower() == "true"