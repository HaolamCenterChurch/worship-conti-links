#!/usr/bin/env python3
"""콘티 곡 제목 → Haolam Worship Moments 재생목록 링크를 제목 아래줄에 붙인다.

사용: python3 conti_links.py < 콘티.txt   (또는 인자로 파일 경로)
"""
import difflib, json, re, subprocess, sys
from pathlib import Path

PLAYLIST = "https://www.youtube.com/playlist?list=PLlWmEcXlwkniayozHuxP1DpQrr1RKE3_B"
ALIASES = json.loads((Path(__file__).parent / "aliases.json").read_text())


def norm(s):
    return re.sub(r"[^0-9a-z가-힣]", "", s.lower())


def playlist():
    out = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(title)s\thttps://www.youtube.com/watch?v=%(id)s", PLAYLIST],
        capture_output=True, text=True, check=True).stdout
    rows = []
    for line in out.splitlines():
        title, url = line.split("\t")
        song = title.split(" | ")[0].rsplit(" - ", 1)[0].strip()  # "곡 - 인도자 | ..." → 곡
        leader = title.split(" | ")[0].rsplit(" - ", 1)[-1].strip()
        rows.append((song, leader, url))
    return rows


def split_leader(query, rows):
    """"기적의 집 이사라" → ("기적의 집", "이사라"). 인도자 이름이 없으면 (query, None)."""
    for leader in sorted({r[1] for r in rows}, key=len, reverse=True):
        if norm(leader) and norm(leader) in norm(query):
            rest = re.sub(r"\s*[-(]?\s*" + re.escape(leader) + r"\s*\)?\s*", " ", query, flags=re.I).strip()
            if rest:
                return rest, leader
    return query, None


def find(query, rows):
    query, leader = split_leader(query, rows)
    q = norm(ALIASES.get(query.strip(), query))
    hits = [r for r in rows if q and q in norm(main_song(r[0]))]
    if leader:
        mine = [r for r in hits if r[1] == leader]
        if mine or hits:  # 그 인도자 영상이 없으면 다른 인도자 영상을 후보로만 보여 준다
            return (mine, False) if mine else (hits, True)
    elif hits:
        return hits, False
    # 대충 쓴 제목: 가장 비슷한 곡 하나를 추정으로 돌려준다
    def score(r):  # 내가 쓴 글자 중 영상 제목과 한 덩어리로 이어서 겹치는 비율
        t = norm(main_song(r[0]))
        sm = difflib.SequenceMatcher(None, q, t, autojunk=False)
        return sm.find_longest_match(0, len(q), 0, len(t)).size / len(q)
    best = max(rows, key=score) if q else None
    return ([best] if best and score(best) >= 0.6 else []), True


def main_song(song):
    """메들리 영상("A + B")은 맨 앞 곡만 메인이다. 뒤에 붙은 곡은 그 영상으로 찾지 않는다."""
    first = re.split(r"\s+\(?[+&]\s+", song)[0]  # "A + B", "A & B", "A (& B)"
    return first[:-1] if first.count(")") > first.count("(") else first


def main():
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    rows = playlist()
    for line in text.splitlines():
        m = re.match(r"(\s*\d+[.)]\s*)(.+)", line)
        if not m:
            print(line)
            continue
        hits, guessed = find(m.group(2), rows)
        if len(hits) == 1 and not guessed:  # 제목을 영상 제목(곡 부분)으로 바꿔 적는다
            print(m.group(1) + main_song(hits[0][0]))
            print(hits[0][2])
            continue
        print(line)  # 재생목록에서 확실히 못 찾은 곡은 이름을 바꾸지 않는다
        if guessed and hits:
            print("  [혹시 이 곡?] " + " / ".join(f"{main_song(s)}({l}) {u}" for s, l, u in hits))
        elif hits:
            print("  [후보 여러 개] " + " / ".join(f"{main_song(s)}({l}) {u}" for s, l, u in hits))
        else:
            print("  [재생목록에 없음]")


if __name__ == "__main__":
    main()
