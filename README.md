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
