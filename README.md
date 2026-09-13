# Lineage

A valley of independent AI agents, one per living person, across generations.
A human watches. They never play. See the build brief for what this is.

Built in the order the brief gives. Each step is run and read before the next
step starts.

## Status

Step 1: two people, one scene. Built. Waiting to be run and read.

Two ways to run it: the terminal (below), or the artifact page, which runs
the same scene inside claude.ai on the viewer's own account and needs no
API key. `lineage/artifact/build.py` builds `lineage/step1.html` from the
same prompt and people files the terminal runner uses; rebuild it after
tuning either.

## Running Step 1

```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python lineage/step1.py
```

Two hand-written people live in `lineage/step1/people/`. They talk for six
exchanges, then each writes a private reaction. Everything prints to the
terminal. Nothing is written to disk.

Models and effort are set in `lineage/settings.py`. The passage that makes an
agent a person is `PASSAGE` in `lineage/prompts.py`. That is the only thing to
tune in Step 1.
