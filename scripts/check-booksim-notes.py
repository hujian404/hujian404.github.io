"""Validate the published reading structure, local links, figures and source excerpts.

Usage: python scripts/check-booksim-notes.py [--source-root PATH]
The optional BookSim2 checkout must be at the documented fixed revision.
"""
from pathlib import Path
import argparse
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / 'notes/booksim-notes'
SHA = '28f43299f1706a3160ffac721ca461d74eb6e618'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path)
    args = parser.parse_args()
    structure = json.loads((NOTES / 'book-structure.json').read_text(encoding='utf-8'))
    assert [c['number'] for c in structure['chapters']] == list(range(1, 26))
    sections = excerpts = links = figures = 0
    for c in structure['chapters']:
        text = (NOTES / c['file']).read_text(encoding='utf-8')
        assert text.splitlines()[0] == f"# Chapter {c['number']}｜{c['title']}"
        actual = re.findall(r'^(#{2,3}) (\d+\.\d+(?:\.\d+)?) (.+)$', text, re.M)
        expected = [('#' * (s['id'].count('.') + 1), s['id'], s['title']) for s in c['sections']]
        assert actual == expected, c['file']
        for s in c['sections']:
            assert f"*原书印刷页 {s['page']}。*" in text, (c['file'], s)
        sections += len(expected)
    for path in sorted(NOTES.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        assert text.count('```') % 2 == 0, path
        assert not re.search(r':contentReference\[|Chapter X|2026-10-22 更新：', text), path
        # The public notes must not contain private server addressing or login paths.
        assert not re.search(r'192\.168\.\d+\.\d+|/data/home/|/home/[a-z][a-z0-9_.-]*/|(?i:password)\s*[:=]', text), path
        for url in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', text):
            if url.startswith(('https://', 'http://', '#')):
                continue
            target = ROOT / url.lstrip('/') if url.startswith('/') else path.parent / url
            assert target.exists(), (path.name, url)
            links += 1
        pattern = r'查看 ([^ ]+) 第 .*?\]\([^)]*/' + SHA + r'/[^)]*#L(\d+)-L(\d+)\)。\n\n```cpp\n(.*?)\n```'
        for source, start, end, snippet in re.findall(pattern, text, re.S):
            excerpts += 1
            if args.source_root:
                original = (args.source_root / source).read_text(encoding='utf-8').splitlines()
                assert snippet == '\n'.join(line.rstrip() for line in original[int(start)-1:int(end)]), (path.name, source)
    assert excerpts == 25, excerpts
    for path in NOTES.rglob('*.drawio'):
        ET.parse(path)
        ET.parse(path.with_suffix('.svg'))
        figures += 1
    assert figures == 9, figures
    page = (ROOT / 'booksim-series.html').read_text(encoding='utf-8')
    assert page.count('<div class="ch-status done">Published</div>') == 26
    assert '>Draft<' not in page
    print(json.dumps(dict(chapters=25, book_sections=sections, source_excerpts=excerpts,
                          checked_source=bool(args.source_root), local_links=links,
                          drawio_svg_pairs=figures), ensure_ascii=False))


if __name__ == '__main__':
    main()
