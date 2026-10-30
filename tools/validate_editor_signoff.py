#!/usr/bin/env python3
"""Fail-closed reviewer gate for independently completed 975-row audit CSV.
Blank machine-generated rows are never approved merely because the lint passed.
"""
import argparse,csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('csv_path',nargs='?',type=Path,default=ROOT/'qa/20261030-editor-review/review-queue.csv');args=parser.parse_args()
rows=list(csv.DictReader(args.csv_path.open(encoding='utf-8-sig',newline='')))
if len(rows)!=975:sys.exit('BLOCK: expected 975 review rows')
seen=set();missing=[]
for row in rows:
 k=(row['kind'],row['id'])
 if k in seen:sys.exit(f'BLOCK: duplicate review id {k}')
 seen.add(k)
 if not all(row.get(field)=='yes' for field in ('humanTranslationApproved','humanUsageApproved','humanLevelApproved')):
  missing.append(row['id']);continue
 if not row.get('reviewer','').strip() or not row.get('reviewDate','').strip():missing.append(row['id'])
if missing:sys.exit(f'BLOCK: independent human review incomplete for {len(missing)}/975 items')
print('Human review forms complete. Approval identity and qualifications must still be independently verified.')
