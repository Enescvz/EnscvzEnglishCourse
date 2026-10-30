#!/usr/bin/env python3
"""Separate decodable audio from listening-quality-approved speech.

This does NOT judge how natural audio sounds automatically. Approval requires
explicit human review and provenance metadata, not an MP3 validity check.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/audio-provenance.json'
REPORT = ROOT / 'qa/audio-quality-report.json'


def audit(root=ROOT):
    manifest = json.loads((root / 'data/audio-provenance.json').read_text(encoding='utf-8'))
    episodes = json.loads((root / 'data/episodes.json').read_text(encoding='utf-8'))
    drills = json.loads((root / 'data/drills.json').read_text(encoding='utf-8'))
    recordings = {f'{category}:{r["id"]}': r for category, group in [('episode', episodes), ('drill', drills)] for r in group}
    records = manifest['recordings']
    errors = []
    if set(records) != set(recordings):
        errors.append({'type': 'manifest_mismatch', 'missing': sorted(set(recordings)-set(records)), 'extra': sorted(set(records)-set(recordings))})
    approved = 0
    quarantined = 0
    for key, item in recordings.items():
        meta = records.get(key)
        if meta is None:
            continue
        if meta.get('audio') != item['audio']:
            errors.append({'type':'audio_path_mismatch', 'id':key})
        path = root / item['audio']
        if not path.is_file():
            if meta.get('quality') == 'unapproved_robotic':
                quarantined += 1
            else:
                errors.append({'type':'missing_audio', 'id':key})
        if meta.get('quality') == 'approved':
            required = ('provider', 'voice', 'license_evidence', 'human_reviewer', 'review_date', 'transcript_verified', 'timing_verified')
            if any(not meta.get(field) for field in required):
                errors.append({'type':'unverified_approval', 'id':key})
            elif meta['provider'].lower() == 'espeak':
                errors.append({'type':'robotic_audio_approved', 'id':key})
            else:
                approved += 1
    report = {
        'recordings': len(recordings),
        'quarantined_synthetic_recordings': quarantined,
        'episodes': len(episodes),
        'drills': len(drills),
        'approved_for_natural_listening': approved,
        'not_approved_for_natural_listening': len(recordings)-approved,
        'status': 'READY' if not errors and approved == len(recordings) else 'BLOCKED',
        'notes': 'Synthetic MP3 bytes removed from the playable package. Metadata and historical progress remain; human playback requires separate verification.',
        'errors': errors,
    }
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--release',action='store_true',help='Exit nonzero until every listening recording is approved')
    args=parser.parse_args()
    result=audit()
    REPORT.parent.mkdir(exist_ok=True,parents=True)
    REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['errors'] or (args.release and result['status']!='READY'):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
