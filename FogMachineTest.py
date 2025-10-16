"""Interactive DMX test REPL.

Run this module to interactively set DMX channel levels.
Commands:
  set <channel> <value>   # channel: 1-512, value: 0-255
  get <channel>           # read back the last value we sent for a channel
  on <channel> [value]    # default value 255
  off <channel>           # set channel to 0
  blackout                # set all channels to 0
  help                    # show commands
  quit | exit | q         # exit
"""

from DMXController import DMXController


def print_help():
    print("Commands:")
    print("  set <channel> <value>   # channel: 1-512, value: 0-255")
    print("  get <channel>           # read back last value we sent")
    print("  on <channel> [value]    # default 255 if value omitted")
    print("  off <channel>           # set channel to 0")
    print("  blackout                # set all channels to 0")
    print("  help                    # show this help")
    print("  quit | exit | q         # exit")


def main():
    controller = DMXController()
    print("Interactive DMX test. Type 'help' for commands. Press Ctrl+C or 'q' to quit.")

    try:
        while True:
            try:
                line = input("dmx> ").strip()
            except EOFError:
                break

            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()

            if cmd in ("quit", "exit", "q"):
                break
            if cmd == "help":
                print_help()
                continue
            if cmd == "blackout":
                controller.blackout()
                print("All channels set to 0.")
                continue
            if cmd == "get":
                if len(parts) != 2:
                    print("Usage: get <channel>")
                    continue
                try:
                    channel = int(parts[1])
                    value = controller.get_channel(channel)
                    print(f"Channel {channel} = {value}")
                except Exception as exc:
                    print(f"Error: {exc}")
                continue
            if cmd == "off":
                if len(parts) != 2:
                    print("Usage: off <channel>")
                    continue
                try:
                    channel = int(parts[1])
                    controller.set_channel(channel, 0)
                    print(f"Channel {channel} set to 0")
                except Exception as exc:
                    print(f"Error: {exc}")
                continue
            if cmd == "on":
                if len(parts) not in (2, 3):
                    print("Usage: on <channel> [value]")
                    continue
                try:
                    channel = int(parts[1])
                    value = int(parts[2]) if len(parts) == 3 else 255
                    controller.set_channel(channel, value)
                    print(f"Channel {channel} set to {value}")
                except Exception as exc:
                    print(f"Error: {exc}")
                continue
            if cmd == "set":
                if len(parts) != 3:
                    print("Usage: set <channel> <value>")
                    continue
                try:
                    channel = int(parts[1])
                    value = int(parts[2])
                    controller.set_channel(channel, value)
                    print(f"Channel {channel} set to {value}")
                except Exception as exc:
                    print(f"Error: {exc}")
                continue

            print("Unknown command. Type 'help' for a list of commands.")
    except KeyboardInterrupt:
        pass
    finally:
        try:
            controller.blackout()
        except Exception:
            pass
        controller.stop()
        print("Exiting.")


if __name__ == "__main__":
    main()

