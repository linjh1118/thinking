"""Verify release files using only the Python standard library."""
from pathlib import Path
import hashlib


def main():
    root=Path(__file__).resolve().parent
    rows=(root/'SHA256SUMS').read_text().splitlines()
    seen=set()
    for line in rows:
        digest,name=line.split('  ',1)
        if not name or Path(name).name!=name or name in seen:
            raise ValueError('Invalid checksum manifest')
        seen.add(name)
        p=root/name
        if p.is_symlink() or not p.is_file():
            raise ValueError('Missing or linked release file: '+name)
        h=hashlib.sha256()
        with p.open('rb') as f:
            for b in iter(lambda:f.read(4<<20),b''):h.update(b)
        if h.hexdigest()!=digest:
            raise ValueError('Checksum mismatch: '+name)
    extras={p.name for p in root.iterdir() if p.is_file()}-seen-{'SHA256SUMS'}
    if extras:raise ValueError('Unlisted files: '+', '.join(sorted(extras)))
    print(f'OK: {len(seen)} release files verified')


if __name__=='__main__': main()
