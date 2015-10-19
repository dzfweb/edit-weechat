# Open your $EDITOR to compose a message in weechat
#
# Usage:
# /edit
#
# History:
# 10-18-2015
# Version 1.0.0: initial release

import os
import os.path
import subprocess
import weechat


def edit(data, buf, args):
    editor = os.environ.get("EDITOR", "vim")
    path = os.path.expanduser("~/.weechat/message.txt")
    open(path, "w+")

    cmd = [editor, path]
    code = subprocess.Popen(cmd).wait()
    if code != 0:
        os.remove(path)
        weechat.command(buf, "/window refresh")
        return weechat.WEECHAT_RC_ERROR

    with open(path) as f:
        text = f.read()
        weechat.buffer_set(buf, "input", text)
        weechat.buffer_set(buf, "input_pos", str(len(text)))

    os.remove(path)
    weechat.command(buf, "/window refresh")

    return weechat.WEECHAT_RC_OK


def main():
    if not weechat.register("edit", "Keith Smiley", "1.0.0", "MIT",
                            "Open your $EDITOR to compose a message", "", ""):
        return weechat.WEECHAT_RC_ERROR

    weechat.hook_command("edit", "Open your $EDITOR to compose a message", "",
                         "", "", "edit", "")

if __name__ == "__main__":
    main()
