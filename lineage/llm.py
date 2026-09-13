"""One thin door to the API. Every model call in Lineage goes through here."""

import sys

import anthropic

_client = None
usage = {"input": 0, "output": 0}


class NoCredentials(Exception):
    """The SDK found no API key at all."""


def client():
    global _client
    if _client is None:
        # Reads ANTHROPIC_API_KEY from the environment. Never hardcoded.
        _client = anthropic.Anthropic()
    return _client


def ask(system, messages, model, max_tokens, effort):
    """Send a conversation and return the text of the reply.

    If the model declines to answer (stop_reason == "refusal") the reply is an
    empty string and the reason goes to stderr. Callers treat an empty reply
    as silence. What silence means is for the people in the room to decide.
    """
    try:
        resp = client().messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            output_config={"effort": effort},
        )
    except TypeError as e:
        # The SDK raises a bare TypeError when no credential is set anywhere.
        if "authentication method" in str(e):
            raise NoCredentials(str(e)) from None
        raise
    usage["input"] += resp.usage.input_tokens
    usage["output"] += resp.usage.output_tokens
    if resp.stop_reason == "refusal":
        d = resp.stop_details
        why = f"{d.category}: {d.explanation}" if d else "no details"
        print(f"    [the model declined to answer: {why}]", file=sys.stderr)
        return ""
    return "".join(b.text for b in resp.content if b.type == "text").strip()
