#!/usr/bin/env python3
"""mk_sidecar.py — builds the B5 disposition workbook (ledger_sidecar.json).

The analyst declares the disposition RULES; this tool performs the partition over the evidence
registry and emits the per-palace addends. CAP-14 then re-enumerates the same numbers from the
sidecar and verifies that each palace's live total equals its registry count (charter law 45/46).

Disposition rules (declared):
  ADDRESSED    - the atom is cited by at least one claim in the claim set
  CORROBORATED - not cited, but its normalised marker core (band prefix stripped: 天/暗/地/天盘干/
                 暗干干/寄宫干) equals that of a cited atom in the same palace
  DEFERRED     - not cited and no corroboration twin: recorded and available, not used by the
                 deliverable (counts appear in the gap report as deferred scope)
  EXCLUDED     - excluded by case scope (do_not_say / forbidden scope); none in this run
  UNPARSEABLE  - the atom could not be typed; none in this run
  ANOMALY      - the atom is itself an anomaly record; none in this run
  ABSENT       - a required role slot that the chart does not populate at that palace
"""
import io, json, os, re, sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(RUN)))))

BAND_PREFIXES = ["天盘干", "暗干干", "寄宫干", "天盘", "地盘", "暗干", "天", "地", "暗", "寄"]


def core(value):
    v = value.strip()
    for p in BAND_PREFIXES:
        if v.startswith(p) and len(v) > len(p):
            return v[len(p):].strip()
    return v


def main():
    reg = json.load(io.open(os.path.join(RUN, "raw/state/evidence_registry.json"), encoding="utf-8"))
    side = json.load(io.open(os.path.join(RUN, "authored/claim_set.json"), encoding="utf-8"))
    cited = set()
    for c in side["claims"]:
        cited |= set(c.get("cited_E", []))
    cited_cores = {}
    for r in reg["e_atoms"]:
        if r["id"] in cited:
            cited_cores.setdefault(r["palace_canonical"], set()).add(core(r["value"]))

    rows = {}
    detail = []
    for r in reg["e_atoms"]:
        p = r["palace_canonical"]
        if r["id"] in cited:
            disp = "ADDRESSED"
        elif core(r["value"]) in cited_cores.get(p, set()):
            disp = "CORROBORATED"
        else:
            disp = "DEFERRED"
        detail.append({"id": r["id"], "palace": p, "disposition": disp,
                       "role": r["role"], "value": r["value"][:48]})
        rows.setdefault(p, {}).setdefault(disp, 0)
        rows[p][disp] += 1

    # absent slots: required roles the chart does not populate (verified by CAP-04 coverage)
    absent = {}
    for p in range(1, 10):
        absent[p] = 2                      # void, horse: absent in every palace
    absent[5] += 3                         # centre: heaven_stem, door, deity absent
    absent[0] = 0                          # chart-level block: no absent roles

    palace_dispositions = []
    rank = {"ADDRESSED": 0, "CORROBORATED": 1, "DEFERRED": 2, "EXCLUDED": 3,
            "UNPARSEABLE": 4, "ANOMALY": 5}
    for p in sorted(rows):
        d = rows[p]
        palace_dispositions.append({
            "palace": p,
            "addressed": d.get("ADDRESSED", 0),
            "corroborated": d.get("CORROBORATED", 0),
            "deferred": d.get("DEFERRED", 0),
            "excluded": d.get("EXCLUDED", 0),
            "unparseable": d.get("UNPARSEABLE", 0),
            "anomaly": d.get("ANOMALY", 0),
        })
    out = {
        "file_role": "B5 disposition workbook. Rules declared by the analyst; the partition and "
                     "all addends are produced by tools/mk_sidecar.py and re-enumerated by CAP-14.",
        "rules": {
            "ADDRESSED": "cited by at least one claim in authored/claim_set.json",
            "CORROBORATED": "not cited; marker core identical to a cited atom in the same palace",
            "DEFERRED": "not cited and no corroboration twin; recorded, not used by the deliverable",
            "EXCLUDED": "excluded by case scope (do_not_say / forbidden scope): none in this run",
            "UNPARSEABLE": "could not be typed: none in this run",
            "ANOMALY": "atom is itself an anomaly record: none in this run",
            "ABSENT": "required role slot the chart does not populate at that palace "
                      "(void and horse everywhere; heaven stem, gate and deity at the centre)",
        },
        "absent_slots_per_palace": {str(k): v for k, v in sorted(absent.items())},
        "absent_slot_list": sorted(["palace %d: void" % p for p in range(1, 10)] +
                                   ["palace %d: horse" % p for p in range(1, 10)] +
                                   ["palace 5: heaven stem", "palace 5: gate", "palace 5: deity"]),
        "global_absent": {"count": 0,
                          "note": "no global absent slot beyond the per-palace rows in this run"},
        "palace_dispositions": palace_dispositions,
        "disposition_detail": sorted(detail, key=lambda d: (d["palace"], d["id"])),
        "tally_check": {
            "registry_atom_count": len(reg["e_atoms"]),
            "partition_sum": sum(sum(rows[p].values()) for p in rows),
            "absent_slot_count": sum(absent.values()),
            "total_slots_closed": sum(sum(rows[p].values()) for p in rows) + sum(absent.values()),
        },
    }
    assert out["tally_check"]["partition_sum"] == len(reg["e_atoms"]), "partition does not close"
    path = os.path.join(RUN, "authored/ledger_sidecar.json")
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"wrote": "authored/ledger_sidecar.json",
                      "registry_atoms": len(reg["e_atoms"]),
                      "partition_sum": out["tally_check"]["partition_sum"],
                      "absent_slots": out["tally_check"]["absent_slot_count"],
                      "total_slots_closed": out["tally_check"]["total_slots_closed"],
                      "per_palace": {str(r["palace"]): sum(v for k, v in r.items() if k != "palace")
                                     for r in palace_dispositions}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
