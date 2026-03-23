"""
utils/parsers.py
Raw telecom data parsers -> normalized structured JSON.

WHY: Each data source (alarms, KPIs, protocol logs) has a different raw
format. Normalizing everything to a single JSON schema decouples the
upstream data variety from the LLM pipeline.

Parsers implemented here (stubs — expanded in Milestone 2+):
  - AlarmParser     : vendor alarm CSV/syslog -> AlarmRecord
  - KPIParser       : PM counter CSV/JSON -> KPIRecord
  - ProtocolParser  : SIP/DIAMETER/GTPv2 text logs -> ProtocolRecord
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from utils.logger import get_logger

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Data models (plain dataclasses — no heavy dependencies)
# ---------------------------------------------------------------------------

@dataclass
class AlarmRecord:
    alarm_id: str
    timestamp: str
    network_element: str          # e.g. "AMF-1", "SMF-POOL-2"
    ne_type: str                  # e.g. "AMF", "SMF", "UPF", "gNB"
    severity: str                 # CRITICAL | MAJOR | MINOR | WARNING
    alarm_code: str
    description: str
    additional_info: dict[str, Any]


@dataclass
class KPIRecord:
    timestamp: str
    network_element: str
    ne_type: str
    kpi_name: str                 # e.g. "PDU_SESSION_SETUP_SR"
    value: float
    unit: str                     # e.g. "%", "ms", "Mbps"
    threshold: float | None
    is_anomaly: bool


@dataclass
class ProtocolRecord:
    timestamp: str
    protocol: str                 # SIP | DIAMETER | GTPv2
    direction: str                # UL | DL
    src: str
    dst: str
    message_type: str             # e.g. "INVITE", "CCR", "Create Session Request"
    result_code: str | None       # e.g. "200 OK", "DIAMETER_UNABLE_TO_COMPLY"
    raw_snippet: str


# ---------------------------------------------------------------------------
# Parser classes (to be expanded per milestone)
# ---------------------------------------------------------------------------

class AlarmParser:
    """Parse vendor alarm exports into AlarmRecord objects."""

    def from_dict(self, raw: dict[str, Any]) -> AlarmRecord:
        """Parse a single alarm from a raw dictionary."""
        return AlarmRecord(
            alarm_id=raw.get("alarm_id", ""),
            timestamp=raw.get("timestamp", ""),
            network_element=raw.get("network_element", ""),
            ne_type=raw.get("ne_type", ""),
            severity=raw.get("severity", "UNKNOWN"),
            alarm_code=raw.get("alarm_code", ""),
            description=raw.get("description", ""),
            additional_info=raw.get("additional_info", {}),
        )

    def from_json_file(self, path: str | Path) -> list[AlarmRecord]:
        """Load a JSON file containing a list of raw alarm dicts."""
        records = []
        with open(path) as f:
            data = json.load(f)
        for item in data:
            try:
                records.append(self.from_dict(item))
            except Exception as e:
                log.warning(f"Skipping malformed alarm record: {e}")
        log.info(f"Parsed {len(records)} alarm records from {path}")
        return records


class KPIParser:
    """Parse PM counter exports into KPIRecord objects."""

    def from_dict(self, raw: dict[str, Any]) -> KPIRecord:
        return KPIRecord(
            timestamp=raw.get("timestamp", ""),
            network_element=raw.get("network_element", ""),
            ne_type=raw.get("ne_type", ""),
            kpi_name=raw.get("kpi_name", ""),
            value=float(raw.get("value", 0.0)),
            unit=raw.get("unit", ""),
            threshold=raw.get("threshold"),
            is_anomaly=bool(raw.get("is_anomaly", False)),
        )


class ProtocolParser:
    """Parse SIP/DIAMETER/GTPv2 log lines into ProtocolRecord objects."""

    def from_dict(self, raw: dict[str, Any]) -> ProtocolRecord:
        return ProtocolRecord(
            timestamp=raw.get("timestamp", ""),
            protocol=raw.get("protocol", ""),
            direction=raw.get("direction", ""),
            src=raw.get("src", ""),
            dst=raw.get("dst", ""),
            message_type=raw.get("message_type", ""),
            result_code=raw.get("result_code"),
            raw_snippet=raw.get("raw_snippet", ""),
        )


# ---------------------------------------------------------------------------
# Convenience: convert any record to dict for JSON serialization
# ---------------------------------------------------------------------------

def record_to_dict(record) -> dict[str, Any]:
    return asdict(record)
