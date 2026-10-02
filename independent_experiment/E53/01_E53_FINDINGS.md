# E53 Findings

## Experiment Summary

E53/VCM2 investigated a separate command-recognition dataset and model family. It examined small CNN classifiers and feature choices including log-Mel, MFCC, and PCEN representations.

## Documented Control Result

For the LOG011 control, the documented values are:

| Metric | Value |
|---|---:|
| Test accuracy | 0.463779 |
| Macro F1 | 0.410447 |
| Weighted F1 | 0.445472 |
| UNKNOWN F1 | 0.922756 |
| SILENCE F1 | 0.585242 |

## Observed Experimental Issues

The documented experiment retained unresolved command-pair confusions including LIST_REMINDERS/CREATE_REMINDER and VOLUME_UP/VOLUME_DOWN. It also showed tradeoffs between operational command recognition and UNKNOWN/SILENCE handling.

## Not Established

E53 did not establish a final Pi deployment, GUI operation, router/action integration, response playback, network-off standalone operation, Section 68 completion, or replacement of E50.
