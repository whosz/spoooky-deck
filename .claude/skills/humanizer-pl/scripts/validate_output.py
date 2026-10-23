#!/usr/bin/env python3
"""Deterministic QA gates for a humanizer input/output pair.

This checks mechanical invariants only. It cannot decide whether a rewrite is
stylistically better, so the humanizer still needs a semantic and editorial
pass before returning the final text.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "evals" / "evals.json"
FORBIDDEN = "\u2014\u2013"
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b|\[\s*placeholder\s*\]", re.I)
NUMBER_RE = re.compile(r"(?<!\w)\d+(?:[.,]\d+)?%?(?!\w)")
URL_RE = re.compile(r"https?://[^\s)\]>]+")
PROCESS_ARTIFACTS = (
    "as an ai language model",
    "as a language model",
    "jako model językowy",
    "i'll now",
    "i will now",
    "teraz przejdę do",
    "poniżej przedstawiam",
    "here's an overview",
    "here is an overview",
    "in the following sections",
)


def _config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _first_nonempty(text: str) -> str:
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def _counts(pattern: re.Pattern[str], text: str) -> Counter[str]:
    return Counter(pattern.findall(text))


def _urls(text: str) -> set[str]:
    return {url.rstrip(".,;:!?\"'") for url in URL_RE.findall(text)}


def _paragraphs(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", block).strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip()
    ]


def check(input_text: str, output_text: str, lang: str = "auto", preserve: Iterable[str] = ()) -> dict[str, bool]:
    cfg = _config()
    lower = output_text.lower()
    detected = lang
    if detected == "auto":
        detected = "pl" if re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", input_text) else "en"
    banned = cfg["banned_words"].get(detected, [])
    fillers = cfg["filler_openers"].get(detected, [])
    artifacts = next(a["list"] for a in cfg["assertions"] if a["id"] == "no_chatbot_artifacts")
    urls_in = _urls(input_text)
    urls_out = _urls(output_text)
    numbers_in = _counts(NUMBER_RE, input_text)
    numbers_out = _counts(NUMBER_RE, output_text)
    required = list(preserve)
    result = {
        "nonempty": bool(output_text.strip()),
        "no_forbidden_dashes": not any(char in output_text for char in FORBIDDEN),
        "no_banned_words": not any(word in lower for word in banned),
        "not_longer_than_input": len(output_text) <= len(input_text),
        "first_line_not_filler": not any(_first_nonempty(output_text).lower().startswith(item) for item in fillers),
        "no_chatbot_artifacts": not any(item in lower for item in artifacts),
        "no_process_artifacts": not any(item in lower for item in PROCESS_ARTIFACTS),
        "no_placeholders": not PLACEHOLDER_RE.search(output_text),
        "no_duplicate_paragraphs": len(_paragraphs(output_text)) == len(set(_paragraphs(output_text))),
        "markdown_fences_balanced": output_text.count("```") % 2 == 0,
        "language_signals_preserved": detected != "pl" or bool(re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", output_text)),
        "urls_preserved": urls_in <= urls_out,
        "numbers_preserved": all(numbers_out[token] >= count for token, count in numbers_in.items()),
        "protected_fragments_preserved": all(fragment.casefold() in output_text.casefold() for fragment in required),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic humanizer QA gates")
    parser.add_argument("--input", required=True, help="original text file")
    parser.add_argument("--output", required=True, help="humanized text file")
    parser.add_argument("--lang", choices=("auto", "pl", "en"), default="auto")
    parser.add_argument("--preserve", action="append", default=[], help="fragment that must remain in output")
    args = parser.parse_args()
    input_text = Path(args.input).read_text(encoding="utf-8")
    output_text = Path(args.output).read_text(encoding="utf-8")
    result = check(input_text, output_text, args.lang, args.preserve)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    failed = [name for name, passed in result.items() if not passed]
    if failed:
        print("FAILED: " + ", ".join(failed), file=sys.stderr)
        return 1
    print("ALL QA GATES PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
