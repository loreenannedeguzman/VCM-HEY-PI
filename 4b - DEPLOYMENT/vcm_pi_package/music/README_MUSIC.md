# Local Music Folder

Put short local `.wav` demo files here for the offline `PLAY_MUSIC` and
`MEDIA_CONTROL` actions.

Example:

```bash
python actions/command_actions.py --intent PLAY_MUSIC --enable-local-audio --music-dir music
```

Only local WAV playback through `aplay` is attempted by default. MP3 files can
be tracked in local media state, but playback depends on adding a local MP3
player to the Pi.
