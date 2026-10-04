# Limitations

## Purpose

This page collects the main evidence boundaries for the final E50 VCM. These are not corrections to the results; they define what the reviewed evidence does and does not establish.

## Established Scope

The project establishes a frozen offline Raspberry Pi VCM prototype with E37 wake detection, E50 fixed-vocabulary command classification, E40 confidence gating, deterministic local routing, local response audio, and return-to-listening behavior. The final physical Pi benchmark establishes the measured results for a 20-trial population: 19 valid command trials and one UNKNOWN/no-action trial.

## Main Limitations

- Raw command classification was moderate: 13/19 = 68.42% on valid command trials.
- End-to-end action success was moderate: 10/19 = 52.63% on valid command trials.
- The final physical benchmark used one valid trial per label, so it does not establish statistically meaningful per-intent metrics.
- Broad environmental wake false-accept rate over arbitrary background/no-wake audio is not established.
- Formal statistically characterized unseen-human-speaker physical-Pi benchmark is not established.
- Full wake-to-action latency is not established.
- Full wake-to-response latency is not established.
- Acoustic speaker-onset latency is not established.
- Full acoustic end-to-end RTF is not established.
- Final calibration/ECE metric is not established.
- Broad noise/reverberation robustness is not established.
- Systematic phrasing-variation robustness is not established.
- Unrestricted dataset redistribution rights are not established as a blanket claim.
- Exact final E37 training-row membership, E37 epochs, optimizer, validation metrics, augmentation count, and complete row-to-checkpoint mapping are not established.

## Counterbalancing Established Result

Within the tested final benchmark population, the accepted action path was conservative: accepted-wrong was 0, accepted-action precision was 10/10 = 100%, safe rejection among non-executed cases was 10/10 = 100%, UNKNOWN/no-action safety was 1/1 = 100%, and return-to-listening was 20/20 = 100%.
