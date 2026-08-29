# 🌍 GeoMind Energy
## AI-Assisted Formation Evaluation Platform for Petroleum Geoscience

GeoMind Energy is an AI-assisted formation evaluation platform designed to support petroleum geoscientists and petrophysicists in the analysis and interpretation of well-log data.

The platform combines deterministic petrophysical calculations with Generative AI to create an end-to-end workflow for well-log analysis, reservoir evaluation, candidate pay-zone identification, AI-assisted interpretation, and automated technical reporting.

> **GeoMind Energy is a decision-support and analytical prototype. It does not replace professional geological, petrophysical, or petroleum-engineering judgment.**

---

## 🚀 Overview

Formation evaluation requires the integration of multiple measurements to understand subsurface formations, evaluate reservoir quality, and identify intervals that may warrant further investigation.

GeoMind Energy brings several of these processes into a single application. The platform accepts well-log data in LAS format and processes the available information through a structured formation-evaluation workflow.

The system performs data-quality assessment, petrophysical evaluation, reservoir characterization, interval analysis, candidate pay identification, and reservoir-quality scoring. The calculated results are then passed to an AI layer that assists with technical interpretation and report generation.

The project combines:
- Petroleum Geoscience
- Petrophysics
- Data Science
- Artificial Intelligence
- Machine Learning
- Software Engineering
- Energy Technology

---

## 🎯 Problem Statement

Traditional formation evaluation often requires analysts to move between multiple tools and workflows for data preparation, petrophysical calculations, interval interpretation, and reporting.

GeoMind Energy explores how these processes can be brought together into a unified application while maintaining a clear distinction between quantitative calculations and AI-generated interpretation.

The goal is not to replace the petroleum geoscientist. Instead, the goal is to provide an **AI-assisted workflow that reduces repetitive analysis and reporting tasks while keeping the underlying calculations traceable.**

---

## 🧠 What GeoMind Energy Does

The current system provides an end-to-end workflow:

```text
LAS Well-Log Data
        │
        ▼
Data Ingestion
        │
        ▼
Data Quality Assessment
        │
        ▼
Petrophysical Evaluation
        │
        ▼
Reservoir Zonation
        │
        ▼
Reservoir Quality Assessment
        │
        ▼
Candidate Pay Identification
        │
        ▼
Interval / Reservoir Scoring
        │
        ▼
AI-Assisted Interpretation
        │
        ▼
Technical Formation Evaluation Report
```

---

**Status:** Active Portfolio Project

---

## Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [What GeoMind Energy Does](#-what-geomind-energy-does)
- [Core Features](#core-features)
- [AI-Assisted Formation Interpretation](#ai-assisted-formation-interpretation)
- [Formation Evaluation Workflow](#formation-evaluation-workflow)
- [Automated Technical Reporting](#automated-technical-reporting)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Example Use Case](#example-use-case)
- [Design Philosophy](#design-philosophy)
- [Why This Project Matters](#why-this-project-matters)
- [Limitations](#limitations)
- [Future Development](#future-development)

---

## Core Features

### 1. LAS Well-Log Data Ingestion
Accepts LAS-format well-log files and extracts available well-log curves for downstream formation evaluation. Built to handle real-world datasets where curve availability and data quality vary.

### 2. Data Quality Assessment
Examines the supplied well-log data prior to evaluation to identify potential data-quality issues and assess suitability for the implemented workflow.

### 3. Petrophysical Evaluation
Processes calculated petrophysical parameters, including:
- Shale volume
- Porosity
- Water saturation
- Reservoir quality indicators
- Candidate pay criteria

These parameters are evaluated together rather than relying on any single measurement.

### 4. Reservoir Zonation
Divides the well into interpreted reservoir and non-reservoir intervals based on the available petrophysical data, providing a structured view of how properties vary with depth.

### 5. Reservoir Quality Assessment
Assesses the relative quality of interpreted reservoir intervals, identifying more favorable characteristics while preserving the distinction between calculated results and interpretation.

### 6. Candidate Pay-Zone Identification
Flags intervals satisfying the implemented petrophysical criteria for candidate pay. **A candidate pay interval does not constitute confirmation of hydrocarbons, commercial reserves, or economic productivity.**

### 7. Reservoir / Interval Scoring
Provides interval-level scoring so interpreted zones can be compared and ranked by their calculated characteristics.

---

## AI-Assisted Formation Interpretation

Generative AI (Google Gemini) is integrated for **interpretation and communication**, not primary quantitative calculation. Quantitative results are always generated by the deterministic analytical workflow first.

```
Well-Log Data
      │
      ▼
Deterministic Calculations
      │
      ▼
Calculated Petrophysical Results
      │
      ▼
Structured Formation Summary
      │
      ▼
Gemini AI
      │
      ▼
Technical Interpretation
      │
      ▼
Automated Report
```

The AI layer is explicitly instructed to:
- Use only the supplied calculated information
- Avoid inventing measurements
- Avoid unsupported geological claims
- Avoid claiming hydrocarbon confirmation
- Distinguish calculated results from interpretation
- Communicate uncertainty and limitations

---

## Formation Evaluation Workflow

| Step | Description |
|------|-------------|
| 1. Upload | User uploads a LAS well-log file |
| 2. Data Processing | System reads and processes available well-log curves |
| 3. Data Quality | Application evaluates quality and availability of supplied data |
| 4. Petrophysical Analysis | Relevant petrophysical properties are calculated |
| 5. Reservoir Evaluation | Calculated properties used to evaluate reservoir intervals |
| 6. Pay Assessment | Intervals meeting criteria are flagged as candidate pay |
| 7. AI Interpretation | Calculated results passed to the AI layer for technical interpretation |
| 8. Reporting | Results compiled into a structured formation-evaluation report |

---

## Automated Technical Reporting

Generates structured formation-evaluation reports including:
- Data-quality assessment
- Reservoir evaluation
- Reservoir intervals
- Candidate pay intervals
- Petrophysical interpretation
- Key findings
- Uncertainties and limitations
- Recommended further evaluation

The goal is a concise technical document that supports further professional review.

---

## System Architecture

```
                         GEOMIND ENERGY
                              │
             ┌────────────────┴────────────────┐
             │                                  │
             ▼                                  ▼
        NEXT.JS FRONTEND                  FASTAPI BACKEND
             │                                  │
             │                                  ▼
             │                         LAS DATA PROCESSING
             │                                  │
             │                                  ▼
             │                       PETROPHYSICAL ENGINE
             │                                  │
             │                    ┌─────────────┼─────────────┐
             │                    │             │             │
             │                    ▼             ▼             ▼
             │               Reservoir       Pay Zone     Data Quality
             │                Zonation      Detection      Assessment
             │                    │             │             │
             │                    └─────────────┼─────────────┘
             │                                  │
             │                                  ▼
             │                         Reservoir Scoring
             │                                  │
             │                                  ▼
             │                             Gemini AI
             │                                  │
             │                                  ▼
             │                       Technical Interpretation
             │                                  │
             └──────────────────────────────────┤
                                                 ▼
                                           PDF Report
```

---

## Technology Stack

**Frontend**
- Next.js
- React
- TypeScript
- Tailwind CSS

**Backend**
- Python
- FastAPI

**Artificial Intelligence**
- Google Gemini API (Gemini Flash)

**Data Processing**
- LAS well-log data
- Python numerical processing
- Petrophysical calculations
- Reservoir interval analysis

**Vector Infrastructure**
- Qdrant

**Reporting**
- Automated PDF report generation

---

## Project Structure

```
GeoMind-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.x
- Node.js
- npm
- Git
- A Gemini API key (for AI interpretation functionality)

### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Environment Variables

Create `backend/.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

> Never commit your actual API key to GitHub. The `.env` file is intentionally excluded from version control.

### Running the Backend

```bash
uvicorn app.main:app --reload
```

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the local URL displayed by Next.js in your browser.

---

## Example Use Case

1. Upload a LAS well-log file
2. Review data quality
3. Run formation evaluation
4. Examine petrophysical results
5. Review reservoir intervals
6. Review candidate pay zones
7. Request AI interpretation
8. Generate a technical report

---

## Design Philosophy

> Use deterministic computation for quantitative evaluation, and AI where it adds value through interpretation and communication.

The application does not depend on the language model to independently invent quantitative petrophysical results.

```
Calculation
     ↓
Evaluation
     ↓
Interpretation
     ↓
Communication
```

This provides a clear separation between computational analysis and generative AI.

---

## Why This Project Matters

Rather than building another general-purpose chatbot, GeoMind Energy explores how AI can be integrated into a specialized petroleum-geoscience application. It demonstrates skills across:

- Domain-specific data processing
- API development
- Frontend engineering
- Petrophysical analysis
- AI integration
- Technical reporting
- Software architecture
- Data validation
- Decision-support systems

---

## Limitations

GeoMind Energy is currently a **research and portfolio project**. Its output should **not** be interpreted as confirmation of:

- Hydrocarbon presence
- Commercial reserves
- Economic viability
- Formation productivity
- Field development potential

Professional formation evaluation may require additional information such as:

- Core analysis
- Formation pressure measurements
- Fluid samples
- Formation testing
- Additional well-log interpretation
- Geological and structural information
- Well-test data
- Production data

The quality of the final interpretation also depends on the quality, completeness, and suitability of the supplied well-log data.

---

## Future Development

- Expanded petrophysical workflows
- Additional well-log-derived parameters
- Interactive well-log visualization
- Multi-well analysis
- Cross-well reservoir comparison
- Improved candidate pay classification
- Integration of core data
- Integration of formation-pressure data
- Integration of production data
- Advanced machine-learning models for formation evaluation
- Improved AI-assisted technical interpretation
- Automated comparison of multiple wells
- Enhanced reservoir characterization

---

## Project Status

**Status:** Active Portfolio Project

The core formation-evaluation workflow, AI-assisted interpretation, and automated reporting pipeline have been implemented.
