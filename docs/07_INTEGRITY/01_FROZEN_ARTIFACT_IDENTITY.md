# Frozen Artifact Identity

| Component | Frozen identity |
|---|---|
| E50 command model | E50_BG_REVISED_VOCAB_ORIGINAL_PRESERVE_E41_INIT |
| E50 weights SHA256 | BC8AC64CED4305DDF43BF4DE377F3CC636A764EFF339CD9F92AF06340C50B8FF |
| E37 wake model | E37_TARGETED_COLOR_VOLUME_FIX |
| E37 weights SHA256 | 687E82E2CEFA6D74CEF2C0A15D28F8F6142D47D4A67E57C68C091E83FC2CEBDE |
| E37 normalization SHA256 | 3BFA93F202DC0C241E577E5B89506F2CB6D0F35B8239297C215A7F81E970B4C7 |
| E40 policy | E40_NON_LED_COMMAND_GUARDRAIL_THRESHOLDS |
| E40 policy SHA256 | A0B2495328FD5A1E0E5885E727623BA6D9F823BE94CCCDFD0AEAD77254BBB3FD |
| Wake threshold | 0.90 |
| Command default threshold | 0.90 |
| Final runtime launcher | scripts/run_vcm_touchscreen_gui.sh |

## Final Vocabulary

PLAY_MUSIC, WEATHER, TIME, LIGHT_ON, LIGHT_OFF, LIGHT_DIM, BRIGHTNESS, TIMER, ALARM, TEMPERATURE, NEXT, PAUSE, STOP, VOLUME_UP, VOLUME_DOWN, CREATE_REMINDER, LIST_REMINDERS, CALL, MESSAGE.

`COLOR` is a historical/E37 target-context label and is not the final E50 command class.

## Frozen Boundary

The frozen E50 VCM core consists of the E37 wake model, command capture, preprocessing, E50 CNN, E40 confidence policy, deterministic router, local actions, response audio, and return-to-listening behavior. The enhanced DUi/GUI is a post-freeze interface layer and does not alter these frozen identities.

