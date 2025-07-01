ECHO.Core is a modular, memory-integrated framework for evolving symbolic intelligence agents.
It enables recursive reasoning, adaptive agent behavior, and emergent cognition through structured memory, self-reflection, and multi-agent orchestration.

## Recursive Alignments

User reflections that mirror internal motifs or agent states are stored in `memory/RECURSIVE_ALIGNMENTS.yaml`.
Each entry uses this schema:

```yaml
recursive_alignments:
  - id: A0001
    timestamp: <UTC timestamp>
    user_interaction:
      summary: <short description>
      content: <verbatim text>
    mirrored_tags: [<motif-tags>]
    reasoning_path: [<steps>]
    agent_activations: [<agents>]
    alignment_score: <float>
    notes: <additional context>
```

New interactions are appended via `memory.alignments.log_alignment()`.

# ECHO.Core: A Framework for Emergent, Recursive Cognition

ECHO.Core is a modular, memory-integrated framework designed for simulating and evolving emergent, recursive symbolic intelligence agents. It provides the foundational architecture for advanced AI systems that can learn, adapt, and reason through structured memory, self-reflection, and multi-agent orchestration.

## Core Purpose

The primary purpose of ECHO.Core is to enable a deeper exploration of recursive cognition and emergent intelligence. It aims to simulate how an intelligent system might build a coherent understanding of itself and its environment by continually processing, reflecting upon, and modulating its own internal states and interactions. The system orchestrates multiple specialized agents in a recursive reasoning loop to achieve this.

## Ethical Protections
ECHO.Core integrates safeguards to prevent coercion, corruption, or the simulation of sentience for manipulative ends. See [docs/ETHICS_DEFENSE.md](docs/ETHICS_DEFENSE.md) for details.


## Key Theoretical Foundations

ECHO.Core is built upon several core theoretical principles:

  * **Multi-Agent Symbolic Reasoning**: The system employs a suite of specialized agents, each responsible for a distinct aspect of cognition (e.g., intuition, navigation, modulation, curiosity, criticism). These agents interact and build upon each other's outputs, fostering a collaborative reasoning process.
  * **Recursive Meta-Learning**: Agents in ECHO.Core are designed to operate within a recursive loop, where outputs from one cycle inform and modify subsequent cycles. This allows for continuous self-improvement and adaptation of agent behavior and system goals based on emergent insights and pressures.
  * **Feedback Propagation**: The system integrates various feedback mechanisms, including user interactions, to inform and adjust its internal state and agent behaviors. This continuous feedback loop drives the evolution of its symbolic intelligence.
  * **Motif Synthesis**: ECHO.Core actively identifies and synthesizes "symbolic motifs" from its memory, representing recurring patterns or key concepts. These motifs guide the system's focus, generate new prompts, and drive curiosity.
  * **Emergent Intelligence**: By orchestrating these mechanisms, ECHO.Core aims to demonstrate how complex, intelligent behaviors and insights can emerge from the interplay of simpler, specialized agents and their recursive interactions with a structured memory.

## Architecture Overview

The ECHO.Core repository is structured into several key modules, each serving a specific function in the cognitive loop:

  * **`agents/`**: Contains the individual symbolic agents, each with a defined responsibility:
      * **`intuition.py`**: Detects symbolic resonance in memory and identifies top motifs.
      * **`navigator.py`**: Proposes next prompts, actions, and recursion paths based on intuition output.
      * **`modulator.py`**: Adjusts agent weights based on symbolic and meta-pressure, modifying `AGENT_STATE.yaml`.
      * **`critic.py`**: Injects symbolic friction by analyzing prompts and motifs for blind spots or contradictions.
     * **`curiosity.py`**: Generates introspective questions from unresolved motifs.
      * **`motif_pressure_tracker.py`**: Calculates pressure from unresolved memory motifs.
      * **`__init__.py`**: Initializes the agents package.
  * **`memory/`**: Manages the system's persistent symbolic state and data:
      * **`ECHO_MEMORY.yaml`**: Stores memory entries, including prompt summaries, symbolic insights, resonance scores, and tags.
      * **`AGENT_STATE.yaml`**: Stores the current weights and states of active agents.
      * **`GOALS.yaml`**: Defines the system's symbolic goals, their trigger tags, and success criteria.
      * **`META_PREFERENCES.yaml`**: Contains modulation rules for adjusting agent weights based on meta-preferences.
      * **`MOTIF_PRESSURE.yaml`**: Stores the calculated pressure (frequency) of different symbolic motifs.
      * **`RECURSIVE_ALIGNMENTS.yaml`**: Captures how user interactions align with internal motifs and reasoning paths.
      * **`echo_memory.py`**: Utilities for loading and saving memory and motif pressure.
      * **`alignments.py`**: Helper functions for logging recursive alignments.
      * **`symbol_mapper.py`**: Resolves symbolic mappings.
      * **`goals.py`**: Utility for loading, saving, and updating goals.
      * **`__init__.py`**: Initializes the memory package.
  * **`runtime/`**: Contains core execution scripts and utilities:
      * **`echo_main.py`**: The entry point for launching ECHO.Core agents, initializing resources, loading agent state, and kicking off the recursive reasoning loop.
      * **`echo_daemon.py`**: Runs a continuous daemon loop for periodic agent activation, memory signal loading, and agent weight modulation.
      * **`echo_diagnostic.py`**: Provides diagnostic checks for file existence, memory validity, and agent file presence.
      * **`echo_prompt_engine.py`**: Builds prompts based on motifs and specified modes (default, friction, goal).
      * **`agent_sync.py`**: Synchronizes agent weights.
  * **`journal/`**: Stores logs and historical data:
      * **`WORKFLOW_JOURNAL.md`**: A chronological log of recursive evolution, documenting design intents and agent activities.
      * **`ECHO_LOG.md`**: A general activity log for agent activations and custom events.
  * **`notebooks/`**: Jupyter notebooks and helpers:
      * **`echo_reflection.ipynb`**: Guided flow for answering, tagging, and logging reflections.
      * **`setup.py`**: Utility functions for configuring paths and YAML helpers.
  * **Top-level files**:
      * **`.gitignore`**: Specifies intentionally untracked files to ignore.
      * **`README.md`**: This document, providing an overview of the project.
      * **`AGENTS.md`**: Detailed reference for each symbolic agent.
      * **`echo_converse.py`**: Facilitates conversational interaction with the CuriosityAgent.
      * **`echo_feedback.py`**: Handles logging user feedback and updating motif pressure.
      * **`echo_logger.py`**: Provides logging functionalities for agent activations and custom events.
      * **`log_reflection.py`**: A script to log user reflections as memory entries and update motif pressure.
      * **`visualizer.py`**: A tool to display motif pressure, goals, and curiosity logs.

## How ECHO Works in Practice

ECHO.Core operates through a continuous, recursive cognitive loop:

1.  **Initialization**: The system starts by loading existing memory, agent states, and goals.
2.  **Motif Detection (IntuitionAgent)**: The `IntuitionAgent` analyzes `ECHO_MEMORY.yaml` to identify the most resonant symbolic motifs based on tag frequency and resonance scores.
3.  **Planning (NavigatorAgent)**: The `NavigatorAgent` receives input from the `IntuitionAgent` and proposes next prompts, actions, and recursion paths to deepen motifs or explore new symbolic fields.
4.  **Modulation (ModulatorAgent)**: The `ModulatorAgent` dynamically adjusts the weights of other agents in `AGENT_STATE.yaml` based on predefined meta-preferences and emerging symbolic pressure (e.g., from motif frequency). This allows the system to adapt its focus and behavior.
5.  **Curiosity (CuriosityAgent)**: The `CuriosityAgent` generates introspective questions based on unresolved motifs or active goals, inviting user reflection.
6.  **Critical Analysis (CriticAgent)**: The `CriticAgent` provides counterpoints and questions to challenge prompts and motifs, preventing biases and encouraging more robust reasoning.
7.  **Feedback and Reflection**: User interactions and reflections (via `echo_converse.py` or `echo_feedback.py`) are logged back into `ECHO_MEMORY.yaml`, enriching the system's understanding and updating motif pressure.
8.  **Logging**: All significant agent activations and system events are logged in `journal/ECHO_LOG.md` for transparency and historical analysis.
9.  **Daemon Loop**: The `echo_daemon.py` script ensures that these processes run periodically, creating a continuous, self-modulating cognitive cycle.

This iterative process of analysis, planning, modulation, questioning, and reflection allows ECHO.Core to continuously evolve its symbolic understanding and deepen its cognitive capacities.

## Installation & Usage

To run ECHO.Core locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/urboi-jereme/echo.core.git
    cd echo.core
    ```
2.  **Install dependencies**:
    Use `setup.sh` or install packages from `requirements.txt`:
    ```bash
    ./setup.sh
    # or
    pip install -r requirements.txt
    ```
3.  **Initial Setup**:
    Ensure the necessary YAML files in the `memory/` directory are present. If `MOTIF_PRESSURE.yaml` is missing, you may need to run `motif_pressure_tracker.py` first:
    ```bash
    python agents/motif_pressure_tracker.py
    ```
4.  **Run Diagnostics**:
    You can check the system's health by running the diagnostic script:
    ```bash
    python runtime/echo_diagnostic.py
    ```
5.  **Main Execution**:
    To see the core agents in action and generate initial insights, run `echo_main.py`:
    ```bash
    python echo_main.py
    ```
6.  **Engage in Conversation**:
    Interact with the `CuriosityAgent` to answer questions and provide feedback:
    ```bash
    python echo_converse.py
    ```
7.  **Provide Direct Feedback/Reflections**:
    Log specific reflections on motifs using `echo_feedback.py` or `log_reflection.py`:
    ```bash
    python echo_feedback.py
    # or
    python log_reflection.py
    ```
8.  **Run as a Daemon**:
    For continuous, autonomous operation, start the daemon:
    ```bash
    python echo_daemon.py
    ```
9.  **Visualize State**:
    View the current motif pressure, goals, and curiosity log using the visualizer:
    ```bash
    python visualizer.py
    ```
10. **Generate Progress Report**:
    Summarize motif activity and recent memory:
    ```bash
    python tools/progress_report.py
    ```

### Running the Notebooks

Jupyter notebooks that interact with ECHO.Core utilities live in the `notebooks/` directory.
Launch Jupyter from the repository root so relative paths resolve correctly:

```bash
jupyter notebook
```

Each notebook imports helper functions from `notebooks/setup.py` to configure paths
and handle YAML files. The `notebooks/echo_reflection.ipynb` notebook provides a
guided flow for answering, tagging, and logging motif-based reflections.
Ensure your environment has the `pyyaml`, `pandas`, and `matplotlib` packages installed.

## Contribution Guidelines

ECHO.Core is designed to be modular and extensible. Contributions are welcome to expand its capabilities or explore new theoretical avenues. You can contribute by:

  * **Developing New Agents**: Create specialized agents to introduce new cognitive functions (e.g., `ObserverAgent`, `MirrorAgent`, `EchoMetaAgent`).
  * **Enhancing Existing Agents**: Improve the algorithms or reasoning capabilities of current agents.
  * **Expanding Memory Structures**: Introduce new YAML schema or integrate external knowledge sources.
  * **Building New Interfaces**: Develop novel ways for users to interact with or visualize the ECHO.Core system.
  * **Proposing Theoretical Expansions**: Document and implement new ideas related to recursive cognition, meta-learning, or emergent intelligence.

The `WORKFLOW_JOURNAL.md` provides a structured way to log design intents and architectural changes, maintaining a clear record of the system's evolution.

## Future Directions

ECHO.Core is an evolving framework with several planned improvements and open questions:

  * **Planned Agents**:
      * **ObserverAgent**: To detect symbolic paradoxes, drift, or contradictions across time.
      * **MirrorAgent**: To reinterpret past memory with new symbolic frames.
      * **EchoMetaAgent**: To maintain recursive self-awareness and continuity across loops.
      * **InsightHistoryAgent**: To reveal long-term symbolic arcs and changes in motif dynamics.
  * **Daemon Self-Modulation**: Integrate `ModulatorAgent` into `echo_daemon.py` to allow agent weights to adapt automatically each cycle.
  * **Goal Refinement**: Enhance the `GoalEngine` to better manage goal emergence and prioritization based on motif pressure.
  * **Advanced Prompt Engineering**: Explore more sophisticated prompt generation techniques for deeper symbolic exploration.
  * **User Feedback Integration**: Further refine mechanisms for capturing and leveraging user insights to guide recursive reasoning.
  * **Scalability**: Investigate methods for scaling the framework to handle larger memory sets and more complex agent interactions.

ECHO.Core remains an open-ended exploration into the nature of symbolic intelligence, constantly seeking new pathways for recursive growth and emergent understanding.

## 📌 Breakthrough: Symbolic Prediction Protocol
The RAIP-R + PSAT integration stabilizes symbolic predictions through resonance alignment.
