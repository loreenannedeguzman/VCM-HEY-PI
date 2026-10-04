# Requirements Traceability

| Requirement | E50 implementation evidence | Validation / result evidence | Status |
|---|---|---|---|
| Offline local VCM | Fixed E37/E50/E40 stack, deterministic router, local response audio. | Final Pi validation and deployability records. | Established for frozen core. |
| Wake phrase before command | E37 wake gate precedes command capture. | Final benchmark reports wake success over the 20-trial Pi population. | Established with measured limitations. |
| 19-command vocabulary | Final E50 vocabulary contains PLAY_MUSIC, WEATHER, TIME, LIGHT_ON, LIGHT_OFF, LIGHT_DIM, BRIGHTNESS, TIMER, ALARM, TEMPERATURE, NEXT, PAUSE, STOP, VOLUME_UP, VOLUME_DOWN, CREATE_REMINDER, LIST_REMINDERS, CALL, MESSAGE. | Final benchmark uses the 19 valid labels plus one UNKNOWN/no-action trial. | Established. |
| Safe rejection | E40 confidence policy rejects low-confidence outputs before routing. | Safe rejection among non-executed final benchmark cases is reported as 10/10. | Established for tested cases. |
| Deterministic actions | Accepted labels route to predefined local actions and response audio. | Accepted-action precision is reported as 10/10. | Established for accepted tested cases. |
| Raspberry Pi deployment | Pi 5 package root, runner, microphone, local audio output, and GUI/core boundary are documented. | Deployment evidence is documentary; this compilation did not execute the runtime. | Documented, not rerun. |
| Latency/RTF reporting | CNN latency, CNN RTF, command-pipeline RTF, and response playback-start latency are recorded. | Results section records final values and measurement boundaries. | Established within measurement definitions. |
| Dataset provenance | E50 command data uses selected collective-family material plus project-specific additions; E37 wake recordings are separate project-specific Pi recordings. | Dataset/provenance audits and E37 recovery audit. | Established with stated limitations. |
| E53 separation | E53 is documented as an independent experiment, not the deployed E50 system. | Independent experiment section. | Established. |

## Limitations

The package does not claim that E37's exact final training rows are fully reconstructed, that E50 used the entire collective Gold Dataset unchanged, or that E53 replaced E50. These exclusions are intentional evidence boundaries.
