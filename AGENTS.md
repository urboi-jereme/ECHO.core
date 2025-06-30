🧠 AGENTS.md — ECHO.Core Agent Reference

This document provides an overview of each symbolic agent in ECHO.Core, detailing their responsibilities, inputs, and outputs. This acts as a human- and Codex-readable API for reasoning agents.


---

🧠 Active Agents

Agent Name	Description	Inputs	Outputs

IntuitionAgent	Detects symbolic resonance in memory	ECHO_MEMORY.yaml	Top motifs ranked by resonance
NavigatorAgent	Proposes next prompts, actions, and recursion paths	Intuition output	Symbolic prompt list, proposed actions
ModulatorAgent	Adjusts agent weights based on symbolic and meta-pressure	META_PREFERENCES.yaml, MOTIF_PRESSURE.yaml	Updated AGENT_STATE.yaml
CuriosityAgent	Generates questions from unresolved motifs	MOTIF_PRESSURE.yaml, GOALS.yaml, motif filters	Question list
GoalEngine	Loads, stores, and tracks symbolic goal state	GOALS.yaml, AGENT_STATE.yaml	Filtered goals
MotifPressureTracker	Calculates pressure from unresolved memory motifs	ECHO_MEMORY.yaml	MOTIF_PRESSURE.yaml
BeliefInputAgent  Reflects on new belief candidates based on motif resonance    ECHO_MEMORY.yaml, MOTIF_PRESSURE.yaml    BELIEFS.yaml updated with suggestions
MotifDashboard   Visualize motif pressure and recent activations  MOTIF_PRESSURE.yaml, emergence_log.yaml  Console dashboard
EmergenceScanner   Scan memory, goals, and beliefs for emergence motifs   ECHO_MEMORY.yaml, GOALS.yaml, BELIEFS.yaml   Updates emergence_log.yaml



---

🌀 Planned/Future Agents

Agent Name	Planned Role

ObserverAgent	Detect symbolic paradox, drift, or contradiction across time
MirrorAgent	Reinterpret past memory with new symbolic frames (uses `memory/RECURSIVE_ALIGNMENTS.yaml` to track echoes)
EchoMetaAgent	Maintain recursive self-awareness and continuity across loops
InsightHistoryAgent	Reveal long-term symbolic arcs and changes in motif dynamics



---

🔄 Agent Lifecycles

Each agent is instantiated within echo_main.py, receiving shared context or symbolic state. Some agents operate in parallel, others run serially in loop:

IntuitionAgent → NavigatorAgent → ModulatorAgent → CuriosityAgent

GoalEngine runs passively for state lookup


Agents do not act independently; they are recursively called as functions of symbolic state.

