"""Step 1: two people, one scene.

No world. No referee. No files except two hand-written self.md and secret.md
per person, under step1/people/. Two agents talk directly for six exchanges,
then each writes a private reaction. Everything prints to the terminal.

Run:   python lineage/step1.py
Needs: ANTHROPIC_API_KEY in the environment.

The goal is that it reads like two real people. If either one sounds like a
helpful assistant, an author, or a narrator, tune PASSAGE in prompts.py.
"""

import os
import sys

import anthropic

import llm
import prompts
import settings

HERE = os.path.dirname(os.path.abspath(__file__))
PEOPLE = os.path.join(HERE, "step1", "people")

SETTING = (
    "Late October, the first hard frost of the year. Dusk. The Holt farmhouse at the "
    "bottom of the valley, by the river. The kitchen: a long table, a fire burning low, "
    "a pot of something thin on it, nine sacks of grain stacked against the back wall "
    "where anyone can count them. Piet is at the neighbour's. Maren Holt is alone, "
    "mending a harness by the fire. Tobias Crane has walked down from the mill with a "
    "folded paper in his coat. He knocks once and comes in without waiting."
)

FIRST = ("maren", "Maren")    # speaks first
SECOND = ("tobias", "Tobias")


class Person:
    def __init__(self, folder, name):
        self.name = name
        with open(os.path.join(PEOPLE, folder, "self.md")) as f:
            self_md = f.read()
        with open(os.path.join(PEOPLE, folder, "secret.md")) as f:
            secret_md = f.read()
        self.system = prompts.person_system(name, self_md, secret_md)
        self.messages = []

    def _ask(self, text, model, max_tokens, effort):
        self.messages.append({"role": "user", "content": text})
        reply = llm.ask(self.system, self.messages, model, max_tokens, effort)
        if not reply:
            reply = "[says nothing]"
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def think(self, text):
        return self._ask(text, settings.SCENE_MODEL,
                         settings.THOUGHT_MAX_TOKENS, settings.THOUGHT_EFFORT)

    def speak(self, text):
        line = self._ask(text, settings.SCENE_MODEL,
                         settings.LINE_MAX_TOKENS, settings.SCENE_EFFORT)
        # If the model echoes the "Name:" convention back, strip it.
        prefix = self.name + ":"
        if line.startswith(prefix):
            line = line[len(prefix):].strip()
            self.messages[-1]["content"] = line or "[says nothing]"
        return line


def left(line):
    return "[leaves]" in line.lower()


def heading(text):
    print()
    print("=" * 72)
    print(text)
    print("=" * 72)


def run():
    a = Person(*FIRST)
    b = Person(*SECOND)

    heading("SETTING")
    print(SETTING)

    before = SETTING + "\n\n" + prompts.BEFORE
    for p in (a, b):
        heading(f"{p.name}, before")
        print(p.think(before))

    heading("SCENE")
    line = a.speak(prompts.OPENER.format(other=b.name))
    print(f"{a.name}: {line}\n")
    line = b.speak(prompts.ENTER.format(other=a.name) + f"\n\n{a.name}: {line}")
    print(f"{b.name}: {line}\n")

    gone = left(line)
    for _ in range(settings.SCENE_EXCHANGES - 1):
        if gone:
            break
        line = a.speak(f"{b.name}: {line}")
        print(f"{a.name}: {line}\n")
        if left(line):
            # The other person gets one last word to the closing door.
            line = b.speak(f"{a.name}: {line}")
            print(f"{b.name}: {line}\n")
            break
        line = b.speak(f"{a.name}: {line}")
        print(f"{b.name}: {line}\n")
        gone = left(line)
    if gone:
        line = a.speak(f"{b.name}: {line}")
        print(f"{a.name}: {line}\n")

    for p, other in ((a, b), (b, a)):
        heading(f"{p.name}, after")
        print(p.think(prompts.AFTER.format(other=other.name)))

    print()
    print(f"[tokens: {llm.usage['input']} in, {llm.usage['output']} out]")


if __name__ == "__main__":
    try:
        run()
    except (llm.NoCredentials, anthropic.AuthenticationError):
        sys.exit("No usable API key. Set ANTHROPIC_API_KEY in the environment and run again.")
    except anthropic.APIConnectionError as e:
        sys.exit(f"Could not reach the API: {e}")
