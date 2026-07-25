# Media Extended subtitle behavior in this project

This reference summarizes the installed plugin implementation inspected in `content/.obsidian/plugins/media-extended/`.

## Installed project configuration

- Plugin ID: `media-extended`
- Inspected version: `4.2.7`
- Manifest: `content/.obsidian/plugins/media-extended/manifest.json`
- Settings: `content/.obsidian/plugins/media-extended/data.json`
- Implementation: `content/.obsidian/plugins/media-extended/main.js`
- Enabled-list entry: `content/.obsidian/community-plugins.json`

Always re-read the manifest and settings if the plugin may have been updated.

## Frontmatter fields

The plugin reads both fields:

```yaml
captions:
  - "[[english.vtt#lang=en&label=English]]"
subtitles:
  - "[[chinese.zh-Hans.vtt#lang=zh-Hans&label=中文（简体）]]"
```

Use `captions` for transcription/closed captions and `subtitles` for translated tracks.

Both fields accept internal wikilinks and URL/file links. Track fragment parameters parsed by version 4.2.7 include:

- `id`
- `format`
- `kind`
- `lang` or `language`
- `label`
- `default`

The plugin's own encoder URL-encodes fragment values, so encoded Chinese labels are normal.

## Filename language inference

The parser recognizes a final BCP-47-like component before the extension:

- `talk.en.vtt` → language `en`, logical basename `talk`
- `talk.zh-Hans.vtt` → language `zh-Hans`, logical basename `talk`

Explicit `#lang=...` metadata takes precedence and is recommended in media-note frontmatter.

## Track loading and selection

The plugin combines:

- Tracks linked from media-note frontmatter
- Sibling subtitle files for local media
- Hosted-service tracks, including YouTube captions

It sorts tracks using configured preferred languages plus the current Obsidian UI language. When `playback.track.default-enabled` is true, the first sorted track is enabled by default.

Relevant settings:

```json
{
  "playback.track.default-enabled": true,
  "playback.track.folder-path": null,
  "playback.track.default-languages": []
}
```

An empty default-language list does not necessarily mean no preference: version 4.2.7 also appends the current Obsidian language. Set `zh-Hans` explicitly only when the user wants a project-wide preference.

## UI actions found in version 4.2.7

The plugin exposes actions corresponding to:

- 添加字幕
- 从本地文件
- 从远程 URL
- 从相邻文件加载
- 打开转录文稿
- 下载字幕
- 转录模式 / 字幕模式
- 显示时间戳
- 高亮当前词

It supports WebVTT and also contains parsers/mime mappings for SRT, SSA, and ASS. Prefer VTT for this project because the existing tracks and transcript view use it.

## Timing behavior

Normal subtitle display requires only cue-level ranges:

```vtt
00:10.000 --> 00:14.000
中文字幕
```

Inline timestamps such as `<00:12.500>` enable finer-grained word timing in the English auto-generated track. A translated track without these inline timestamps still supports:

- Playback display
- Cue-level synchronization
- Transcript opening
- Cue-level seeking

It does not provide trustworthy per-word highlighting. Do not distribute source-language word timestamps across Chinese words heuristically and present them as accurate.

## Vault-layout caution

This repository can be opened in Obsidian in two ways:

1. Git root as vault: paths begin with `content/`; the nested Media Extended installation is not loaded.
2. `content/` as vault: Media Extended under `content/.obsidian/` is installed and enabled.

Before using `obsidian plugin:reload` or visual testing, check:

```bash
obsidian eval code="({name: app.vault.getName(), basePath: app.vault.adapter.basePath, enabled: app.plugins.enabledPlugins.has('media-extended')})"
```

Do not claim a live plugin test if the CLI is connected to the Git-root vault where `media-extended` is unavailable.
