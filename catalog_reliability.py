"""Synthetic catalog ingestion reliability demo.

Run: python catalog_reliability.py
"""
from dataclasses import dataclass
from typing import Any

FIELDS = ("title", "color", "size", "quantity", "price")
COLORS = {"nav": "Navy", "blu": "Blue", "blk": "Black", "wht": "White"}
SIZES = {"sm": "S", "med": "M", "lg": "L", "xl": "XL"}

GOLDEN = [
    {"id": "214", "title": "Linen Wrap Midi Dress", "color": "Navy", "size": "M", "quantity": 24, "price": 42.0},
    {"id": "215", "title": "Cotton Utility Shirt", "color": "Blue", "size": "S", "quantity": 12, "price": 35.5},
    {"id": "216", "title": "Wool Overshirt", "color": "Black", "size": "L", "quantity": 8, "price": 89.0},
    {"id": "217", "title": "Canvas Tote", "color": "White", "size": "XL", "quantity": 40, "price": 18.0},
    {"id": "218", "title": "Ribbed Tank", "color": "Green", "size": "M", "quantity": 16, "price": 22.0},
]

PREDICTIONS = [
    {"id": "214", "title": "Linen Wrap Midi Dress", "color": "nav", "size": "med", "quantity": "24", "price": "$42.00"},
    {"id": "215", "title": "Cotton Utility Shirt", "color": "blu", "size": "S", "quantity": 12, "price": 35.5},
    {"id": "216", "title": "Wool Overshirt", "color": "Black", "size": "L", "quantity": 8, "price": 89},
    {"id": "217", "title": "Canvas Tote", "color": "White", "size": "XL", "quantity": 40, "price": 18},
    {"id": "218", "title": "Ribbed Tank", "color": "Green", "size": "M", "quantity": None, "price": 22},
]

@dataclass
class Outcome:
    item_id: str
    first_pass: bool
    final_pass: bool
    repaired: list[str]
    review: bool
    mismatches: list[str]


def validate(row: dict[str, Any]) -> list[str]:
    errors = [f for f in FIELDS if row.get(f) in (None, "")]
    try:
        if row.get("quantity") is not None and int(row["quantity"]) < 0:
            errors.append("quantity")
    except (ValueError, TypeError):
        errors.append("quantity")
    try:
        if row.get("price") is not None and float(row["price"]) < 0:
            errors.append("price")
    except (ValueError, TypeError):
        errors.append("price")
    return errors


def repair(row: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    out = dict(row)
    repaired = []
    if isinstance(out.get("color"), str) and out["color"].lower() in COLORS:
        out["color"] = COLORS[out["color"].lower()]; repaired.append("color")
    if isinstance(out.get("size"), str) and out["size"].lower() in SIZES:
        out["size"] = SIZES[out["size"].lower()]; repaired.append("size")
    if isinstance(out.get("quantity"), str) and out["quantity"].isdigit():
        out["quantity"] = int(out["quantity"]); repaired.append("quantity")
    if isinstance(out.get("price"), str):
        try:
            out["price"] = float(out["price"].replace("$", "").replace(",", "")); repaired.append("price")
        except ValueError:
            pass
    return out, repaired


def main() -> None:
    outcomes = []
    for prediction, expected in zip(PREDICTIONS, GOLDEN):
        first_pass = not validate(prediction) and all(prediction.get(f) == expected.get(f) for f in FIELDS)
        repaired, fields = repair(prediction)
        mismatches = [f for f in FIELDS if repaired.get(f) != expected.get(f)]
        final_pass = not validate(repaired) and not mismatches
        outcomes.append(Outcome(prediction["id"], first_pass, final_pass, fields, not final_pass, mismatches))
    fields = len(outcomes) * len(FIELDS)
    correct = sum(len(FIELDS) - len(o.mismatches) for o in outcomes)
    first = sum(o.first_pass for o in outcomes) / len(outcomes) * 100
    final = sum(o.final_pass for o in outcomes) / len(outcomes) * 100
    print("# Synthetic catalog reliability report\n")
    print(f"Records: {len(outcomes)}")
    print(f"First-pass success: {first:.1f}%")
    print(f"Final success after bounded repair: {final:.1f}%")
    print(f"Field-level accuracy: {correct / fields * 100:.1f}%")
    print(f"Human review queue: {sum(o.review for o in outcomes)}")
    print("\n| Item | First pass | Final | Repaired | Review | Mismatches |")
    print("|---|---:|---:|---|---:|---|")
    for o in outcomes:
        print(f"| {o.item_id} | {'yes' if o.first_pass else 'no'} | {'yes' if o.final_pass else 'no'} | {', '.join(o.repaired) or '—'} | {'yes' if o.review else 'no'} | {', '.join(o.mismatches) or '—'} |")

if __name__ == "__main__":
    main()
