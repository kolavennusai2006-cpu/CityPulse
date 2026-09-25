# CityPulse — AI Civic Intelligence OS

> **Detect. Connect. Investigate. Explain. Simulate.**

CityPulse is an AI-powered civic intelligence platform designed to turn fragmented urban signals into a single, understandable picture of what is happening across a city.

Instead of looking at weather, traffic, transit delays, citizen complaints, air quality, and civic events separately, CityPulse combines these signals, analyzes how they change over time and across locations, detects unusual patterns, reconstructs emerging civic events, and explains the evidence in plain language.

---

## The Idea

### One glance should tell a resident:

- What is happening?
- Where is it happening?
- Why was it flagged?
- How serious is it?
- What evidence supports it?
- What changed over time?
- What could happen under a simulated scenario?

CityPulse is designed around the intelligence loop:

```text
SENSE
  ↓
UNDERSTAND
  ↓
CONNECT
  ↓
DETECT
  ↓
EXPLAIN
  ↓
SIMULATE
  ↓
RESPOND
Problem Statement

Urban civic information is often fragmented across multiple systems.

Weather conditions, traffic congestion, public transit delays, citizen complaints, air quality, incidents, and other city signals may be available separately, with different formats, timestamps, update rates, and levels of reliability.

This creates two problems:

Residents do not have a single, understandable view of what is happening around them.
City stakeholders may miss relationships and emerging patterns when each signal is viewed independently.

CityPulse addresses this by creating a unified civic intelligence layer that:

Collects
   ↓
Validates
   ↓
Normalizes
   ↓
Analyzes
   ↓
Connects
   ↓
Detects
   ↓
Explains
   ↓
Simulates
CityPulse Architecture

CityPulse is built as a 16-layer AI Civic Intelligence architecture.

1.  MULTI-SOURCE INGESTION
            ↓
2.  DATA QUALITY ENGINE
            ↓
3.  NORMALIZATION ENGINE
            ↓
4.  CIVIC DIGITAL TWIN
            ↓
5.  MULTI-LAYER ANOMALY ENGINE
            ↓
6.  TEMPORAL REASONING ENGINE
            ↓
7.  CROSS-SIGNAL FUSION
            ↓
8.  EVENT INTELLIGENCE
            ↓
9.  CIVIC EVENT GRAPH
            ↓
10. RISK ENGINE
            ↓
11. AGENTIC AI LAYER
            ↓
12. EVIDENCE MEMORY
            ↓
13. GROUNDED GENAI
            ↓
14. SIMULATION
            ↓
15. TIME MACHINE
            ↓
16. CIVIC COMMAND CENTER
1. Multi-Source Ingestion

CityPulse is designed to work with multiple civic data streams.

Current architectural signal categories include:

Weather
Traffic
Transit
Complaints
AQI
Events

The ingestion layer allows different sources to enter the intelligence pipeline without requiring every source to use the same format.

2. Data Quality Engine

Before civic signals are analyzed, the system evaluates data quality.

The layer considers:

Validation
Missing Data
Outliers
Source Health
Timestamp Consistency

This helps prevent incomplete or abnormal source data from directly producing misleading civic conclusions.

3. Normalization Engine

Different sources are converted into a common civic representation.

The common schema contains:

zone
timestamp
signal
value
source

This allows weather, traffic, transit, complaints, and other signals to be processed consistently by the downstream intelligence layers.

4. Civic Digital Twin

CityPulse maintains a simplified digital representation of the monitored city.

Each monitored zone maintains information about:

Current State
Signal State
Historical State
Baseline
Trends
Risk
Events

For the Jaipur demonstration, internal zone identifiers are presented using human-friendly names:

Internal ID	Display Area
ZONE_A	Pink City Core
ZONE_B	Malviya Nagar
ZONE_C	Vaishali Nagar
ZONE_D	C-Scheme
ZONE_E	Sanganer

The internal IDs remain useful for system processing while the dashboard presents recognizable area names to users.

5. Multi-Layer Anomaly Engine

CityPulse does not depend on a single anomaly rule.

The architecture combines multiple detection approaches:

Statistical Baseline

Identifies deviations from expected signal behavior.

Machine Learning

Uses machine-learning based anomaly detection to identify unusual civic patterns.

Temporal Rules

Detects abnormal signal changes over successive observations.

Spatial Detection

Provides spatial context for understanding whether unusual conditions are concentrated in a particular area.

Change-Point Detection

Identifies significant shifts in civic signal behavior.

These outputs are combined into an:

ANOMALY ENSEMBLE
6. Temporal Reasoning Engine

A civic event is not always defined by a single abnormal value.

CityPulse therefore evaluates how signals evolve over time.

The temporal layer considers:

Persistence
Acceleration
Trend
Change Point
Early Warning

This helps distinguish temporary fluctuations from patterns that continue or intensify.

7. Cross-Signal Fusion

CityPulse looks for convergence between different civic signals.

The system evaluates:

Signal Count
Time Overlap
Spatial Overlap
Convergence Score

For example, an increase in rainfall, traffic congestion, transit delays, and citizen complaints during a similar time window may represent a stronger civic signal than any one indicator alone.

8. Event Intelligence

CityPulse transforms related anomalies into structured civic events.

An event can contain:

Event ID
Zone
Start Time
End Time
Duration
Signals
Risk
Evidence
Temporal State
Timeline
Recovery State

Events can move through different lifecycle stages:

START
  ↓
DEVELOPING
  ↓
ESCALATING
  ↓
PEAK
  ↓
RECOVERING

This allows the dashboard to communicate not only that an incident exists, but also how it is evolving.

9. Civic Event Graph

CityPulse connects related signals into a civic event graph.

Example:

              WEATHER
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
     TRAFFIC   TRANSIT  COMPLAINTS
        │        │        │
        └────────┼────────┘
                 ↓
           CIVIC EVENT

The graph is designed to represent:

Observed Signals
Temporal Relationships
Spatial Relationships
Possible Relationships
Correlation is not automatically treated as causation.

CityPulse uses evidence-oriented language such as:

Possible relationship
Observed association
Temporal overlap
Spatial overlap
Not confirmed causation
10. Risk Engine

The Risk Engine converts civic evidence into a unified risk representation.

Risk considers:

Severity
Confidence
Persistence
Exposure
Convergence

The result is a:

CIVIC RISK SCORE

CityPulse uses the following status thresholds:

Risk Score	Status
0–29	NORMAL
30–49	WATCH
50–74	EMERGING
75–100	CRITICAL

This allows a complex set of signals to be communicated through a simple civic status.

11. Agentic AI Layer

CityPulse includes a Civic AI Agent designed around structured investigation rather than unrestricted generation.

The agent supports:

Investigate
Compare
Verify
Explain
Simulate

Conceptually:

User Question
      ↓
Civic AI Agent
      ↓
Investigation Tools
      ↓
Current Data
Historical Data
Event Timeline
Evidence
Zone Comparison
      ↓
Grounded Explanation

This gives users a way to ask not only what is happening, but also why the system flagged it.

12. Evidence Memory

CityPulse retains structured civic context through:

Event Memory
Historical Memory
Evidence Store

This supports investigation and replay by preserving the evidence associated with detected events.

13. Grounded GenAI

The generative AI layer works from structured civic evidence.

Structured Evidence
        ↓
Civic Intelligence Context
        ↓
Grounded GenAI
        ↓
Civic Intelligence Brief

The brief is designed to answer:

What happened?
Why was it flagged?
What changed?
Which signals are involved?
What evidence supports the alert?
What remains uncertain?

The objective is to generate useful explanations without inventing unsupported facts.

14. What-If Simulation

CityPulse supports hypothetical scenario analysis.

Users can modify selected civic inputs such as:

Rainfall
Traffic
Transit Delay

The simulation pipeline is:

USER SCENARIO
      ↓
RECOMPUTE CIVIC STATE
      ↓
RECOMPUTE RISK
      ↓
PROJECT CONSEQUENCES

All simulated results are explicitly identified as:

SIMULATED — NOT OBSERVED

This keeps hypothetical outcomes separate from real observations.

15. Time Machine

CityPulse includes a historical replay concept for understanding how civic events evolve.

PAST
 │
 ├── -30 min
 ├── -15 min
 ├── NOW
 └── FUTURE SCENARIO

The Time Machine can be used to examine:

Historical Snapshots
Event Evolution
Risk Changes
Signal Changes
Recovery

This helps users understand the progression of an incident rather than only viewing its current state.

16. Civic Command Center

All intelligence is presented through a unified dashboard.

The command center brings together:

Live Pulse
Priority Alerts
Risk Map
Zone Risk
Signal Intelligence
Event Graph
Live Incident Map
Historical Risk Profile
Event Replay
Citizen Reporting
Safety Checker
AI Investigation
Civic Brief
What-If Simulation
Data Source Status

The design goal is simple:

Understand the city's civic state in seconds, then investigate deeper when needed.

Key Features
Live Civic Pulse

Provides a consolidated view of current civic conditions.

Priority Alert

Highlights high-priority civic conditions so important incidents are visible immediately.

Risk Map

Provides a visual representation of risk across monitored zones.

Zone Intelligence

Allows users to inspect individual areas and understand the signals contributing to their current status.

Event Graph

Connects related civic signals into a single event context.

Historical Risk Profile

Provides historical context for understanding recurring or significant conditions.

Time-Based Replay

Shows how detected events change across multiple observations.

Citizen Reporting

Allows residents to report civic conditions such as:

Waterlogging
Road Damage
Accident
Power Outage
Gas Leak
Transit Issue
Traffic Signal Failure
Fallen Tree
Garbage
Streetlight Issue
Other Civic Problems
Citizen Safety Checker

Provides a simple interface for assessing current civic conditions before or during travel.

Ask CityPulse

Users can ask questions about monitored civic conditions and receive structured, evidence-based responses.

What-If Simulation

Users can modify selected conditions and observe the resulting simulated civic risk.

Current Demonstration

The current demonstration uses a structured civic scenario to show how CityPulse processes multiple signals over time.

Example signals include:

Rainfall
Traffic
Transit Delay
Citizen Complaints

A multi-signal disruption is processed through:

Baseline
   ↓
Anomaly Detection
   ↓
ML Detection
   ↓
Temporal Reasoning
   ↓
Cross-Signal Fusion
   ↓
Event Detection
   ↓
Risk Calculation
   ↓
Evidence
   ↓
AI Explanation
   ↓
Recovery

This demonstrates the core intelligence pipeline without requiring every real-world civic feed to be available during the hackathon.

Real-World Data Integration

The architecture is designed to support verified external civic sources.

Potential integration categories include:

Weather
Disaster Alerts
Air Quality
Traffic
Transit
Citizen Complaints
Civic Events
News

External feeds should pass through the same intelligence pipeline:

External Source
      ↓
Validation
      ↓
Data Quality
      ↓
Normalization
      ↓
Civic State
      ↓
Detection
      ↓
Fusion
      ↓
Risk
      ↓
Evidence
      ↓
Explanation

This allows the same architecture to move from synthetic demonstrations toward real-time civic intelligence.

Data and Epistemic Honesty

CityPulse distinguishes between different information states.

OBSERVED
SIMULATED
REPORTED
VERIFIED

The platform is designed to avoid presenting an inferred relationship as a confirmed cause.

For example:

Evidence-based

Rainfall, traffic congestion, and transit delays increased during the same observation window.

Not automatically claimed

Rainfall caused the traffic disruption.

Instead, the system can communicate:

Possible relationship
Observed association
Temporal overlap
Spatial overlap
Not confirmed causation

This is especially important for a public-facing civic intelligence system.

Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Node.js
Express
AI / ML Engine
Python
NumPy
Pandas
scikit-learn
Generative AI
Google Gemini
Weather Integration
Open-Meteo
Development
VS Code
Git
GitHub
Project Structure
CivicPulse/
│
├── Backend/
│   ├── package.json
│   ├── package-lock.json
│   └── server.js
│
├── Python_Engine/
│   ├── agent.py
│   ├── change_point.py
│   ├── citypulse_output.json
│   ├── civic_brief.py
│   ├── detection.py
│   ├── early_warning.py
│   ├── ensemble_engine.py
│   ├── event_engine.py
│   ├── event_lifecycle.py
│   ├── features.py
│   ├── generator.py
│   ├── intelligence_output.py
│   ├── ml_engine.py
│   ├── normalizer.py
│   ├── recovery_engine.py
│   ├── server.py
│   ├── simulation.py
│   ├── statistical_engine.py
│   ├── temporal_engine.py
│   ├── tools.py
│   ├── weather_api.py
│   ├── weather_live.py
│   └── test_*.py
│
├── index (3).html
├── script (2).js
├── style (2).css
├── README.md
└── .gitignore
Running the Project Locally
1. Frontend

Open the frontend using VS Code Live Server.

Main file:

index (3).html
2. Node Backend

Open a terminal:

cd Backend
npm install
npm start
3. Python Intelligence Engine

Open another terminal:

cd Python_Engine
python server.py

The Python engine provides the civic intelligence and AI-related processing used by the platform.

API

The primary CityPulse API endpoint is:

GET /api/citypulse

The API provides the consolidated CityPulse state used by the intelligence and dashboard layers.

Additional agent and intelligence capabilities include endpoints for:

Investigation
Explanation
Verification
Zone Comparison
Event Timeline
Event Evidence
Recovery
Simulation
Security

Sensitive credentials should never be committed to GitHub.

Environment variables should be used for API keys and other secrets.

Example:

GEMINI_API_KEY=your_key_here

The repository excludes local secret and environment files through .gitignore.

Design Principles

CityPulse follows several core principles:

1. Glanceable

Important information should be understandable within seconds.

2. Evidence-Driven

Alerts should be backed by structured civic evidence.

3. Multi-Signal

Important events should not depend on only one metric.

4. Temporal

The system should understand how conditions evolve.

5. Spatial

The system should understand where conditions are occurring.

6. Explainable

Users should be able to understand why something was flagged.

7. Epistemically Honest

Observed facts, possible relationships, and simulations should remain clearly separated.

8. Citizen-Centric

The final output should be useful to people, not only machines.

Why CityPulse?

Traditional dashboards often answer:

"What is the current number?"

CityPulse aims to answer:

"What is happening, where is it happening, why is it important, what evidence supports it, and how is it evolving?"

That is the core idea behind CityPulse.

Team
Member 1 — AI / ML + Civic Intelligence

Responsible for:

Synthetic Civic Data
Statistical Detection
ML Anomaly Detection
Feature Engineering
Temporal Reasoning
Change-Point Detection
Ensemble Intelligence
Early Warning
Event Intelligence
Risk Intelligence
Recovery
Member 2 — Backend + Agentic AI

Responsible for:

Backend APIs
Civic AI Agent
Investigation Tools
Zone Comparison
Evidence Retrieval
Grounded GenAI
Simulation
Member 3 — Frontend + User Experience

Responsible for:

Command Center UI
Risk Visualization
Incident Map
Event Graph
Citizen Experience
Safety Features
Interactive Controls
Dashboard Presentation
Project Vision
