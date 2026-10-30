# Listening — new voice and quality policy (28 October 2026)

User auditioned the official public HeyGen preview voices **Lea** (female) and **Daran** (male) and found both suitable as *voice references*. Their previews are external demonstrations, not American English Lab recordings, and are **not bundled**. Do not assume that demonstration playback grants a commercial or redistribution license for generated audio.

## Verified current state

- 18 mini-dialogue episodes and 24 dictation drills; 42 bundled MP3s generated with eSpeak, **not suitable as natural American English listening exemplars**.
- 0 tracks have completed a **human** naturalness/accent/transcript review.
- The voice generation attempt using Lea (HeyGen public voice, Orca) failed **without creating audio**: the free allowance displayed 8 seconds remaining, while the requested script required 14 seconds. Do not retry a generation automatically; ask user before any new generation, and do not spend money without approval.
- No robot-generated MP3s have been overwritten. All previous curricula, progress storage, scripts and timings remain intact.

## Replacement protocol

1. Verify that the proposed engine and voice have a **clear license for bundling and distributing MP3s inside a free app**. External demo URLs by themselves do not grant rights.
2. Record one original 20–40s two-person everyday dialogue with distinct US voices. Audition the result for clarity, prosody, contractions, linking, speed, and consistency; compare with real US native speaker examples.
3. Add a new asset only after confirming provenance, rights, audio intelligibility, transcript accuracy, and start/end timings for every turn. Replace old playback paths **only after** these validations. The UI's AB repeat and dictation depend on correct timing data.
4. Never label old eSpeak material as natural, human, or editorially approved. Gate production with `python tools/audio_quality_gate.py --release`. A default audit command records the honest gap without failing normal development tests.
5. Production listening targets: original dialogues in daily situations and licensed real-human recordings, increasing from 17 minutes to meaningful short and longer content. Distinguish generated from human recordings in metadata.

Current metadata: `data/audio-provenance.json`. Check with `python tools/audio_quality_gate.py` and inspect `qa/audio-quality-report.json`.
