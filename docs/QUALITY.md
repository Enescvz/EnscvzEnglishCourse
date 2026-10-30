# Quality gates and known gaps

- Source of truth: bundled `/data/*.json` and `/assets/audio/*.mp3`.
- Every card has a stable ID, Turkish meaning, compact English definition and original sample sentence. Content is an editorial first pass and has not received independent teacher review.
- No B1/A2/A1 standalone vocabulary cards; general vocabulary is editorially tagged B2/C1. Specialist terms may have different actual CEFR levels, since professional terminology is not itself certified CEFR vocabulary.
- General/frequency priority is editorial, not a validated external corpus frequency ranking.
- CEFR overall competency cannot be inferred from 25 multiple-choice questions, listening dictation alone or time studied.
- `npm test` checks data uniqueness, score model, answer cardinality, media presence and timestamps, and route HTML assembly. It does NOT validate dictionary semantics or natural human voice.
- Automated speech recognition can route user audio through the browser vendor; opt-in warning is mandatory.
- `tests/e2e_playwright.py` is supplied but remains *UNVERIFIED*: managed Chromium browser policy blocked all URL navigations in the authoring container. Run on personal machine before treating the app as production QA-complete.
- Listening synthesis cannot faithfully substitute natural American conversation; outbound VOA link helps independently practice with humans.
- Known gaps: no embedded human voice podcast, no licensed audio/transcript syncing from humans, no Turkish translations for full Reading passages, no FSRS, no automated essay evaluation, no valid full CEFR placement exam, no multi-device cloud sync, no end-to-end Safari validation.


## Updated hard pre-release gates (27 October 2026)

Run `npm run release:check`: it must return zero before generating a publication archive. No GitHub upload of an incomplete version. The checked quantities include 3500 distinct general B2/C1 cards, at least 200 separate finance/accounting terms, 600 distinct phrasal verbs, sufficient original listening/reading lessons, properly credited licensed human audio, manual US-English editorial sign-off, and successful Chromium desktop + WebKit iPhone end-to-end testing. The report is saved as `development-status.json`.

**Important rights note:** VOA says *VOA-produced* learning texts and recordings are public domain when properly credited. Embedded wire service (e.g., AP/Reuters/AFP) photos/text/audio may have separate copyright and cannot be copied as VOA-original content. Any future imported human recordings must be traced to the original producer, rights and transcript; external links alone are not considered embedded human audio.

Oxford says its Oxford 5000 advanced addition consists of 2,000 B2/C1 entries, so the 3,500-card target cannot be claimed to be an exact copy of that list; independent, sense-aware curation and level verification are needed.

## Contextual examples and sentence listening (development update)

- All **565** current vocabulary entries (281 general and 284 specialist) and **139** phrasal cards have at least one original English example.
- Replaced **all 284** repetitive, generic Accounting/Finance sample sentences with distinct financial/accounting scenarios.
- **107** entries now have at least two distinct contextual sentences (76 vocabulary, 31 phrasals). One example is NOT counted twice or transformed into a cosmetic variant to inflate the count.
- Card UI plays full sentences with browser-provided **en-US TTS** if that voice is available; otherwise displays an explicit error. This is not a human recording.
- New sentence dictation hides the model sentence until submission, measures order-aware token accuracy, and uses the existing listening review mode. This is not a scientifically validated listening placement assessment.
- `npm run qa:examples` creates `qa/example_audit.json` for editorial triage. It checks structure and placeholders but **cannot certify** naturalness, semantics, dialect accuracy, or CEFR assignments.
- Release lock now also requires two distinct sentences for every vocabulary/phrasal card, on top of the original human-review and real-audio requirements.

All new content remains `authored_unreviewed`; do not publish until rights, US-English native usage and technical behavior are verified.


## Development update — extended content batches

- **281** general B2/C1-tagged vocabulary cards and **284** specialist accounting/finance terms; all remain unreviewed.
- **199** unique authored phrasal-verb headwords, including 60 new cards with definitions, Turkish glosses, syntax, and two independent examples. B2/C1 tags are editorial candidates, **not independently certified**.
- **18** original podcast dialogue lessons and **24** listening drills. **42** bundled synthetic en-US MP3 files with measured duration/timestamps; zero bundled human voices.
- **150** additional individual original context sentences were written for older cards. Overall **317** cards have two distinct examples and **447** still need a second one.
- `npm run qa:sandbox` runs Chromium with a virtual origin and **mock localStorage** in this restricted environment. This is a UI-flow smoke test in desktop/mobile viewports. It does **not** prove real server navigation, Safari WebKit, durable localStorage, or native audio playback on an iPhone. Its evidence is `qa/browser_harness_report.json` (not accepted by the release gate).
- `npm run test:all` runs structural/algorithm tests; `python tools/audio_qa.py` verifies MP3 playability and approximate timing, not human listening transcript correctness.
- The release gate remains locked: no ZIP, GitHub deployment, or signoff until all requirements and editorial review are complete.
