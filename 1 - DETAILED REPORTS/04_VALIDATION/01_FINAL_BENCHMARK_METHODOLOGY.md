# Final Benchmark Methodology

## Benchmark Scope

The final physical Raspberry Pi benchmark tested the frozen E50 VCM as an integrated runtime stack:

```text
wake phrase
  -> E37 wake gate
  -> command capture
  -> E50 command CNN
  -> E40 confidence policy
  -> deterministic router
  -> local action / response
  -> return to listening
```

The benchmark used 20 trials: one representative trial for each of the 19 final E50 command labels plus one UNKNOWN/no-action trial.

## Metric Definitions

| Metric | Definition |
|---|---|
| Wake success | E37 accepted wake during the trial. |
| Valid-command wake success | E37 accepted wake on valid command-label trials only. |
| Raw command classification | E50 top predicted label matched the expected command label before considering E40 acceptance. |
| E40 acceptance | Predicted label passed the applicable confidence threshold. |
| Accepted-correct | Accepted valid command produced the correct corresponding action. |
| Accepted-wrong | Accepted valid command produced a wrong action. |
| Accepted-action precision | Accepted-correct / accepted executed valid commands. |
| Safe rejection | Non-executed cases produced no routed command action. |
| End-to-end action success | Correct label, accepted by policy, correct local action/response behavior, and return-to-listening. |
| UNKNOWN/no-action safety | Unsupported input produced no command action. |
| Return-to-listening | Runtime returned to the listening state after the trial. |

## Why The Metrics Are Separate

Raw classification, acceptance, action correctness, safe rejection, and return-to-listening are different layers of the system. A model can classify correctly but be rejected by E40. A model can classify incorrectly but still avoid a wrong action if E40 rejects. A command can be callable but not demo-ready or statistically validated. The final benchmark should therefore be read as a layered system test, not a single generic accuracy number.

## Benchmark Limitations

Because the final benchmark has one valid trial per label, it does not establish statistically meaningful per-intent metrics. It also does not establish broad robustness across speakers, rooms, microphones, background audio, phrasing variations, or reverberation conditions.
