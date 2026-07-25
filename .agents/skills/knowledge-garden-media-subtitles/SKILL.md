---
name: knowledge-garden-media-subtitles
description: Create polished Simplified Chinese WebVTT subtitles from English or auto-generated VTT files and connect them to Obsidian Media Extended media notes in this knowledge-garden project. Use this skill whenever the user mentions 中文字幕、翻译字幕、VTT、WebVTT、视频转录、Media Extended/media-extend/media-extand、captions/subtitles frontmatter, or asks whether translated subtitles will display correctly in this project. In this repository, prefer this project skill over similarly named global subtitle skills.
compatibility: Python 3; project-local Obsidian vault under content/; Media Extended is optional for file generation and required for playback integration.
---

# Media Extended Chinese subtitles

Use this workflow for subtitle translation and Media Extended integration in this repository. Preserve the source subtitle and make the translated track easy to select, validate, and maintain.

## Resolve project paths

This project-local skill lives under the Git root at `.agents/skills/knowledge-garden-media-subtitles/`. Pi discovers project `.agents/skills/` from the current directory and its ancestors. Resolve paths from the skill location rather than assuming the shell's current directory:

- Git root: the ancestor containing `.git/` and `.agents/`
- Vault root: `<git-root>/content/`, which contains `.obsidian/`

Important vault-relative locations:

- Media notes: `Knowledge/Sources/Media/`
- Subtitle tracks: `Knowledge/Assets/Subtitles/`
- Media covers and screenshots: `Knowledge/Assets/Media/Images/`
- Generic attachments: `Knowledge/Assets/Attachments/`
- Media Extended installation: `.obsidian/plugins/media-extended/`

Search rather than assuming a note or attachment location. Run these from the vault root, or use its absolute path:

```bash
rg -n --fixed-strings '<subtitle-basename-or-media-uid>' .
find . -type f -name '*.vtt'
```

## End-to-end workflow

### 1. Locate the source track and media note

Read the media note frontmatter and identify:

- Media URL or local media file
- `mx-uid`
- Existing `captions` and `subtitles`
- Source VTT path and language

Keep the original track. For an English source named `name.en.vtt`, normally create `name.zh-Hans.vtt` beside it unless the note or plugin configuration clearly uses a dedicated subtitle folder.

### 2. Prepare readable translation units

Auto-generated YouTube VTT often splits one sentence across many tiny cues and includes inline word timestamps. Do not translate those fragments independently: context-free translation produces awkward Chinese.

Use the bundled helper to strip inline word timestamps and merge adjacent fragments into semantic groups:

```bash
python3 <skill-dir>/scripts/vtt_tool.py prepare \
  '<source.en.vtt>' \
  --groups /tmp/subtitle-groups.json \
  --source-tsv /tmp/subtitle-source.tsv
```

Review `/tmp/subtitle-source.tsv` and correct obvious ASR errors before translating. Use the full talk context, speaker identity, slide terminology, and nearby cues to infer intended wording.

### 3. Translate into polished Simplified Chinese

Create a UTF-8 TSV with one translation per line:

```text
001\t[音乐]
002\t大家好，欢迎来到……
003\t……
```

Translation principles:

- Translate meaning and discourse flow, not isolated English fragments.
- Keep technical names recognizable: `Agent`, `PR`, `diff`, `commit message`, `Vibe coding`, `Notion`, `Claude`, `Cursor`, language names, and personal names may remain in English where clearer.
- Use stable project terminology: `cognitive debt` → `认知债务`; `microworld` → `微型世界`; `shared spaces` → `共享空间`; `literate code diff` → `叙事式代码 diff`.
- Translate sound descriptions such as `[music]`, `[applause]`, and `[laughter]`.
- Rephrase obvious speech-recognition mistakes rather than reproducing nonsense.
- Keep each cue concise enough to read. Split ideas across adjacent existing time ranges when useful.
- Do not invent word-level timing for translated words. Accurate word highlighting requires alignment or forced-alignment tooling.

### 4. Build and validate WebVTT

```bash
python3 <skill-dir>/scripts/vtt_tool.py build \
  --groups /tmp/subtitle-groups.json \
  --translations /tmp/subtitle-zh.tsv \
  --output '<target.zh-Hans.vtt>'

python3 <skill-dir>/scripts/vtt_tool.py validate '<target.zh-Hans.vtt>'
```

A valid result must:

- Start with `WEBVTT`
- Be UTF-8
- Have valid start/end timestamps and non-empty cue text
- Preserve chronological order
- Cover the complete spoken content
- Contain no replacement characters (`�`) or untranslated accidental fragments

The helper warns about overlapping cues but does not reject them because WebVTT permits overlap.

### 5. Attach the translation to the media note

Media Extended distinguishes original captions from translated subtitles:

- `captions`: same-language transcription/closed captions, often auto-generated
- `subtitles`: translated subtitle tracks

Add Chinese under `subtitles`; do not replace the English `captions` entry.

Use the helper for a minimal frontmatter edit:

```bash
python3 <skill-dir>/scripts/vtt_tool.py attach \
  '<media-note.md>' \
  '<target.zh-Hans.vtt>' \
  --property subtitles \
  --lang zh-Hans \
  --label '中文（简体）'
```

Expected form:

```yaml
captions:
  - "[[source.en.vtt#lang=en&label=...]]"
subtitles:
  - "[[source.zh-Hans.vtt#lang=zh-Hans&label=%E4%B8%AD%E6%96%87%EF%BC%88%E7%AE%80%E4%BD%93%EF%BC%89]]"
```

The helper uses the basename in the wikilink to follow this vault's convention. Before relying on it, ensure duplicate basenames do not exist in the vault.

### 6. Verify Obsidian resolution and Media Extended behavior

Read [Media Extended reference](references/media-extended.md) when attaching tracks, changing plugin settings, or explaining playback behavior.

If Obsidian is open, verify that the wikilink resolves. Account for this repository's nested vault: the CLI may currently target the Git root rather than `content/`.

Example when the active vault is the Git root:

```bash
obsidian eval code="(() => { const note='content/<note-path>'; const dest=app.metadataCache.getFirstLinkpathDest('<subtitle-basename>', note); return dest?.path })()"
```

In Media Extended, the user should be able to:

1. Open the media note/player.
2. Open the subtitle menu.
3. Select `中文（简体）`.
4. Use `打开转录文稿` to view transcript or subtitle mode.

Cue-level display and seeking work without inline word timestamps. The `高亮当前词` feature will not provide precise Chinese word highlighting unless a separately aligned track is created.

### 7. Change plugin-wide defaults only when requested

Do not silently change global playback preferences. If the user wants Chinese selected by default, inspect `<vault-root>/.obsidian/plugins/media-extended/data.json` and set through the UI when possible:

- `默认启用字幕` → enabled
- `默认语言` → `zh-Hans`

The settings keys are:

```json
{
  "playback.track.default-enabled": true,
  "playback.track.default-languages": ["zh-Hans"]
}
```

## Quality checks before finishing

- Compare several opening, middle, and closing cues against the English source.
- Check names and domain terminology manually.
- Check long Chinese cues for readability.
- Confirm the media note retains all previous tracks.
- Confirm the subtitle link resolves to the intended file.
- Report whether validation was structural only or included a live player test.

## Final response

Report concisely:

- Created subtitle path
- Updated media note path
- Cue count and validation result
- How to select/open the track in Media Extended
- Whether word-level highlighting is available
- Any limitation, such as the active Obsidian instance pointing at a different vault
