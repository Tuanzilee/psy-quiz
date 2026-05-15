# CLAUDE.md

## Repo 用途

收錄輔仁、臺大、成大三校共 632 題普通心理學轉學考試題的單頁刷題網站(純前端 + localStorage)。

線上部署:**https://tuanzilee.github.io/psy-quiz/**(GitHub Pages)

## 檔案結構

```
psy/
├── index.html              ← Build 產物(約 800 KB,含全部題目 JSON)。GH Pages 服務這支
├── psych_template.html     ← UI template(155 KB,不含資料)。改 UI / JS 邏輯改這裡
├── build_html.py           ← 把 template + 根目錄的 JSON 組成 index.html
├── .github/workflows/
│   └── build.yml           ← GitHub Actions:push 後自動 build & commit index.html
├── FJU_107.json … FJU_114B.json    ← 輔仁題庫(8 份)
├── NTU_108.json … NTU_114.json     ← 臺大題庫(6 份)
├── NCKU_107.json … NCKU_114.json   ← 成大題庫(7 份)
├── concepts.json           ← 章節 / 概念清單
├── FJU_questions.json      ← 舊單檔合併版(看起來已淘汰,別改)
├── fujen_psych_prep.html   ← 舊版頁面(已淘汰)
├── README.md
└── 其他資料/                ← 原始 PDF / 講義,不影響 build
```

**21 份題庫 JSON 與 `concepts.json` 都在 repo 根目錄**(不在 `data/` 子目錄)。

### 不能直接改的檔

- **`index.html`** — build 產物。改 JS / UI 永遠改 `psych_template.html`,改題目改根目錄的 `*.json`,然後重 build。
- **`FJU_questions.json`、`fujen_psych_prep.html`** — 看起來是舊版遺留,改了也不會被 build 採用。

## 工作流(2026-05-15 起)

- **2026-05-15 之前**:都用 GitHub Web UI 拖檔上傳源檔,Actions 接著自動 build。從沒在本機跑過 build,也沒從 CLI push 過。
- **2026-05-15 起**:改用本機 git workflow——本機 build + commit index.html 一起 push(下述標準流程)。
- **源 vs 產物**:
  - `psych_template.html` 是真正的源,改 UI / JS 改這裡
  - 根目錄的 `*.json` 是真正的源,改題目改這裡
  - `index.html` 是 build 產物,**永遠別手改**(手改會被下次 Actions build 蓋掉)

### 標準 commit 流程(本機 build + commit index.html 一起 push)

1. 改 `psych_template.html` 或根目錄 JSON
2. `python3 build_html.py`(本機 build,順手驗證沒事)
3. `git add psych_template.html / JSON / index.html`(三個一起 add)
4. `git commit -m "..."`
5. `git push origin main`
6. Actions 會在 ubuntu 上重 build,因為 byte-identical 不會多 commit → pull 也不會卡

**為什麼選這條**:本機 build 跟 Actions build 已驗證 byte-identical(commit `22fc513` → `1b7782a` 那次,diff 0 bytes)。若未來 Python 版本或 `build_html.py` 邏輯改變導致 drift,Actions 那邊還是會 auto-commit 補救 → 正常情況最簡潔,異常情況自動兜底。

**反例**(別這樣做):只 commit template、不 commit index.html → push 後 Actions 會額外產一個 auto-build commit,本機 pull 前還得 stash 自己的 build artifact,徒增麻煩。

## Build 流程

```bash
python3 build_html.py
```

會讀 `psych_template.html` + `build_html.py` 裡 `FILE_ORDER` 列出的 JSON(repo 根目錄),組出 `index.html`。

新增學校試卷:把檔名加進 `build_html.py` 的 `FILE_ORDER` 再 build。

## Commit / Push 流程

改題庫:
```bash
# 1. 改根目錄的 X.json(如 NCKU_114.json)
# 2. 跑 build
python3 build_html.py
# 3. commit
git add NCKU_114.json index.html
git commit -m "修正 NCKU_114 Q15 答案"
git push
```

改 UI / JS:
```bash
# 1. 改 psych_template.html
# 2. build
python3 build_html.py
# 3. commit
git add psych_template.html index.html
git commit -m "模考新增分層抽題邏輯"
git push
```

**Commit message 風格:中文,動詞開頭,簡潔。**
範例:「修正 NTU_113 Q24 答案」、「新增章節篩選」、「修 startExam 重複出題」。

GitHub Actions(`build.yml`)會在 push 後自動跑 build 並 commit `index.html`,所以本地 build 算雙保險。

## 與 Claude 的協作風格

- **直接動手,做完再報。** 不需要逐步請示;只在「會動到大量檔案 / 不可逆操作 / 需求模糊」時才停下確認。
- **改檔優先用 Edit(str_replace),少用 Write 整檔覆蓋。** 整檔覆蓋風險高、diff 難看。
- **不要重複問同樣的事。** 已經問過或已寫進這份 CLAUDE.md 的事,直接照辦。
- 改 JS 邏輯記得**改 `psych_template.html`,不是 `index.html`**。
- 改完 template 後要記得跑 build,否則本地 `index.html` 不會更新。

## 已知狀態(2026-05-15)

### 題庫分布(共 632 題)

| 學校 | 年度 | 題數 |
|---|---|---|
| FJU | 107、108、109、111、112、113、114A、114B | 119 |
| NTU | 108、109、111、112、113、114 | 225 |
| NCKU | 107、108、109、111、112、113、114 | 288 |

題型:選擇、是非、配合、申論、名詞解釋。

### 待勘誤

- NCKU 107(50 題)、NCKU 108-114(278 題)— 多為 AI 推導答案,信心度 medium
- NCKU 114 Q15、Q16、Q25、Q29、Q38(原試卷英文,出題詭異)
- NTU 114 是非題、NTU 113 Q18 / Q24

### 最近處理過 / 待處理

- **模考重複出題**(已修,2026-05-15,commit `22fc513` + Actions `1b7782a`):`psych_template.html` 新增 `stratifiedExamPick()`,在 `startExam()` 非 preset 分支調用。分層邏輯:未做過 > 做錯/跳過 > 已答對,每層內洗牌;沒答 / 跳過視為 wrong(要重做);客觀題比對 `q.answer`、申論看 `selfScores.score >= max * 0.6`。`examState` + `redoWrong()` 同時新增 `wrongReasons: {}` 預留欄位(未來「錯因標記」feature 用)。

### 已知 bug(2026-05-15 診斷,暫未修)

兩個都跟 `reviewExam(id)` 把 `examState` 設為 history entry 的 **reference 而非 copy** 有關。

- **Bug A:review 舊模考時按【完成(存進歷史)】會在 `EXAMS_KEY` 多塞一筆相同 id**
  - 路徑:`reviewExam` → `examState = hist[i]` → 使用者按【完成】→ `finishExam()` 的 `hist.unshift(examState)` 把同一個物件再塞一次回 `EXAMS_KEY`
  - 影響:歷史會有兩張外觀一樣的 card;`deleteExamFromHistory(id)` 用 `filter(e => e.id !== id)` 會**同時刪掉兩筆**(因為 id 相同)

- **Bug B:review 模式做任何編輯(改自評分數、標錯因)只寫到 `CURRENT_EXAM_KEY`,沒人讀那裡**
  - 路徑:`updateSelfScore` / `toggleWrongReason` → `saveCurrentExam()` → 寫 `CURRENT_EXAM_KEY`
  - 但 `reviewExam` 下次進來是讀 `EXAMS_KEY`,不讀 `CURRENT_EXAM_KEY`(`submittedAt` 有值會跳過 resume 路徑)
  - 影響:review 模式下的編輯永久遺失,回首頁再點開該模考會回到原狀

- **修法方向(暫定 Option 2)**:reviewExam 進去時設 flag(例:`_isReviewing = true`),`updateSelfScore` / `toggleWrongReason` 偵測到 review 模式 → 改寫 `EXAMS_KEY` 對應 entry,不寫 `CURRENT_EXAM_KEY`;【完成】按鈕在 review 模式隱藏(或改文案「儲存更新」)

- **緊急度:低**。線上版 `EXAMS_KEY` 目前空(新工作流剛建立、還沒累積使用者實戰場次),bug 在實際情境下尚未發作。等使用者開始累積模考紀錄、需要回頭補錯因時再修。
