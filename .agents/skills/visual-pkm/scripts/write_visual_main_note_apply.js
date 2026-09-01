(async () => {
  const resultKey = "__VISUAL_MAIN_NOTE_RESULT__";
  const cfg = globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  delete globalThis.__VISUAL_MAIN_NOTE_CONFIG__;
  if (!cfg || typeof cfg !== "object") throw new Error("缺少 Visual Main Note 配置");
  globalThis[resultKey] = { runId: cfg.runId, status: "running" };
  const debugPath = ".tmp_visual-pkm-write-progress.json";
  const checkpoint = async (stage, details = {}) => {
    await app.vault.adapter.write(
      debugPath,
      JSON.stringify({ stage, details, at: new Date().toISOString() }, null, 2),
    );
  };

  try {
    await checkpoint("start");
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const plugin = app.plugins.getPlugin("obsidian-excalidraw-plugin");
    if (!plugin) throw new Error("Excalidraw 插件未启用");

    const targetPath = String(cfg.targetPath || "");
    const spec = cfg.visualSpec;
    if (!targetPath.startsWith("Knowledge/Notes/") || !targetPath.endsWith(".md")) {
      throw new Error(`目标不是 Knowledge/Notes/*.md：${targetPath}`);
    }
    if (!spec || !Array.isArray(spec.elements) || !spec.elements.length) {
      throw new Error("完整视觉规格缺少 elements");
    }

    const getFile = (path) => {
      const file = app.vault.getAbstractFileByPath(path);
      if (!file || !file.stat || typeof file.path !== "string") {
        throw new Error(`文件不存在：${path}`);
      }
      return file;
    };
    const activeElements = (elements) =>
      (elements || []).filter((element) => element && !element.isDeleted);

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
      const markers = [
        body.indexOf("\n# Excalidraw Data"),
        body.indexOf("\n==⚠  Switch to EXCALIDRAW VIEW"),
      ].filter((index) => index >= 0);
      const drawingIndex = markers.length ? Math.min(...markers) : -1;
      return {
        frontmatter,
        knowledgeBody: (drawingIndex >= 0 ? body.slice(0, drawingIndex) : body).trim(),
      };
    };

    const normalizedFrontmatter = (file) => {
      const frontmatter = app.metadataCache.getFileCache(file)?.frontmatter || {};
      const clean = {};
      for (const [key, value] of Object.entries(frontmatter)) {
        if (["position", "excalidraw-plugin", "date", "updated"].includes(key)) continue;
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
    const removeGeneratedExcalidrawTag = (text) => {
      const normalized = String(text).replace(/\r\n/g, "\n");
      if (!normalized.startsWith("---\n")) return normalized;
      const end = normalized.indexOf("\n---\n", 4);
      if (end < 0) throw new Error("frontmatter 未闭合，无法移除插件标签");
      const lines = normalized.slice(4, end).split("\n");
      const output = [];
      for (let index = 0; index < lines.length; index += 1) {
        const line = lines[index];
        const inline = line.match(/^(\s*tags\s*:\s*)\[(.*)\](\s*)$/i);
        if (inline) {
          const kept = inline[2]
            .split(",")
            .map((value) => value.trim())
            .filter(Boolean)
            .filter(
              (value) => value.replace(/^['"]|['"]$/g, "").trim() !== "excalidraw",
            );
          if (kept.length) output.push(`${inline[1]}[${kept.join(", ")}]${inline[3]}`);
          continue;
        }
        if (/^\s*tags\s*:\s*['"]?excalidraw['"]?\s*$/i.test(line)) continue;
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
          if (kept.length) output.push(line, ...kept);
          index = cursor - 1;
          continue;
        }
        output.push(line);
      }
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
        throw new Error("目标知识卡在 dry-run 后发生变化（文件大小不同）");
      }
      if (
        cfg.expectedMtime != null &&
        Math.abs(Number(file.stat.mtime) - Number(cfg.expectedMtime)) > 2000
      ) {
        throw new Error("目标知识卡在 dry-run 后发生变化（修改时间不同）");
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
      if (!app.commands.executeCommandById("obsidian-excalidraw-plugin:convert-to-excalidraw")) {
        throw new Error("Excalidraw 转换命令未执行");
      }
    } else {
      await leaf.setViewState({ type: "excalidraw", state: { file: targetPath }, active: true });
      app.workspace.revealLeaf(leaf);
    }
    await waitFor(
      () =>
        leaf.view?.getViewType?.() === "excalidraw" &&
        leaf.view?.file?.path === targetPath &&
        leaf.view?._loaded,
      `Excalidraw 视图未就绪：${targetPath}`,
    );
    await checkpoint("view-ready");

    file = getFile(targetPath);
    let afterConversionText = await app.vault.read(file);
    let afterConversionFrontmatter = normalizedFrontmatter(file);
    const afterTags = tagsFromFrontmatter(afterConversionFrontmatter);
    if (!beforeTags.includes("excalidraw") && afterTags.includes("excalidraw")) {
      const cleaned = removeGeneratedExcalidrawTag(afterConversionText);
      await app.vault.modify(file, cleaned);
      await sleep(300);
      afterConversionText = await app.vault.read(file);
      afterConversionFrontmatter = normalizedFrontmatter(file);
      if (leaf.view?.getViewType?.() !== "excalidraw") {
        await leaf.setViewState({
          type: "excalidraw",
          state: { file: targetPath },
          active: true,
        });
        await waitFor(
          () => leaf.view?.getViewType?.() === "excalidraw" && leaf.view?._loaded,
          `标签清理后 Excalidraw 视图未就绪：${targetPath}`,
        );
      }
    }
    if (splitMarkdown(afterConversionText).knowledgeBody !== beforeMarkdown.knowledgeBody) {
      throw new Error("Excalidraw 初始化改变了知识卡正文");
    }
    if (!equalValue(beforeFrontmatter, afterConversionFrontmatter)) {
      throw new Error("Excalidraw 初始化改变了原有 frontmatter");
    }

    const view = leaf.view;
    const viewEA = plugin.ea;
    viewEA.setView(view);
    const sceneApi = viewEA.getExcalidrawAPI();
    if (!alreadyDrawing) {
      const background = spec.canvas?.background;
      if (background && background !== "transparent") {
        sceneApi.updateScene({ appState: { viewBackgroundColor: background } });
      }
    }

    let originalElements = activeElements(viewEA.getViewElements());
    await checkpoint("scene-read", { elements: originalElements.length });
    const oldGenerated = originalElements.filter(
      (element) => element.customData?.visualPkm?.visualId === spec.visual_id,
    );
    let baseX = 0;
    let baseY = 0;
    if (oldGenerated.length) {
      baseX = Math.min(...oldGenerated.map((element) => Number(element.x || 0)));
      baseY = Math.min(...oldGenerated.map((element) => Number(element.y || 0)));
      if (!viewEA.deleteViewElements(oldGenerated)) {
        throw new Error(`无法替换旧视觉：${spec.visual_id}`);
      }
      // Do not save the transient empty scene. Saving between deletion and insertion
      // makes Excalidraw treat the note as an empty drawing and can trigger its backup
      // recovery modal, which blocks the same atomic replacement run.
      originalElements = activeElements(viewEA.getViewElements());
      await checkpoint("old-generation-deleted", {
        deleted: oldGenerated.length,
        remaining: originalElements.length,
      });
    } else if (originalElements.length) {
      baseX =
        Math.max(
          ...originalElements.map(
            (element) => Number(element.x || 0) + Math.abs(Number(element.width || 0)),
          ),
        ) + 200;
      baseY = Math.min(...originalElements.map((element) => Number(element.y || 0)));
    }

    const preservedIds = new Set(originalElements.map((element) => element.id));
    const builder = plugin.ea.getAPI();
    builder.reset();
    builder.setView(view);
    await checkpoint("builder-ready");

    const applyStyle = (style = {}) => {
      const merged = { ...(spec.defaults || {}), ...style };
      for (const key of [
        "strokeColor",
        "backgroundColor",
        "fillStyle",
        "strokeWidth",
        "strokeStyle",
        "roughness",
        "opacity",
        "fontSize",
        "textAlign",
        "verticalAlign",
      ]) {
        if (merged[key] != null) builder.style[key] = merged[key];
      }
      builder.style.startArrowHead =
        merged.startArrowHead === "none" ? null : merged.startArrowHead || null;
      builder.style.endArrowHead =
        merged.endArrowHead === "none" ? null : merged.endArrowHead || "arrow";
    };

    const idsByKey = new Map();
    const idsByGroup = new Map();
    const componentFiles = new Map(
      (spec.reused_components || []).map((path) => [path, getFile(path)]),
    );
    try {
      let itemIndex = 0;
      for (const item of spec.elements) {
        itemIndex += 1;
        await checkpoint("adding-element", {
          index: itemIndex,
          total: spec.elements.length,
          key: item.key,
          type: item.type,
        });
        applyStyle(item.style);
        let id;
        if (item.type === "rectangle") {
          id = builder.addRect(baseX + item.x, baseY + item.y, item.width, item.height);
        } else if (item.type === "ellipse") {
          id = builder.addEllipse(baseX + item.x, baseY + item.y, item.width, item.height);
        } else if (item.type === "diamond") {
          id = builder.addDiamond(baseX + item.x, baseY + item.y, item.width, item.height);
        } else if (item.type === "text") {
          id = builder.addText(baseX + item.x, baseY + item.y, item.text, {
            autoResize: item.width == null,
            width: item.width,
            textAlign: item.textAlign || "left",
            textVerticalAlign: item.style?.verticalAlign || spec.defaults?.verticalAlign,
          });
        } else if (item.type === "line" || item.type === "arrow") {
          const points = item.points.map(([x, y]) => [baseX + x, baseY + y]);
          if (item.type === "line") {
            id = builder.addLine(points);
          } else {
            let startArrowHead = item.style?.startArrowHead || null;
            let endArrowHead = item.style?.endArrowHead || "arrow";
            if (item.style?.startArrowHead === "none") startArrowHead = null;
            if (item.style?.endArrowHead === "none") endArrowHead = null;
            id = builder.addArrow(points, { startArrowHead, endArrowHead });
          }
        } else if (item.type === "icon") {
          const componentFile = componentFiles.get(item.path) || getFile(item.path);
          id = await builder.addImage(baseX + item.x, baseY + item.y, componentFile, true, true);
          const image = builder.getElement(id);
          if (item.width || item.height) {
            const ratio = Math.abs(Number(image.width || 1) / Number(image.height || 1));
            if (item.width && item.height) {
              image.width = item.width;
              image.height = item.height;
            } else if (item.width) {
              image.width = item.width;
              image.height = item.width / ratio;
            } else {
              image.height = item.height;
              image.width = item.height * ratio;
            }
          }
        } else {
          throw new Error(`不支持的元素类型：${item.type}`);
        }
        if (!id) throw new Error(`生成元素失败：${item.key}`);
        const generated = builder.getElement(id);
        generated.customData = {
          ...(generated.customData || {}),
          visualPkm: {
            visualId: spec.visual_id,
            key: item.key,
            group: item.group || null,
            role: item.role,
            specHash: cfg.specHash,
          },
        };
        idsByKey.set(item.key, id);
        if (item.group) {
          if (!idsByGroup.has(item.group)) idsByGroup.set(item.group, []);
          idsByGroup.get(item.group).push(id);
        }
      }

      await checkpoint("elements-built", { count: idsByKey.size });
      for (const ids of idsByGroup.values()) {
        if (ids.length > 1) builder.addToGroup(ids);
      }
      await checkpoint("groups-built", { count: idsByGroup.size });
      const added = await builder.addElementsToView(false, false, true, false);
      if (!added) throw new Error("完整视觉写入目标 Drawing 失败");
      await checkpoint("elements-added-to-view");
      await view.forceSave(true);
      await checkpoint("first-save-done");
    } finally {
      builder.destroy();
    }

    viewEA.setView(view);
    const savedElements = activeElements(viewEA.getViewElements());
    const savedById = new Map(savedElements.map((element) => [element.id, element]));
    const missingPreserved = [...preservedIds].filter((id) => !savedById.has(id));
    if (missingPreserved.length) {
      throw new Error(`完整视觉写入丢失了 ${missingPreserved.length} 个原有元素`);
    }
    const generated = savedElements.filter(
      (element) => element.customData?.visualPkm?.visualId === spec.visual_id,
    );
    if (generated.length !== spec.elements.length) {
      throw new Error(
        `完整视觉元素数量不一致：预期 ${spec.elements.length}，实际 ${generated.length}`,
      );
    }

    const finalText = await app.vault.read(file);
    if (splitMarkdown(finalText).knowledgeBody !== beforeMarkdown.knowledgeBody) {
      throw new Error("保存完整视觉后知识卡正文发生变化");
    }
    await waitFor(
      () => equalValue(beforeFrontmatter, normalizedFrontmatter(file)),
      "保存完整视觉后原有 frontmatter 发生变化",
      5000,
    );
    if (!/(^|\n)excalidraw-plugin\s*:\s*parsed\s*($|\n)/.test(finalText)) {
      throw new Error("目标缺少 excalidraw-plugin: parsed");
    }
    if (!finalText.includes("```compressed-json")) {
      throw new Error("目标缺少插件生成的 compressed-json Drawing");
    }

    viewEA.viewZoomToElements(false, generated, 0.12);
    await view.forceSave(true);
    await checkpoint("final-save-done", { generated: generated.length });
    const result = {
      status: "applied",
      mode: cfg.mode,
      target_note: targetPath,
      created,
      drawing_preexisted: alreadyDrawing,
      visual_id: spec.visual_id,
      spec_sha256: cfg.specHash,
      generated_elements: generated.length,
      groups: Object.fromEntries([...idsByGroup].map(([key, ids]) => [key, ids.length])),
      reused_components: spec.reused_components || [],
      replaced_previous_generation: oldGenerated.length,
      original_elements_preserved: preservedIds.size,
      view_type: view.getViewType(),
    };
    globalThis[resultKey] = { runId: cfg.runId, status: "done", result };
    if (await app.vault.adapter.exists(debugPath)) {
      await app.vault.adapter.remove(debugPath);
    }
    return JSON.stringify(result);
  } catch (error) {
    try {
      await checkpoint("error", {
        message: error instanceof Error ? error.message : String(error),
      });
    } catch {
      // Keep the original error if debug checkpointing also fails.
    }
    globalThis[resultKey] = {
      runId: cfg.runId,
      status: "error",
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : null,
    };
    throw error;
  }
})()
