(async () => {
  const resultKey = "__VISUAL_MAIN_NOTE_RESULT__";
  const cfg = globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  delete globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  if (!cfg || typeof cfg !== "object") throw new Error("缺少 Visual Main Note 配置");
  globalThis[resultKey] = { runId: cfg.runId, status: "running" };

  try {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const plugin = app.plugins.getPlugin("obsidian-excalidraw-plugin");
  if (!plugin) throw new Error("Excalidraw 插件未启用");

  const targetPath = String(cfg.targetPath || "");
  if (!targetPath.startsWith("Knowledge/Notes/") || !targetPath.endsWith(".md")) {
    throw new Error(`目标不是 Knowledge/Notes/*.md：${targetPath}`);
  }
  const componentPaths = [...new Set(cfg.componentPaths || [])];
  if (!componentPaths.length) throw new Error("没有可嵌入的 Excalidraw icon 组件");
  const maxIconSize = Number(cfg.maxIconSize || 180);
  const gap = Number(cfg.gap ?? 48);
  if (!(maxIconSize > 0) || gap < 0) throw new Error("无效的 icon 尺寸或间距");

  const getFile = (path) => {
    const file = app.vault.getAbstractFileByPath(path);
    if (!file || !file.stat || typeof file.path !== "string") {
      throw new Error(`文件不存在：${path}`);
    }
    return file;
  };

  const componentFiles = componentPaths.map((path) => {
    if (
      !String(path).startsWith("Knowledge/Assets/Excalidraw/Icon - ") ||
      !String(path).endsWith(".excalidraw")
    ) {
      throw new Error(`无效 icon 组件路径：${path}`);
    }
    return getFile(path);
  });

  const paletteCssPath = "Knowledge/Assets/Styles/concept-visualization-palette.css";
  const paletteCss = await app.vault.read(getFile(paletteCssPath));
  const canvasMatch = paletteCss.match(
    /--concept-color-canvas\s*:\s*(#[0-9a-fA-F]{6})\s*;/,
  );
  if (!canvasMatch) throw new Error("项目色板缺少 --concept-color-canvas");
  const defaultCanvasColor = canvasMatch[1].toUpperCase();
  const normalizeColor = (value) => String(value || "").trim().toUpperCase();

  const activeElements = (elements) =>
    (elements || []).filter((element) => element && !element.isDeleted);

  for (const componentFile of componentFiles) {
    const scene = await plugin.ea.getSceneFromFile(componentFile);
    const elements = activeElements(scene?.elements);
    if (!elements.length) throw new Error(`icon 组件没有有效元素：${componentFile.path}`);
    if (
      elements.some(
        (element) =>
          ["image", "frame", "embeddable"].includes(element.type) ||
          element.frameId != null,
      )
    ) {
      throw new Error(`icon 组件包含嵌套 image/frame/embeddable：${componentFile.path}`);
    }
    let commonGroups = new Set(elements[0].groupIds || []);
    for (const element of elements.slice(1)) {
      const groups = new Set(element.groupIds || []);
      commonGroups = new Set([...commonGroups].filter((group) => groups.has(group)));
    }
    if (commonGroups.size !== 1) {
      throw new Error(`icon 组件没有唯一公共 group：${componentFile.path}`);
    }
  }

  const splitMarkdown = (text) => {
    const normalized = String(text || "").replace(/\r\n/g, "\n");
    let frontmatter = "";
    let body = normalized;
    if (normalized.startsWith("---\n")) {
      const end = normalized.indexOf("\n---\n", 4);
      if (end >= 0) {
        frontmatter = normalized.slice(4, end);
        body = normalized.slice(end + 5);
      }
    }
    const drawingMarkers = [
      body.indexOf("\n# Excalidraw Data"),
      body.indexOf("\n==⚠  Switch to EXCALIDRAW VIEW"),
    ].filter((index) => index >= 0);
    const drawingIndex = drawingMarkers.length ? Math.min(...drawingMarkers) : -1;
    const knowledgeBody = drawingIndex >= 0 ? body.slice(0, drawingIndex) : body;
    return { frontmatter, knowledgeBody: knowledgeBody.trim() };
  };

  const normalizedFrontmatter = (file) => {
    const frontmatter = app.metadataCache.getFileCache(file)?.frontmatter || {};
    const clean = {};
    for (const [key, value] of Object.entries(frontmatter)) {
      if (
        key === "position" ||
        key === "excalidraw-plugin" ||
        key === "date" ||
        key === "updated"
      ) continue;
      clean[key] = value;
    }
    return clean;
  };

  const stableValue = (value) => {
    if (Array.isArray(value)) return value.map(stableValue);
    if (value && typeof value === "object") {
      return Object.fromEntries(
        Object.keys(value)
          .sort()
          .map((key) => [key, stableValue(value[key])]),
      );
    }
    return value;
  };

  const equalValue = (left, right) =>
    JSON.stringify(stableValue(left)) === JSON.stringify(stableValue(right));

  const tagsFromFrontmatter = (frontmatter) => {
    const value = frontmatter?.tags;
    if (Array.isArray(value)) return value.map(String);
    if (typeof value === "string") {
      return value
        .replace(/^\[|\]$/g, "")
        .split(/[\s,]+/)
        .map((item) => item.replace(/^['"]|['"]$/g, ""))
        .filter(Boolean);
    }
    return [];
  };

  const removeAddedExcalidrawTag = (text) => {
    const normalized = String(text).replace(/\r\n/g, "\n");
    if (!normalized.startsWith("---\n")) return normalized;
    const end = normalized.indexOf("\n---\n", 4);
    if (end < 0) throw new Error("frontmatter 未闭合，无法移除插件工作流标签");
    const lines = normalized.slice(4, end).split("\n");
    const output = [];
    let removed = false;
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index];
      const inline = line.match(/^(\s*tags\s*:\s*)\[(.*)\](\s*)$/i);
      if (inline) {
        const values = inline[2]
          .split(",")
          .map((value) => value.trim())
          .filter(Boolean);
        const kept = values.filter(
          (value) => value.replace(/^['"]|['"]$/g, "").trim() !== "excalidraw",
        );
        if (kept.length !== values.length) removed = true;
        if (kept.length) output.push(`${inline[1]}[${kept.join(", ")}]${inline[3]}`);
        continue;
      }
      const scalar = line.match(/^(\s*tags\s*:\s*)(['"]?excalidraw['"]?)\s*$/i);
      if (scalar) {
        removed = true;
        continue;
      }
      if (/^\s*tags\s*:\s*$/i.test(line)) {
        const block = [];
        let cursor = index + 1;
        while (cursor < lines.length && /^\s+-\s+/.test(lines[cursor])) {
          block.push(lines[cursor]);
          cursor += 1;
        }
        const kept = block.filter(
          (item) =>
            item
              .replace(/^\s+-\s+/, "")
              .replace(/^['"]|['"]$/g, "")
              .trim() !== "excalidraw",
        );
        if (kept.length !== block.length) removed = true;
        if (kept.length) output.push(line, ...kept);
        index = cursor - 1;
        continue;
      }
      output.push(line);
    }
    if (!removed) return normalized;
    return `---\n${output.join("\n")}\n---\n${normalized.slice(end + 5)}`;
  };

  const waitFor = async (predicate, message, timeoutMs = 20000) => {
    const started = Date.now();
    while (Date.now() - started < timeoutMs) {
      const value = await predicate();
      if (value) return value;
      await sleep(150);
    }
    throw new Error(message);
  };

  let file = app.vault.getAbstractFileByPath(targetPath);
  let created = false;
  if (cfg.mode === "new") {
    if (file) throw new Error(`新知识卡目标已存在：${targetPath}`);
    if (typeof cfg.newContent !== "string" || !cfg.newContent.trim()) {
      throw new Error("新知识卡缺少最小内容");
    }
    file = await app.vault.create(targetPath, cfg.newContent);
    created = true;
  } else if (cfg.mode === "existing") {
    file = getFile(targetPath);
    if (cfg.expectedSize != null && Number(file.stat.size) !== Number(cfg.expectedSize)) {
      throw new Error("目标知识卡在 dry-run 后发生变化（文件大小不同），停止写入");
    }
    if (
      cfg.expectedMtime != null &&
      Math.abs(Number(file.stat.mtime) - Number(cfg.expectedMtime)) > 2000
    ) {
      throw new Error("目标知识卡在 dry-run 后发生变化（修改时间不同），停止写入");
    }
  } else {
    throw new Error(`无效模式：${cfg.mode}`);
  }

  const beforeText = await app.vault.read(file);
  await waitFor(
    () => {
      const cache = app.metadataCache.getFileCache(file);
      return beforeText.startsWith("---\n") ? cache?.frontmatter : cache;
    },
    `metadata 未就绪：${targetPath}`,
    10000,
  );
  const beforeMarkdown = splitMarkdown(beforeText);
  const beforeFrontmatter = normalizedFrontmatter(file);
  const beforeTags = tagsFromFrontmatter(beforeFrontmatter);
  const alreadyDrawing =
    /(^|\n)excalidraw-plugin\s*:\s*parsed\s*($|\n)/.test(beforeText) &&
    beforeText.includes("```compressed-json");

  let leaf = [
    ...app.workspace.getLeavesOfType("excalidraw"),
    ...app.workspace.getLeavesOfType("markdown"),
  ].find((candidate) => candidate.view?.file?.path === targetPath);
  if (!leaf) leaf = app.workspace.getLeaf("tab");
  if (!alreadyDrawing) {
    await leaf.setViewState({
      type: "markdown",
      state: { file: targetPath, mode: "source" },
      active: true,
    });
    app.workspace.revealLeaf(leaf);
    await sleep(250);
    const executed = app.commands.executeCommandById(
      "obsidian-excalidraw-plugin:convert-to-excalidraw",
    );
    if (!executed) throw new Error("Excalidraw 转换命令未执行");
    await waitFor(
      () =>
        leaf.view?.getViewType?.() === "excalidraw" &&
        leaf.view?.file?.path === targetPath &&
        leaf.view?._loaded,
      `Excalidraw 视图未就绪：${targetPath}`,
    );
  } else {
    await leaf.setViewState({ type: "excalidraw", state: { file: targetPath }, active: true });
    app.workspace.revealLeaf(leaf);
    await waitFor(
      () =>
        leaf.view?.getViewType?.() === "excalidraw" &&
        leaf.view?.file?.path === targetPath &&
        leaf.view?._loaded,
      `已有 Excalidraw 视图未就绪：${targetPath}`,
    );
  }

  file = getFile(targetPath);
  await sleep(250);
  let afterConversionText = await app.vault.read(file);
  let afterConversionFrontmatter = normalizedFrontmatter(file);
  const afterTags = tagsFromFrontmatter(afterConversionFrontmatter);
  if (!beforeTags.includes("excalidraw") && afterTags.includes("excalidraw")) {
    const cleaned = removeAddedExcalidrawTag(afterConversionText);
    if (cleaned === afterConversionText) {
      throw new Error("插件新增了 excalidraw 标签，但脚本无法安全移除");
    }
    await app.vault.modify(file, cleaned);
    await sleep(300);
    afterConversionText = await app.vault.read(file);
    afterConversionFrontmatter = normalizedFrontmatter(file);
  }

  if (splitMarkdown(afterConversionText).knowledgeBody !== beforeMarkdown.knowledgeBody) {
    throw new Error("Excalidraw 初始化改变了知识卡正文，停止嵌入");
  }
  if (!equalValue(beforeFrontmatter, afterConversionFrontmatter)) {
    throw new Error("Excalidraw 初始化改变了原有 frontmatter，停止嵌入");
  }

  if (leaf.view?.getViewType?.() !== "excalidraw" || leaf.view?.file?.path !== targetPath) {
    await leaf.setViewState({ type: "excalidraw", state: { file: targetPath }, active: true });
    await waitFor(
      () => leaf.view?.getViewType?.() === "excalidraw" && leaf.view?._loaded,
      `标签清理后 Excalidraw 视图未重新就绪：${targetPath}`,
    );
  }

  const view = leaf.view;
  const viewEA = plugin.ea;
  viewEA.setView(view);
  const currentScene = viewEA.getExcalidrawAPI();
  if (!alreadyDrawing) {
    currentScene.updateScene({
      appState: { viewBackgroundColor: defaultCanvasColor },
    });
    await sleep(150);
  }
  const originalElements = activeElements(viewEA.getViewElements());
  const originalIds = new Set(originalElements.map((element) => element.id));
  const existingByPath = new Map();
  for (const element of originalElements) {
    if (element.type !== "image") continue;
    const linked = viewEA.getViewFileForImageElement(element);
    if (linked?.path && !existingByPath.has(linked.path)) {
      existingByPath.set(linked.path, element);
    }
  }

  const nonDeleted = originalElements;
  const minY = nonDeleted.length
    ? Math.min(...nonDeleted.map((element) => Number(element.y || 0)))
    : 0;
  const maxX = nonDeleted.length
    ? Math.max(
        ...nonDeleted.map(
          (element) => Number(element.x || 0) + Math.abs(Number(element.width || 0)),
        ),
      )
    : -200;
  let cursorX = nonDeleted.length ? maxX + 200 : 0;
  const cursorY = minY;

  const builder = plugin.ea.getAPI();
  builder.reset();
  builder.setView(view);
  const addedIds = [];
  const reused = [];
  try {
    for (const componentFile of componentFiles) {
      if (existingByPath.has(componentFile.path)) {
        reused.push(componentFile.path);
        continue;
      }
      const newId = await builder.addImage(cursorX, cursorY, componentFile, true, true);
      if (!newId) throw new Error(`无法嵌入 icon：${componentFile.path}`);
      const generated = builder.getElement(newId);
      if (!generated || generated.type !== "image") {
        throw new Error(`Excalidraw 未生成 image reference：${componentFile.path}`);
      }
      const width = Math.abs(Number(generated.width || 1));
      const height = Math.abs(Number(generated.height || 1));
      const scale = Math.min(1, maxIconSize / Math.max(width, height));
      generated.x = cursorX;
      generated.y = cursorY;
      generated.width = width * scale;
      generated.height = height * scale;
      generated.groupIds = [];
      generated.frameId = null;
      generated.angle = 0;
      generated.locked = false;
      generated.backgroundColor = "transparent";
      generated.version = (generated.version || 1) + 1;
      generated.updated = Date.now();
      cursorX += generated.width + gap;
      addedIds.push(newId);
    }

    if (addedIds.length) {
      const added = await builder.addElementsToView(false, false, false, false);
      if (!added) throw new Error("把入选 icon 添加到目标 Drawing 失败");
      await view.forceSave(true);
    }
  } finally {
    builder.destroy();
  }

  viewEA.setView(view);
  const savedElements = activeElements(viewEA.getViewElements());
  const savedById = new Map(savedElements.map((element) => [element.id, element]));
  const missingOriginal = [...originalIds].filter((id) => !savedById.has(id));
  if (missingOriginal.length) {
    throw new Error(`嵌入操作丢失了 ${missingOriginal.length} 个原有场景元素`);
  }
  const unexpectedNew = savedElements.filter(
    (element) => !originalIds.has(element.id) && !addedIds.includes(element.id),
  );
  if (unexpectedNew.length) throw new Error("嵌入操作产生了未计划的场景元素");
  const invalidAdded = addedIds
    .map((id) => savedById.get(id))
    .filter((element) => !element || element.type !== "image");
  if (invalidAdded.length) throw new Error("新增项中存在非 image reference 元素");

  const resolvedPaths = new Map();
  for (const element of savedElements.filter((item) => item.type === "image")) {
    const linked = viewEA.getViewFileForImageElement(element);
    if (linked?.path && !resolvedPaths.has(linked.path)) {
      resolvedPaths.set(linked.path, element);
    }
  }
  const missingComponents = componentPaths.filter((path) => !resolvedPaths.has(path));
  if (missingComponents.length) {
    throw new Error(`保存后缺少 icon image reference：${missingComponents.join("、")}`);
  }

  const finalText = await app.vault.read(file);
  const finalMarkdown = splitMarkdown(finalText);
  const finalFrontmatter = normalizedFrontmatter(file);
  if (finalMarkdown.knowledgeBody !== beforeMarkdown.knowledgeBody) {
    throw new Error("保存 icon 后知识卡正文发生变化");
  }
  if (!equalValue(beforeFrontmatter, finalFrontmatter)) {
    throw new Error("保存 icon 后原有 frontmatter 发生变化");
  }
  if (!/(^|\n)excalidraw-plugin\s*:\s*parsed\s*($|\n)/.test(finalText)) {
    throw new Error("目标缺少 excalidraw-plugin: parsed");
  }
  if (!finalText.includes("```compressed-json")) {
    throw new Error("目标缺少插件生成的 compressed-json Drawing");
  }
  const finalScene = await viewEA.getSceneFromFile(file);
  const finalCanvasColor = normalizeColor(finalScene?.appState?.viewBackgroundColor);
  if (!alreadyDrawing && finalCanvasColor !== defaultCanvasColor) {
    throw new Error("首次初始化的知识卡画布背景没有保存为默认 --concept-color-canvas");
  }

  const stagingElements = componentPaths
    .map((path) => resolvedPaths.get(path))
    .filter(Boolean);
  if (stagingElements.length) {
    viewEA.viewZoomToElements(false, stagingElements, 0.15);
  }
  await view.forceSave(true);

  const result = {
    status: "applied",
    mode: cfg.mode,
    target_note: targetPath,
    created,
    drawing_preexisted: alreadyDrawing,
    requested_components: componentPaths,
    added_components: componentPaths.filter((path) => !reused.includes(path)),
    reused_components: reused,
    original_elements_preserved: originalIds.size,
    final_elements: savedElements.length,
    view_type: view.getViewType(),
    palette_css: paletteCssPath,
    canvas_background: finalCanvasColor,
    project_palette_required: false,
    icon_palette_gate: false,
    component_colors_preserved: true,
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
