# Open your $EDITOR to compose a message in weechat
#
# Usage:
# /edit
#
# Optional settings:
# /set plugins.var.python.edit.editor "vim -f"
#
# History:
# 10-18-2015
# Version 1.0.1: Add configurable editor key
# Version 1.0.0: initial release

import os
import os.path
import subprocess
import weechat


def edit(data, current_buffer, args):
    data = decode_from_utf8(data)
    args = decode_from_utf8(args)
    e = EVENTROUTER
    team = e.weechat_controller.buffers[current_buffer].team
    args = args.split(' ')
    extension = "md"
    backticks = False
    channel = e.weechat_controller.buffers[current_buffer]
    if len(args) > 1:
        if args[1].startswith('#'):
            channel = team.channels[team.get_channel_map()[args[1][1:]]]
        else:
            extension = args[1]
            backticks = True
            if len(args) > 2 and args[2].startswith('#'):
                channel = team.channels[team.get_channel_map()[args[2][1:]]]

    editor = (weechat.config_get_plugin("editor") or
              os.environ.get("EDITOR", "vim -f"))
    path = os.path.expanduser("~/.weechat/slack_edit." + extension)
    open(path, "w+")

    cmd = editor.split() + [path]
    code = subprocess.Popen(cmd).wait()
    if code != 0:
        os.remove(path)
        weechat.command(current_buffer, "/window refresh")
        return weechat.WEECHAT_RC_ERROR

    with open(path) as f:
        text = f.read()
        if backticks:
            text = "```\n" + text.strip() + "\n```"
        channel.send_message(text)

    os.remove(path)
    weechat.command(current_buffer, "/window refresh")

    return weechat.WEECHAT_RC_OK


def main():
    if not weechat.register("edit", "Keith Smiley", "1.0.0", "MIT",
                            "Open your $EDITOR to compose a message", "", ""):
        return weechat.WEECHAT_RC_ERROR

    weechat.hook_command("edit", "Open your $EDITOR to compose a message", "",
                         "", "", "edit", "")

if __name__ == "__main__":
    main()
