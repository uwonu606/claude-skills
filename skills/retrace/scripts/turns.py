import argparse
import glob
import json
import os
import re
from datetime import datetime

SKILL_BODY_PREFIX = "Base directory for this skill:"
COMMAND_NAME = re.compile(r"<command-name>(.*?)</command-name>", re.S)
COMMAND_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)


def local_time(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone()


def message_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text")
    return ""


def as_user_turn(record):
    if record.get("type") != "user" or record.get("isSidechain") or record.get("isMeta"):
        return None
    text = message_text(record.get("message", {}).get("content")).strip()
    if not text or text.startswith(SKILL_BODY_PREFIX) or text.startswith("<local-command"):
        return None
    name = COMMAND_NAME.search(text)
    if name:
        args = COMMAND_ARGS.search(text)
        text = f"{name.group(1)} {args.group(1).strip() if args else ''}".strip()
    return text


def as_assistant_turn(record):
    if record.get("type") != "assistant" or record.get("isSidechain"):
        return None
    return message_text(record.get("message", {}).get("content")).strip() or None


def read_session(path):
    turns = []
    for line in open(path, encoding="utf-8"):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        timestamp = record.get("timestamp")
        if not timestamp:
            continue
        user_text = as_user_turn(record)
        if user_text:
            turns.append(("U", local_time(timestamp), user_text))
            continue
        assistant_text = as_assistant_turn(record)
        if assistant_text:
            turns.append(("A", local_time(timestamp), assistant_text))
    return turns


def sessions(directory):
    found = []
    for path in glob.glob(os.path.join(directory, "*.jsonl")):
        turns = read_session(path)
        if turns:
            found.append((turns[0][1], os.path.basename(path)[:8], turns))
    return sorted(found)


def stamp(moment):
    return moment.strftime("%m-%d %H:%M")


def print_user_turns(directory, width):
    found = sessions(directory)
    zone = found[0][0].strftime("%Z") if found else ""
    print(f"# times in {zone}")
    for started, session_id, turns in found:
        users = [turn for turn in turns if turn[0] == "U"]
        print(f"\n## {session_id} {started.strftime('%Y-%m-%d %H:%M')} ({len(users)} user turns)")
        for _, moment, text in users:
            print(f"[{stamp(moment)}] {session_id} | {text.replace(chr(10), ' / ')[:width]}")


def print_around(directory, session_id, pattern, before, after, width):
    path = glob.glob(os.path.join(directory, session_id + "*.jsonl"))[0]
    turns = read_session(path)
    for index, (role, _, text) in enumerate(turns):
        if role == "U" and pattern in text:
            for role_near, moment, text_near in turns[max(0, index - before): index + after + 1]:
                print(f"--- {role_near} [{stamp(moment)} {moment.strftime('%Z')}] {session_id}\n{text_near[:width]}\n")
            return
    print(f"no user turn in {session_id} contains {pattern!r}")


def main():
    parser = argparse.ArgumentParser(description="Claude Code session transcripts as timestamped turns in local time.")
    sub = parser.add_subparsers(dest="command", required=True)
    users = sub.add_parser("users", help="every user turn of every session, oldest session first")
    users.add_argument("directory")
    users.add_argument("--width", type=int, default=600)
    around = sub.add_parser("around", help="turns around the first user turn containing PATTERN")
    around.add_argument("directory")
    around.add_argument("session_id")
    around.add_argument("pattern")
    around.add_argument("--before", type=int, default=1)
    around.add_argument("--after", type=int, default=2)
    around.add_argument("--width", type=int, default=2000)
    args = parser.parse_args()
    if args.command == "users":
        print_user_turns(args.directory, args.width)
    else:
        print_around(args.directory, args.session_id, args.pattern, args.before, args.after, args.width)


if __name__ == "__main__":
    main()
