# Validation Evidence Boundaries

## Established

- Final physical Pi benchmark population: 20 trials.
- Valid command trials: 19.
- UNKNOWN/no-action trials: 1.
- Wake success, raw command classification, E40 acceptance, accepted-action precision, safe rejection, UNKNOWN/no-action safety, and return-to-listening for the tested population.
- CNN-only Raspberry Pi inference latency and RTF.
- Qualified response playback-start latency over 5 accepted/executed trials.
- Bounded command-window false-accept result over the tested out-of-scope prompts.
- E51 as an offline comparison baseline, not a deployed replacement.

## Not Established

- Broad environmental wake false-accept rate over arbitrary background/no-wake audio.
- Formal statistically characterized unseen-human-speaker physical-Pi benchmark.
- Full wake-to-action latency.
- Full wake-to-response latency.
- Acoustic speaker-onset latency.
- Full acoustic end-to-end RTF.
- Final calibration/ECE metric.
- Broad noise/reverberation robustness.
- Systematic phrasing-variation robustness.
- Statistically meaningful per-intent physical-Pi metrics from one trial per label.
- Unrestricted dataset redistribution rights as a blanket claim.
- Exact final E37 training-row membership.

## Reporting Rule

Use established metrics directly, but do not broaden them. For example, `0/4` bounded command-window false accepts is not the same as a broad environmental FAR claim, and CNN-only latency is not the same as full acoustic wake-to-action latency.
