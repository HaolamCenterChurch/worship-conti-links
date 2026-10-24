# worship-conti-links — 콘티 레퍼런스 링크 스킬

하올람센터처치 찬양팀용. 콘티(곡 제목 목록)를 주면 **Haolam Worship Moments** 유튜브 재생목록에서 곡을 찾아
제목을 영상 제목(곡 부분)으로 바로잡고 바로 아래줄에 영상 링크를 붙이는 Claude Code 스킬이다.

- 재생목록 하나만 쓴다: https://www.youtube.com/playlist?list=PLlWmEcXlwkniayozHuxP1DpQrr1RKE3_B
- 확실히 찾은 곡만 이름을 바꾼다. 짐작뿐이면 `[혹시 이 곡?]`, 여러 인도자 영상이 있으면 `[후보 여러 개]`, 없으면 `[재생목록에 없음]`.
- 제목 뒤에 인도자 이름을 붙이면 그 인도자 영상을 고른다. 메들리 영상(`A + B`)은 맨 앞 곡만 찾는다.
- 부르는 이름이 영상 제목과 다르면 `aliases.json` 에 `"부르는 이름": "영상 제목 일부"` 로 넣는다.

절차는 [`SKILL.md`](SKILL.md).

## 준비물

- Python 3 (표준 라이브러리만 씀)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 실행할 때마다 재생목록을 새로 읽는다

## 쓰는 법

Claude Code 에서 "콘티 링크 붙여줘" 하고 곡 목록을 주면 된다. 수동으로는:

```bash
printf '1. 내 삶은 주의 것\n2. Firm foundation\n' | python3 conti_links.py
```

```
1. 내 삶은 주의 것
  [혹시 이 곡?] 전쟁은 주의 것 (Battle Belongs)(한명진) https://www.youtube.com/watch?v=j4_VrMe7pxs
2. Firm Foundation
https://www.youtube.com/watch?v=yfzyWcB_O1g
```
