"""Build lineage/step1.html: Step 1 as a page that runs in the claude.ai
Artifact viewer, where the page can ask Claude on the viewer's own account.

It is built from the same files the terminal runner uses (prompts.py, the two
people under step1/people/, the setting in step1.py), so tuning those and
re-running this keeps both in step.

Run:  python lineage/artifact/build.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINEAGE = os.path.dirname(HERE)
sys.path.insert(0, LINEAGE)

import prompts    # noqa: E402
import settings   # noqa: E402
import step1      # noqa: E402

# Since the page has no system prompt slot, this joins the person's files to
# the situation inside the one leading turn.
BRIDGE = (
    "Everything above is who you are. Everything below is happening to you now. "
    "You answer only as {name}, in {name}'s own words. No preamble, no labels, "
    "no quotation marks around the whole of what you say."
)

BLURB = {
    "maren": "Thirty-four. Farms the two river plots her father cleared. Nine measures in the store, forty owed.",
    "tobias": "Forty-one. The miller. Every sack in the valley crosses his floor. A folded note in his coat.",
}


def read(folder, name):
    with open(os.path.join(step1.PEOPLE, folder, name)) as f:
        return f.read()


def person(folder, name):
    self_md = read(folder, "self.md")
    return {
        "key": folder,
        "name": name,
        "full": self_md.split(".", 1)[0].replace("I am ", ""),
        "blurb": BLURB[folder],
        "self": self_md,
        "secret": read(folder, "secret.md"),
    }


def main():
    people = [person(*step1.FIRST), person(*step1.SECOND)]
    data = {
        "passage": prompts.PASSAGE,
        "sceneRules": prompts.SCENE_RULES,
        "thoughtRules": prompts.THOUGHT_RULES,
        "bridge": BRIDGE,
        "setting": step1.SETTING,
        "before": prompts.BEFORE,
        "opener": prompts.OPENER,
        "enter": prompts.ENTER,
        "after": prompts.AFTER,
        "exchanges": settings.SCENE_EXCHANGES,
        "people": people,
        "files": [
            {"path": "lineage/prompts.py · PASSAGE", "text": prompts.PASSAGE},
            {"path": "lineage/prompts.py · SCENE_RULES", "text": prompts.SCENE_RULES},
            {"path": "lineage/prompts.py · THOUGHT_RULES", "text": prompts.THOUGHT_RULES},
        ] + [
            {"path": f"lineage/step1/people/{p['key']}/{name}", "text": p[key]}
            for p in people for name, key in (("self.md", "self"), ("secret.md", "secret"))
        ],
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    with open(os.path.join(HERE, "step1.template.html")) as f:
        html = f.read()
    marker = "/*__DATA__*/null"
    assert marker in html, "template is missing the data marker"
    out = os.path.join(LINEAGE, "step1.html")
    with open(out, "w") as f:
        f.write(html.replace(marker, blob, 1))
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
