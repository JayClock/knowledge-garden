(async () => {
  const resultKey = "__VISUAL_MAIN_NOTE_RESULT__";
  const cfg = globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  delete globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  if (!cfg || typeof cfg !== "object") throw new Error("缺少 icon 自动提取配置");
  globalThis[resultKey] = { runId: cfg.runId, status: "running" };

  try {
    const plugin = app.plugins.getPlugin("obsidian-excalidraw-plugin");
    if (!plugin) throw new Error("Excalidraw 插件未启用");
    const notePath = String(cfg.notePath || "");
    const spec = cfg.extractionSpec;
    if (!notePath.startsWith("Knowledge/Notes/") || !notePath.endsWith(".md")) {
      throw new Error(`目标不是 Knowledge/Notes/*.md：${notePath}`);
    }
    if (!spec || !Array.isArray(spec.icons)) throw new Error("缺少自动提取 icons 规格");

    const getFile = (path) => {
      const file = app.vault.getAbstractFileByPath(path);
      if (!file || !file.stat || typeof file.path !== "string") {
        throw new Error(`文件不存在：${path}`);
      }
      return file;
    };
    const noteFile = getFile(notePath);
    const scene = await plugin.ea.getSceneFromFile(noteFile);
    const elements = (scene?.elements || []).filter((element) => element && !element.isDeleted);
    const visualElements = elements.filter(
      (element) => element.customData?.visualPkm?.visualId === spec.visual_id,
    );
    if (!visualElements.length) {
      throw new Error(`知识卡中找不到 AI 生成视觉：${spec.visual_id}`);
    }

    const randomId = () => {
      const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const bytes = new Uint8Array(20);
      crypto.getRandomValues(bytes);
      return [...bytes].map((value) => alphabet[value % alphabet.length]).join("");
    };
    const created = [];
    const reports = [];

    for (const candidate of spec.icons) {
      if (app.vault.getAbstractFileByPath(candidate.path)) {
        throw new Error(`Icon Library 目标已存在，停止覆盖：${candidate.path}`);
      }
      const selected = visualElements.filter(
        (element) => element.customData?.visualPkm?.group === candidate.group,
      );
      if (!selected.length) {
        throw new Error(`成品中找不到待提取 group：${candidate.group}`);
      }
      if (
        selected.some(
          (element) =>
            ["image", "frame", "embeddable"].includes(element.type) ||
            element.frameId != null,
        )
      ) {
        throw new Error(
          `group ${candidate.group} 包含 image/frame/embeddable，不能提取为原生 icon`,
        );
      }

      const selectedIds = new Set(selected.map((element) => element.id));
      const minX = Math.min(...selected.map((element) => Number(element.x || 0)));
      const minY = Math.min(...selected.map((element) => Number(element.y || 0)));
      const groupId = randomId();
      const idMap = new Map(selected.map((element) => [element.id, randomId()]));
      const extracted = selected.map((element) => {
        const clone = structuredClone(element);
        clone.id = idMap.get(element.id);
        clone.x = Number(clone.x || 0) - minX;
        clone.y = Number(clone.y || 0) - minY;
        clone.groupIds = [groupId];
        clone.frameId = null;
        clone.containerId = null;
        clone.startBinding = null;
        clone.endBinding = null;
        clone.boundElements = (clone.boundElements || [])
          .filter((binding) => selectedIds.has(binding.id))
          .map((binding) => ({ ...binding, id: idMap.get(binding.id) }));
        clone.customData = {};
        clone.link = null;
        clone.locked = false;
        clone.isDeleted = false;
        clone.version = Math.max(1, Number(clone.version || 1));
        clone.versionNonce = Math.floor(Math.random() * 2147483647);
        clone.updated = Date.now();
        return clone;
      });

      const iconScene = {
        type: "excalidraw",
        version: 2,
        source: "visual-pkm",
        elements: extracted,
        appState: {
          gridSize: null,
          viewBackgroundColor: "#ffffff",
        },
        files: {},
      };
      const folder = app.vault.getAbstractFileByPath("Knowledge/Assets/Excalidraw");
      if (!folder) throw new Error("Icon Library 目录不存在");
      const iconFile = await app.vault.create(
        candidate.path,
        JSON.stringify(iconScene, null, 2),
      );
      const saved = await plugin.ea.getSceneFromFile(iconFile);
      const savedElements = (saved?.elements || []).filter(
        (element) => element && !element.isDeleted,
      );
      if (savedElements.length !== extracted.length) {
        throw new Error(`提取后元素数量不一致：${candidate.path}`);
      }
      if (
        savedElements.some((element) =>
          ["image", "frame", "embeddable"].includes(element.type),
        )
      ) {
        throw new Error(`提取结果不是纯原生组件：${candidate.path}`);
      }
      let commonGroups = new Set(savedElements[0]?.groupIds || []);
      for (const element of savedElements.slice(1)) {
        const groups = new Set(element.groupIds || []);
        commonGroups = new Set([...commonGroups].filter((group) => groups.has(group)));
      }
      if (commonGroups.size !== 1) {
        throw new Error(`提取结果没有唯一公共 group：${candidate.path}`);
      }
      created.push(candidate.path);
      reports.push({
        path: candidate.path,
        source_group: candidate.group,
        elements: savedElements.length,
        colors_preserved: true,
      });
    }

    const result = {
      status: "applied",
      note: notePath,
      visual_id: spec.visual_id,
      created_icons: created,
      reports,
      source_visual_unchanged: true,
    };
    globalThis[resultKey] = { runId: cfg.runId, status: "done", result };
    return JSON.stringify(result);
  } catch (error) {
    globalThis[resultKey] = {
      runId: cfg.runId,
      status: "error",
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : null,
    };
    throw error;
  }
})()
