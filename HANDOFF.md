# EA Excerpts — handoff

## v1 (12 Nov 2026)
- Built from the VocalPrep pattern: Capture (open file, markers, drag/double-tap select, Add to library) and Library.
- Library: waveform (L/R lanes) or sonogram (log/linear, FFT 2048/4096/8192, floor, top), both playable; tap to seek;
  hover/touch readout of Hz, nearest note and cents.
- 88-key keyboard (piano model from VocalPrep, or sine); note names + Hz under the keys (white row, black row), A4 = 440;
  a pressed key draws its frequency line on the sonogram.
- Back up to Dropbox… (share sheet: one .json + one 24-bit WAV per excerpt) and Restore… (pick the .json and .wavs).
- Export notes… (Markdown) and Share audio… per excerpt.

## v2 (12 Nov 2026)
- Play point: a tap on the waveform or the time line (ruler) sets it. If audio is playing, the playhead jumps there
  and keeps playing (a playing section continues inside the section if the tap is in it).
- Space = play / stop from the play point (no longer guesses the section); stopping returns to the play point.
  Key auto-repeat ignored.
- Fixed the sticky Space: tapped buttons kept focus and Safari "clicked" them again on Space key-up (double toggle).
  Buttons now drop focus after a tap and Space key-up is swallowed.

## v3 (12 Nov 2026)
- Renamed the stages: **Capture → Audition**, **Library → Excerpts** (tabs, side panel, buttons, dialog, messages).
  Internal ids (tabCap, vLib…) and saved data unchanged.
