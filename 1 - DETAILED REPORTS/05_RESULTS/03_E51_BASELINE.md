# E51 Baseline Context

## Purpose

E51 is retained as a comparable fresh-initialization offline baseline. It helps interpret the final E50 command-model result but does not replace E50 and is not a second final Raspberry Pi deployment benchmark.

## Comparison Summary

| Model | Parameters | Weights size | Initialization | Selected evidence role |
|---|---:|---:|---|---|
| E51 comparable baseline | 66,483 | 251,009 bytes | Fresh initialization | Offline same-architecture comparison baseline. |
| Final E50 | 66,483 | 251,734 bytes | Mapped E41 initialization | Final selected command model. |

Documented comparison evidence reports E51 current95-compatible 77/90 = 85.56%, phase_av-compatible 131/194 = 67.53%, combined revised test 2727/4230 = 64.47%, and phase_av accepted precision 89.61%. Final E50 reports current95-compatible 83/90 = 92.22%, phase_av-compatible 139/194 = 71.65%, combined revised test 2724/4230 = 64.40%, phase_av accepted precision 91.92%, and final physical Pi end-to-end action success 10/19 = 52.63%.

## Boundary

E51 should be cited only as comparative offline evidence. It is not the deployed VCM, not the final runner, not an E37/E40 replacement, and not evidence that E53 superseded E50.

## Relationship To E50

E50 remains the frozen final command model with identity `E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT`. E51 supports comparison and sanity-checking of development choices; it is not the final system identity.
