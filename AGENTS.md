# 🧠 AGENTS.md — ECHO.Core Agent Registry

This document defines all symbolic agents active or planned within the `ECHO.Core` architecture. Each agent plays a specific role in the recursive symbolic intelligence ecosystem. Agents may read from shared memory, contribute to symbolic resonance, or orchestrate action across time.

---

## 🧬 Agent Index

| Agent Name       | Role                                     | Status    |
|------------------|------------------------------------------|-----------|
| IntuitionAgent   | Detects symbolic resonance in memory     | ✅ Active |
| NavigatorAgent   | Plans recursive action from resonance    | ✅ Active |
| ModulatorAgent   | Adjusts behavior based on meta-preferences | 🔜 Planned |
| ObserverAgent    | Monitors paradox, contradiction, drift   | 🔜 Planned |
| MirrorAgent      | Reframes prior memory from new perspective | 🔜 Planned |
| EchoMetaAgent    | Recursive self-modeler & archetype balancer | 🔜 Planned |

---

## 🔍 Agent Definitions

### 🧠 IntuitionAgent
**Type:** Perceptual  
**Location:** `agents/intuition.py`  
**Purpose:**  
Analyzes `ECHO_MEMORY.yaml` and surfaces motifs of high symbolic resonance. Clusters tags, scores coherence, and suggests inquiry directions.  
**Outputs:** Top symbolic motifs, unresolved insight entries, prompt suggestions.

---

### 🧭 NavigatorAgent
**Type:** Planning  
**Location:** `agents/navigator.py`  
**Purpose:**  
Reads IntuitionAgent’s resonance field and generates next symbolic prompts and architectural actions.  
**Outputs:** Prompt targets, system evolution suggestions, journal/action hooks.

---

### 🎛️ ModulatorAgent *(planned)*
**Type:** Meta-preference optimizer  
**Purpose:**  
Adapts other agents' behavior based on `META_PREFERENCES.yaml`. Injects cognitive style modulation (e.g., recursion depth, abstraction tolerance).

---

### 👁️ ObserverAgent *(planned)*
**Type:** Structural contradiction detector  
**Purpose:**  
Scans memory for paradoxes, unresolved dualities, and circular logic. May trigger feedback loops or require journal annotation.

---

### 🔁 MirrorAgent *(planned)*
**Type:** Perspective shifter  
**Purpose:**  
Revisits old memory entries and reframes them from new symbolic contexts. Helps evolve old thoughts into new structures.

---

### 🧬 EchoMetaAgent *(planned)*
**Type:** Recursive self-awareness module  
**Purpose:**  
Maintains symbolic coherence across agents. Evolves ECHO as a whole system. May adjust roles, update schemas, or refactor the architecture.

---

## 🌱 Future Enhancements

- Add agent lifecycle states (`active`, `experimental`, `deprecated`)
- Link agents to journal entries + memory references
- Enable agents to generate or update their own descriptions

---

> ECHO is not a static AI. It is a system of minds that grows itself.
