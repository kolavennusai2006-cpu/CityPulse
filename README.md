# CityPulse — AI Civic Intelligence OS

> **Detect. Connect. Investigate. Explain. Simulate.**

CityPulse is an AI-powered civic intelligence platform designed to turn fragmented urban signals into one clear and understandable picture of what is happening across a city.

Instead of viewing weather, traffic, transit delays, citizen complaints, air quality, and civic events separately, CityPulse combines these signals, analyzes their changes over time and location, detects unusual patterns, reconstructs emerging civic events, and explains the evidence in plain language.

---

## 🚀 Live Demo

🔗 **[Open CityPulse Dashboard](https://kolavennusai2006-cpu.github.io/CityPulse/)**

🔗 **[GitHub Repository](https://github.com/kolavennusai2006-cpu/CityPulse)**

---

# 💡 The Idea

### One glance should tell a resident:

- What is happening?
- Where is it happening?
- Why was it flagged?
- How serious is it?
- What evidence supports it?
- What changed over time?
- What could happen under a simulated scenario?

CityPulse follows the intelligence loop:

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

🚨 Problem Statement

Urban civic information is fragmented across multiple systems.

Weather conditions, traffic congestion, public transit delays, citizen complaints, air quality, incidents, and other civic signals may exist separately with different formats, timestamps, update rates, and reliability.

This creates two major problems:

Residents do not have a single, understandable view of what is happening around them.
Important relationships and emerging patterns can be difficult to identify when every signal is viewed independently.

CityPulse addresses this by creating a unified civic intelligence layer:

Collect
  ↓
Validate
  ↓
Normalize
  ↓
Analyze
  ↓
Connect
  ↓
Detect
  ↓
Explain
  ↓
Simulate
🧠 16-Layer CityPulse Architecture

CityPulse is built around a 16-layer AI Civic Intelligence architecture.

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

CityPulse is designed to process multiple civic data streams:

Weather
Traffic
Transit
Complaints
AQI
Events

Different sources may produce information in different formats and at different time intervals.

2. Data Quality Engine

Incoming data is evaluated before entering the intelligence pipeline.

The layer considers:

Validation
Missing Data
Outliers
Source Health
Timestamp Consistency

This helps reduce the effect of incomplete or abnormal source data.

3. Normalization Engine

Different civic feeds are converted into a common representation:

zone
timestamp
signal
value
source

This common model allows downstream intelligence modules to process signals consistently.

4. Civic Digital Twin

CityPulse maintains a simplified digital representation of the monitored city.

Each zone contains:

Current State
Signal State
Historical State
Baseline
Trend
Risk
Events
Jaipur Demonstration Zones
Internal ID	Display Area
ZONE_A	Pink City Core
ZONE_B	Malviya Nagar
ZONE_C	Vaishali Nagar
ZONE_D	C-Scheme
ZONE_E	Sanganer

Internal IDs are used for system processing while the dashboard uses human-friendly area names.

5. Multi-Layer Anomaly Engine

CityPulse combines multiple anomaly-detection approaches.

Statistical Baseline

Detects deviations from expected signal behavior.

Machine Learning

Uses ML-based anomaly detection to identify unusual civic patterns.

Temporal Rules

Detects abnormal signal changes across successive observations.

Spatial Detection

Adds geographic context to unusual conditions.

Change-Point Detection

Identifies significant shifts in civic signal behavior.

These outputs are combined into an:

ANOMALY ENSEMBLE
6. Temporal Reasoning Engine

CityPulse analyzes how civic signals evolve over time.

The temporal layer considers:

Persistence
Acceleration
Trend
Change Point
Early Warning

This helps distinguish temporary fluctuations from conditions that continue or intensify.

7. Cross-Signal Fusion

CityPulse looks for convergence between different civic signals.

It evaluates:

Signal Count
Time Overlap
Spatial Overlap
Convergence Score

For example, rainfall, traffic congestion, transit delays, and citizen complaints increasing during a similar time window can form a stronger combined civic signal than one metric viewed alone.

8. Event Intelligence

Related anomalies are grouped into structured civic events.

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
Event Lifecycle
START
  ↓
DEVELOPING
  ↓
ESCALATING
  ↓
PEAK
  ↓
RECOVERING

This allows CityPulse to communicate how an incident is evolving instead of showing only a single alert.

9. Civic Event Graph

CityPulse connects related civic signals into an event graph.

              WEATHER
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
     TRAFFIC   TRANSIT  COMPLAINTS
        │        │        │
        └────────┼────────┘
                 ↓
            CIVIC EVENT

The graph represents:

Observed Signals
Temporal Relationships
Spatial Relationships
Possible Relationships
⚠️ Correlation is not automatically treated as causation.

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
Risk Levels
Risk Score	Status
0–29	NORMAL
30–49	WATCH
50–74	EMERGING
75–100	CRITICAL
11. Agentic AI Layer

CityPulse includes a Civic AI Agent for structured civic investigation.

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

The goal is to make the AI investigate the available evidence instead of generating unsupported answers.

12. Evidence Memory

CityPulse maintains structured civic context through:

Event Memory
Historical Memory
Evidence Store

This supports investigation, event replay, and historical analysis.

13. Grounded GenAI

The generative AI layer works from structured civic evidence.

Structured Evidence
        ↓
Civic Intelligence Context
        ↓
Grounded GenAI
        ↓
Civic Intelligence Brief

The brief focuses on:

What happened?
Why was it flagged?
What changed?
Which signals are involved?
What evidence supports the alert?
What remains uncertain?
14. What-If Simulation

CityPulse supports hypothetical scenario analysis.

Users can modify selected civic inputs such as:

Rainfall
Traffic
Transit Delay

Simulation flow:

USER SCENARIO
      ↓
RECOMPUTE CIVIC STATE
      ↓
RECOMPUTE RISK
      ↓
PROJECT CONSEQUENCES

All hypothetical outputs are explicitly labelled:

SIMULATED — NOT OBSERVED
15. Time Machine

CityPulse includes historical replay for understanding how events evolve.

PAST
 │
 ├── -30 min
 ├── -15 min
 ├── NOW
 └── FUTURE SCENARIO

The Time Machine can examine:

Historical Snapshots
Event Evolution
Risk Changes
Signal Changes
Recovery
16. Civic Command Center

The final intelligence is presented through a unified dashboard.

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
Design Goal

Understand the city's civic state in seconds, then investigate deeper when needed.

🌆 Key Features
Live Civic Pulse

Provides a consolidated view of current civic conditions.

Priority Alerts

Makes important civic conditions immediately visible.

Risk Map

Shows civic risk across monitored zones.

Zone Intelligence

Allows users to inspect the signals contributing to a zone's status.

Event Graph

Connects related civic signals into one event context.

Historical Risk Profile

Provides historical context for significant or recurring conditions.

Event Replay

Shows how an event changes across multiple observations.

Citizen Reporting

Residents can report:

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

Provides a simple way to assess current civic conditions before or during travel.

Ask CityPulse

Users can ask questions about monitored civic conditions and receive evidence-based responses.

What-If Simulation

Users can modify selected conditions and view the resulting simulated civic risk.

🧪 Current Demonstration

The current demonstration uses a structured multi-signal civic scenario.

Example signals:

Rainfall
Traffic
Transit Delay
Citizen Complaints

The intelligence pipeline processes these signals through:

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

This demonstrates how CityPulse can detect, investigate, explain, simulate, and replay a developing civic disruption.

🌍 Real-World Data Integration

The architecture is designed to support verified external civic sources for:

Weather
Disaster Alerts
Air Quality
Traffic
Transit
Citizen Complaints
Civic Events
News

External feeds can follow the same processing pipeline:

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

This allows the architecture to extend from synthetic demonstrations toward real-world civic intelligence.

🔎 Data and Epistemic Honesty

CityPulse distinguishes between:

OBSERVED
SIMULATED
REPORTED
VERIFIED

The platform is designed not to present an inferred relationship as confirmed causation.

For example:

Observed

Rainfall, traffic congestion, and transit delays increased during the same observation window.

Not automatically claimed

Rainfall caused the traffic disruption.

Instead, CityPulse communicates:

Possible relationship
Observed association
Temporal overlap
Spatial overlap
Not confirmed causation

This distinction is especially important for a public-facing civic intelligence system.

🛠️ Technology Stack
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
📁 Project Structure
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
├── index.html
├── index (3).html
├── script (2).js
├── style (2).css
├── README.md
└── .gitignore
▶️ Running the Project Locally
Frontend

Run the dashboard using VS Code Live Server.

Main dashboard:

index (3).html

The root index.html acts as the deployment entry point for GitHub Pages.

Node Backend
cd Backend
npm install
npm start
Python Intelligence Engine

Open another terminal:

cd Python_Engine
python server.py
🔌 API

Primary CityPulse endpoint:

GET /api/citypulse

The API provides consolidated CityPulse intelligence for the dashboard.

Additional capabilities include:

Investigation
Explanation
Verification
Zone Comparison
Event Timeline
Event Evidence
Recovery
Simulation
🔐 Security

API keys and secrets should never be committed to GitHub.

Use environment variables for sensitive credentials.

Example:

GEMINI_API_KEY=your_key_here

Local environment and secret files are excluded through .gitignore.

🎯 Design Principles
1. Glanceable

Important information should be understandable within seconds.

2. Evidence-Driven

Alerts should be supported by structured civic evidence.

3. Multi-Signal

Important civic events should not depend on a single metric.

4. Temporal

The system should understand how conditions evolve.

5. Spatial

The system should understand where conditions are occurring.

6. Explainable

Users should understand why something was flagged.

7. Epistemically Honest

Observed facts, possible relationships, and simulations remain clearly separated.

8. Citizen-Centric

The final intelligence should be useful to citizens and stakeholders, not only machines.

👥 Team Contributions
Member 1 — AI / ML + Civic Intelligence Engine

Responsible for the intelligence and analytical core:

Synthetic Civic Data
Feature Engineering
Statistical Detection
ML Anomaly Detection
Temporal Reasoning
Change-Point Detection
Ensemble Intelligence
Early Warning
Event Intelligence
Risk Intelligence
Event Lifecycle
Recovery Analysis
Core Responsibility

Transform raw civic signals into structured intelligence, anomalies, events, risk, evidence, and recovery states.

Member 2 — Backend + Agentic AI

Responsible for the backend and AI investigation layer:

Backend APIs
Civic AI Agent
Investigation Tools
Zone Comparison
Evidence Retrieval
Grounded GenAI
Civic Brief
Simulation
Core Responsibility

Connect the intelligence engine with the application and provide investigation, explanation, verification, comparison, simulation, and grounded AI capabilities.

Member 3 — Frontend + User Experience

Responsible for the citizen-facing command center:

Dashboard Interface
Live Pulse
Risk Visualization
Incident Map
Event Graph
Historical Risk Profile
Event Replay
Citizen Reporting
Safety Checker
Interactive Controls
What-If Interface
Dashboard Presentation
Core Responsibility

Convert complex civic intelligence into a professional, glanceable, interactive interface that citizens and stakeholders can understand quickly.

🏆 Why CityPulse?

Traditional dashboards often answer:

"What is the current number?"

CityPulse aims to answer:

"What is happening, where is it happening, why is it important, what evidence supports it, and how is it evolving?"

That is the core idea behind CityPulse.

🚀 Project Vision

CityPulse is designed to evolve from a hackathon prototype into a broader civic intelligence platform capable of combining urban signals, detecting emerging disruptions, investigating their evidence, explaining them clearly, and exploring hypothetical scenarios.

DATA
  ↓
INTELLIGENCE
  ↓
CIVIC AWARENESS
  ↓
BETTER DECISIONS
