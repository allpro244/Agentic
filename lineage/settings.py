"""Lineage settings. Every tunable knob lives here and nowhere else.

The API key is never here. It comes from the ANTHROPIC_API_KEY environment
variable (the SDK reads it itself).
"""

# Models.
SCENE_MODEL = "claude-sonnet-5"    # lines of dialogue, ordinary private thoughts, ledger updates
THOUGHT_MODEL = "claude-opus-5"    # private thoughts on major decisions:
                                   # marriage, killing, betrayal, a death in the family, inheritance

# How hard each kind of call thinks: low | medium | high | xhigh | max.
# A line of speech is quick and impulsive. A private thought gets a little longer.
SCENE_EFFORT = "low"
THOUGHT_EFFORT = "medium"

# Output ceilings.
LINE_MAX_TOKENS = 600
THOUGHT_MAX_TOKENS = 1500

# One exchange is one line from each person. Six exchanges is twelve lines.
SCENE_EXCHANGES = 6
