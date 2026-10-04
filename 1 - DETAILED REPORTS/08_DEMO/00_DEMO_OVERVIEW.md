# Demo Overview

## Purpose

This section provides the operational demo view of the frozen E50 voice-command module. It explains what the operator does, what the system should do, and how demo behavior relates to the frozen core.

## Demo System Boundary

The demo uses the frozen E50 VCM core through the deployment interface. The post-freeze enhanced DUi/GUI may present prompts or status around the core, but it is not a new model and does not change E37, E50, E40, vocabulary, thresholds, routing semantics, or benchmark identity.

## Operator Flow

1. Start from the deployed Pi package/interface.
2. Say the wake phrase: `Hey Pi`.
3. Wait for the command window.
4. Say one supported command phrase.
5. Observe local action/response behavior.
6. Confirm the system returns to listening.

## Demonstrated Capabilities

The demo is intended to show wake-gated operation, fixed-vocabulary command recognition, confidence-based rejection, deterministic routing, local response audio, UNKNOWN/no-action safety, and return-to-listening behavior.
