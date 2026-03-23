# 5G Telecom AI Engine

> **Production-grade AI system for 5G network analysis, root cause analysis (RCA), and intelligent troubleshooting — powered by Kara-Kumru-v1.0-2B with QLoRA fine-tuning and RAG.**

---

## Overview

This engine processes raw 5G network telemetry — alarms, KPI metrics, protocol logs (SIP, DIAMETER, GTPv2), and call flows — and outputs:

- **Root Cause Analysis (RCA)** with confidence scores
- **Human-readable explanations** of network events
- **Actionable troubleshooting suggestions**

The architecture is designed for real telecom production environments, modular enough to evolve into a full product.

---

## Architecture

```
Raw Telecom Data
(Alarm / KPI / Logs / PCAP)
        │
        ▼
  Parser / Normalizer
   (utils/parsers.py)
        │
        ▼
  Structured JSON
  (dataset/processed/)
        │
        ▼
Fine-tuned LLM (Kara-Kumru-v1.0-2B)
  + QLoRA adapter
  (training/ + inference/)
        │
        ▼
   RAG Retriever
(3GPP specs + domain docs)
    (rag/)
        │
        ▼
  RCA + Explanation Engine
    (inference/rca_engine.py)
        │
        ▼
  FastAPI REST Output
      (api/)
```

---

## Project Structure

```
5G-LLM-ENGINE/
│
├── dataset/
│   ├── raw/                  # Raw alarm/KPI/log files (JSON, CSV, PCAP)
│   ├── processed/            # Cleaned, normalized JSON ready for training
│   └── schemas/              # JSON Schema definitions for validation
│
├── training/
│   ├── configs/              # LoRA + training hyperparameter configs
│   ├── checkpoints/          # Model checkpoints (symlinked from GDrive)
│   ├── train.py              # Main QLoRA fine-tuning script (Colab-ready)
│   └── dataset_prep.py       # Dataset loading + formatting for SFTTrainer
│
├── inference/
│   ├── infer.py              # CLI inference: load base + LoRA, run prompt
│   └── rca_engine.py         # RCA reasoning: input + RAG + LLM -> output
│
├── rag/
│   ├── documents/            # 3GPP specs, telecom PDFs, knowledge base
│   ├── vectorstore/          # Persisted FAISS / Chroma index
│   ├── embed.py              # Document ingestion + embedding pipeline
│   └── retriever.py          # Query interface for RAG retrieval
│
├── utils/
│   ├── parsers.py            # Alarm / KPI / log parsers -> structured JSON
│   ├── validators.py         # JSON schema validation helpers
│   └── logger.py             # Structured logging setup
│
├── evaluation/
│   ├── eval.py               # RCA accuracy, Top-3, explanation quality
│   └── metrics.py            # ROUGE, custom telecom accuracy metrics
│
├── api/
│   ├── main.py               # FastAPI app entry point
│   ├── routes/               # Endpoint definitions
│   └── schemas.py            # Pydantic request/response models
│
├── notebooks/
│   └── milestone1_setup.ipynb  # Colab setup + environment verification
│
├── docs/                     # Architecture diagrams, design notes
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Project Setup | Done |
| 2 | Dataset Design | Pending |
| 3 | Synthetic Data Generation | Pending |
| 4 | QLoRA Fine-Tuning Pipeline | Pending |
| 5 | Inference Engine | Pending |
| 6 | RAG System | Pending |
| 7 | RCA Engine | Pending |
| 8 | Evaluation | Pending |
| 9 | Production Architecture | Pending |

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/cem8kaya/5G-LLM-ENGINE.git
cd 5G-LLM-ENGINE
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Google Colab Setup

Open `notebooks/milestone1_setup.ipynb` in Colab and run all cells to:
- Mount Google Drive
- Install dependencies
- Verify GPU availability
- Clone this repo into Colab

### 3. Run Inference (after fine-tuning)

```bash
python inference/infer.py \
  --input '{"alarm_id": "AMF-001", "severity": "CRITICAL", "description": "AMF overload"}' \
  --model ./training/checkpoints/kumru-5g-v1
```

---

## Model

**Base model:** `Kara-Kumru-v1.0-2B`
**Fine-tuning method:** QLoRA (4-bit quantization + LoRA adapters)
**Training platform:** Google Colab (T4/A100)
**Framework:** HuggingFace Transformers + PEFT + TRL

---

## Domain Coverage

| Component | Protocols / Standards |
|-----------|----------------------|
| Core Network | AMF, SMF, UPF, PCF, UDM, NRF |
| IMS | SIP, DIAMETER (Cx, Sh, Rx) |
| Transport | GTPv2-C, GTPv1-U |
| Radio | NG-RAN, gNB, PDCP/RLC/MAC |
| Standards | 3GPP TS 23.501, 23.502, 29.518 |

---

## License

Apache 2.0 — see [LICENSE](LICENSE)
