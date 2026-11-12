# EA Excerpts — working notes for Claude

The user (Lawrence) is an electroacoustic composer. EA Excerpts is their iPad/Mac app for studying excerpts of
electroacoustic compositions kept on Dropbox. It follows VocalPrep (L-SIAL/vocalprep): same layout, colours and workflow.

## The app
- One file: `app/ea_excerpts_vNN.html` (HTML + CSS + JS, no build step, no libraries).
- `build.py` copies it to `site/index.html` and adds the offline service worker, manifest and drawn icons (needs Pillow).
- `.github/workflows/deploy.yml` publishes to https://l-sial.github.io/ea-excerpts/ on every push to `main` (1–2 min).
- Version: `<span class="ver …">vNN</span>` next to the name. `HANDOFF.md` = change history (newest at the end).

## How to make a change
1. `git mv` the html to the next number so there is only ever ONE html in `app/`.
2. Change the version span.
3. Make the change; comments starting `// vNN:` that say why.
4. Extract the `<script>` and run `node --check`; build (`python3 build.py`) and load `site/` in a headless browser.
   Test hooks: `window.__ea`.
5. Add a `## vNN (date)` section at the end of `HANDOFF.md`.
6. Commit; push to `main` if allowed, otherwise push a branch, open a pull request and tell the user to tap **Merge**.

## The user's rules
- Interface words: **Audition** (stage 1) and **Excerpts** (stage 2). Code ids still say cap/lib.
- Short replies: the result and how to use it, numbered steps.
- Colours: parchment (#F2EDE2 / #FBF8F2) with black and muted grey-blacks; sonogram ramps white → sienna → near-black. No dark mode.
- Keyboard: full 88 keys A0–C8, A4 = 440; note names and Hz UNDER the keys, not on them.
- Excerpts are stored as 24-bit WAV. Files with more than 2 channels are folded to stereo.
- Backups go to Dropbox through the share sheet (Save to Files › Dropbox); the app can't write there by itself.
- Never delete the user's files. Don't change saved data in a way older versions can't read: add fields, don't rename.

## Data (IndexedDB `ea-excerpts`)
- `meta` {id, name, composer, piece, group, notes, src (file name), start, end, sr, ch, created}
- `audio` (24-bit WAV blob, by excerpt id) — missing audio is restored by opening the source file (matched by name).
- `files` {name, markers[{t,note}], composer, piece} by sanitised file name.
