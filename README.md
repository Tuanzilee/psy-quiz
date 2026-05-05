# Psych Quiz

收錄輔仁、臺大、成大三校共 **632 題** 普通心理學轉學考試題的單頁刷題網站。

## 題庫概況

| 學校 | 年度 | 題數 |
|---|---|---|
| 輔仁（FJU） | 107、108、109、111、112、113、114A、114B | 119 |
| 臺大（NTU） | 108、109、111、112、113、114 | 225 |
| 成大（NCKU） | 107、108、109、111、112、113、114 | 288 |
| **總計** | | **632** |

題型涵蓋選擇題、是非題、配合題、申論題、名詞解釋。

## 使用方式

直接打開 `index.html` 即可。手機桌機都支援，不需要 server。

### 部署到 GitHub Pages

1. Push 此 repo 到 GitHub
2. 進 Settings → Pages → Source 選 `main` branch、root（`/`）
3. 等幾分鐘後即有公開網址 `https://<username>.github.io/<repo-name>/`

### 主要功能

- 三 tab 導航：主頁／瀏覽／章節
- 刷題模式：上一題／下一題、三色記號（懂了／不確定／不懂）
- 進度本機保存（localStorage，不會傳出去）
- 解析、章節、提示三 tab
- 篩選：學校／年度／題型／狀態（AND 邏輯）
- 申論題、名詞解釋的關鍵字批改
- 申論題答題骨架顯示
- 配合題支援多選項（A-Z）

## 專案結構

```
psych-quiz/
├── index.html              # 最終成品（給 GH Pages 用，build 出來的）
├── psych_template.html     # 不含資料的 UI template
├── build_html.py           # build script
├── data/
│   ├── concepts.json
│   └── questions/
│       ├── FJU_107.json
│       ├── ...
│       └── NCKU_114.json
└── README.md
```

`index.html` 是 build 產物但 commit 進 repo，因為 GitHub Pages 直接服務 repo 內檔案，不會幫你跑 build script。

## 改題庫流程

### 修正某題答案 / 章節 / 解析

1. 編輯 `data/questions/{學校}_{年度}.json`
2. 跑 `python3 build_html.py`
3. `git add data/questions/X.json index.html`
4. `git commit -m "fix XXX_YY Q23 answer"`
5. `git push`

### 新增學校年度試卷

1. 在 `data/questions/` 新增 JSON 檔（schema 見下方）
2. 把檔名加進 `build_html.py` 的 `FILE_ORDER`
3. 跑 build → commit → push

## Schema

```json
{
  "id": "NCKU_114_01",
  "source": "NCKU",
  "year": 114,
  "year_ad": 2025,
  "type": "選擇題",
  "language": "en",
  "difficulty": "medium",
  "section": {"type": "選擇題", "number": 1, "title": "第2章 心理學方法"},
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "answer": "A",
  "answer_confidence": "medium",
  "answer_source": "ai_generated",
  "reference_answer": "...",
  "ai_hint": "...",
  "common_mistakes": "...",
  "concepts": ["..."],
  "scholars": ["..."],
  "school_of_thought": "...",
  "key_concepts": "...",
  "keywords_required": [],
  "essay_outline": null,
  "needs_image": false,
  "images": [],
  "answer_note": "...",
  "topic": "第2章 心理學方法"
}
```

| 欄位 | 取值 |
|---|---|
| `type` | 選擇題／是非題／配合題／申論題／名詞解釋 |
| `language` | zh／en |
| `answer_confidence` | high（原試卷有答案／可靠來源）／ medium（AI 推導，未勘誤） |
| `answer_source` | user_provided／ai_generated |
| `topic` | 對應 16 章節之一（見下表） |

## 16 章對照

| 章 | 名稱 |
|---|---|
| 第 1 章 | 緒論 |
| 第 2 章 | 心理學方法 |
| 第 3 章 | 行為的生物基礎 |
| 第 4 章 | 感覺與知覺 |
| 第 5 章 | 注意與意識 |
| 第 6 章 | 學習 |
| 第 7 章 | 記憶 |
| 第 8 章 | 語言與心智表徵 |
| 第 9 章 | 思考與創造力 |
| 第 10 章 | 智力 |
| 第 11 章 | 動機與情緒 |
| 第 12 章 | 性格 |
| 第 13 章 | 社會心理學 |
| 第 14 章 | 發展心理學 |
| 第 15 章 | 壓力、適應與健康 |
| 第 16 章 | 心智異常 |

## 待勘誤

許多題目的答案、章節、解析由 AI 推導，標 `medium` 信心度。優先勘誤順序：

- NCKU 107（50 題）
- NCKU 108-114（278 題）
- NCKU 114（特別注意：原試卷英文／出題詭異，Q15、Q16、Q25、Q29、Q38 邊界模糊）
- NTU 114 是非題、NTU 113 Q18／Q24

## 免責聲明

- 本工具自用、學習目的
- 題目原始版權屬於各校
- AI 推導的答案可能有誤，正式應試以官方答案為準
