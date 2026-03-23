"""
utils/validators.py
JSON schema validation for dataset records.

WHY: Catching malformed training samples early (before fine-tuning) prevents
silent model degradation. Schema validation is the "type system" for our data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from utils.logger import get_logger

log = get_logger(__name__)

# ---------------------------------------------------------------------------
# Schema definitions — will be expanded per milestone
# ---------------------------------------------------------------------------

ALARM_SCHEMA = {
    "type": "object",
    "required": ["alarm_id", "timestamp", "network_element", "ne_type",
                 "severity", "alarm_code", "description"],
    "properties": {
        "alarm_id":        {"type": "string"},
        "timestamp":       {"type": "string"},
        "network_element": {"type": "string"},
        "ne_type":         {"type": "string", "enum": ["AMF", "SMF", "UPF", "PCF",
                                                        "UDM", "NRF", "gNB", "IMS",
                                                        "PCSCF", "ICSCF", "SCSCF"]},
        "severity":        {"type": "string", "enum": ["CRITICAL", "MAJOR", "MINOR", "WARNING"]},
        "alarm_code":      {"type": "string"},
        "description":     {"type": "string", "minLength": 5},
        "additional_info": {"type": "object"},
    },
    "additionalProperties": False,
}

TRAINING_SAMPLE_SCHEMA = {
    "type": "object",
    "required": ["instruction", "input", "output"],
    "properties": {
        "instruction": {"type": "string", "minLength": 10},
        "input":       {"type": "string"},
        "output":      {"type": "string", "minLength": 20},
        "metadata":    {"type": "object"},
    },
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_record(record: dict[str, Any], schema: dict) -> tuple[bool, str]:
    """Validate a single record against a JSON schema.

    Returns:
        (is_valid, error_message)  — error_message is empty string if valid.
    """
    try:
        jsonschema.validate(instance=record, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, e.message


def validate_dataset_file(path: str | Path, schema: dict) -> dict[str, Any]:
    """Validate all records in a JSON file and report results.

    Returns:
        Summary dict with counts and list of errors.
    """
    path = Path(path)
    with open(path) as f:
        records = json.load(f)

    results = {"total": len(records), "valid": 0, "invalid": 0, "errors": []}

    for i, record in enumerate(records):
        ok, msg = validate_record(record, schema)
        if ok:
            results["valid"] += 1
        else:
            results["invalid"] += 1
            results["errors"].append({"index": i, "error": msg})

    log.info(
        f"Validated {path.name}: {results['valid']}/{results['total']} valid"
        + (f", {results['invalid']} errors" if results["invalid"] else "")
    )
    return results
