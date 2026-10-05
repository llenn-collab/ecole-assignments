#!/usr/bin/env python3
"""mk_rt_lines.py — composes the red-team lines (charter grammar: RT|A###|criticizes=C###|...) from
the authored rt_rows. Composition is mechanical; CAP-13 then validates every emitted line against
the grammar, so a malformed row is rejected rather than silently emitted."""
import io, json, os, sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    side = json.load(io.open(os.path.join(RUN, "authored/claim_set.json"), encoding="utf-8"))
    rows = side["rt_rows"]
    # ordering fixed by archetype id then claim id (charter RT scope rule)
    rows = sorted(rows, key=lambda r: (r["id"], r["criticizes"]))
    out = ["RT|%s|criticizes=%s|kind=%s|status=%s" %
           (r["id"], r["criticizes"], r["kind"], r["status"]) for r in rows]
    d = os.path.join(RUN, "renders")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "rt_lines.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(json.dumps({"wrote": "renders/rt_lines.txt", "lines": len(out)}, indent=2))


if __name__ == "__main__":
    main()
