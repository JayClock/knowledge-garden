(async () => {
  const options = globalThis.PALETTE_SYNC_OPTIONS || {};
  const fs = require("fs");
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const normalizeHex = (value) => {
    const text = String(value ?? "").trim();
    return /^#[0-9a-f]{6}$/i.test(text) ? text.toUpperCase() : text.toUpperCase();
  };
  const isHex = (value) => /^#[0-9A-F]{6}$/.test(value);
  const isIgnoredColor = (value) =>
    !value || value === "TRANSPARENT" || value === "NONE" || /^#[0-9A-F]{6}00$/.test(value);
  const configPath = options.configPath;
  if (!configPath) throw new Error("PALETTE_SYNC_OPTIONS.configPath is required");

  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  if (config.schemaVersion !== 1) throw new Error(`Unsupported sync-state schema: ${config.schemaVersion}`);
  if (!Array.isArray(config.managedFiles)) throw new Error("managedFiles must be an array");
  const requestedPaths = [
    ...new Set((Array.isArray(options.paths) ? options.paths : []).map((path) => String(path || "").trim()).filter(Boolean)),
  ];
  const targeted = requestedPaths.length > 0;
  if (!targeted && !config.managedFiles.length) throw new Error("No managedFiles configured");
  const isPaletteDrawingPath = (path) =>
    (path.startsWith("Knowledge/Notes/") || path.startsWith("Knowledge/Maps/")) &&
    path.endsWith(".md");
  for (const path of requestedPaths) {
    if (!isPaletteDrawingPath(path)) {
      throw new Error(
        `Targeted palette audit only accepts Knowledge/Notes/*.md or Knowledge/Maps/*.md: ${path}`,
      );
    }
  }
  const configuredByPath = new Map(config.managedFiles.map((item) => [item.path, item]));
  const defaultBackgroundRole = (path) =>
    path.startsWith("Knowledge/Maps/")
      ? "--concept-color-warm-fill"
      : "--concept-color-canvas";
  const managedItems = targeted
    ? requestedPaths.map((path) => ({
        path,
        backgroundRole: configuredByPath.get(path)?.backgroundRole || defaultBackgroundRole(path),
      }))
    : config.managedFiles;

  const plugin = app.plugins.plugins["obsidian-excalidraw-plugin"];
  if (!plugin?.ea) throw new Error("Obsidian Excalidraw plugin is not available");
  const ea = plugin.ea;

  const readPaletteCss = async (path) => {
    if (/^(?:\/|[A-Za-z]:[\\/])/.test(path)) return fs.readFileSync(path, "utf8");
    const file = app.vault.getAbstractFileByPath(path);
    if (!file) throw new Error(`Palette CSS not found: ${path}`);
    return await app.vault.read(file);
  };
  const css = await readPaletteCss(config.paletteCss);
  const cssValues = {};
  for (const match of css.matchAll(/(--concept-color-[a-z0-9-]+)\s*:\s*(#[0-9a-f]{6})\s*;/gi)) {
    cssValues[match[1]] = normalizeHex(match[2]);
  }

  const roles = Object.keys(config.lastApplied || {});
  if (!roles.length) throw new Error("lastApplied palette snapshot is empty");
  const oldPalette = {};
  const newPalette = {};
  for (const role of roles) {
    oldPalette[role] = normalizeHex(config.lastApplied[role]);
    newPalette[role] = cssValues[role];
    if (!newPalette[role]) throw new Error(`Missing base variable in CSS: ${role}`);
  }

  const assertUnique = (palette, label) => {
    const seen = new Map();
    for (const [role, color] of Object.entries(palette)) {
      if (seen.has(color)) throw new Error(`${label} duplicates ${color}: ${seen.get(color)} and ${role}`);
      seen.set(color, role);
    }
    return seen;
  };
  const oldRoleByColor = assertUnique(oldPalette, "lastApplied");
  assertUnique(newPalette, "current CSS palette");
  for (const [role, color] of Object.entries(newPalette)) {
    const oldRole = oldRoleByColor.get(color);
    if (oldRole && oldRole !== role && oldPalette[role] !== color) {
      throw new Error(`Cross-role color collision: ${role} now uses the previous value of ${oldRole} (${color})`);
    }
  }

  const oldToNew = new Map(roles.map((role) => [oldPalette[role], newPalette[role]]));
  const allowedDuringMigration = new Set([...Object.values(oldPalette), ...Object.values(newPalette)]);
  const allowedAfterApply = new Set(Object.values(newPalette));
  const roleChanges = roles
    .filter((role) => oldPalette[role] !== newPalette[role])
    .map((role) => ({ role, from: oldPalette[role], to: newPalette[role] }));

  const parseEmbeddedFiles = (text) => {
    const result = {};
    const regex = /^([a-f0-9]+): \[\[([^\]|]+)(?:\|[^\]]+)?\]\](?:\s+(\{.*\}))?$/gm;
    for (const match of text.matchAll(regex)) {
      let colorMap = {};
      try { colorMap = match[3] ? JSON.parse(match[3]) : {}; } catch (_) {}
      result[match[1]] = { path: match[2], colorMap };
    }
    return result;
  };
  const auditColor = (color, context, unknowns) => {
    const normalized = normalizeHex(color);
    if (isIgnoredColor(normalized)) return;
    if (!isHex(normalized) || !allowedDuringMigration.has(normalized)) unknowns.push({ ...context, color: normalized });
  };

  const resolveEmbeddedFile = (linkPath, sourcePath) => {
    const direct = app.vault.getAbstractFileByPath(linkPath);
    if (direct) return direct;
    if (!linkPath.includes("/") && linkPath.endsWith(".excalidraw")) {
      const icon = app.vault.getAbstractFileByPath(
        `Knowledge/Assets/Excalidraw/${linkPath}`,
      );
      if (icon) return icon;
    }
    return app.metadataCache.getFirstLinkpathDest(linkPath, sourcePath);
  };

  const preflight = [];
  const allUnknowns = [];
  const unsupportedImages = [];
  const componentSceneCache = new Map();
  for (const item of managedItems) {
    const file = app.vault.getAbstractFileByPath(item.path);
    if (!file) throw new Error(`Managed drawing not found: ${item.path}`);
    if (!newPalette[item.backgroundRole]) throw new Error(`Unknown backgroundRole for ${item.path}: ${item.backgroundRole}`);
    const text = await app.vault.read(file);
    const scene = await ea.getSceneFromFile(file);
    const embedded = parseEmbeddedFiles(text);
    let elementFields = 0;
    let changedElements = 0;
    const changedIds = new Set();
    for (const element of scene.elements) {
      if (element.type === "image") continue;
      for (const field of ["strokeColor", "backgroundColor"]) {
        const color = normalizeHex(element[field]);
        auditColor(color, { path: item.path, kind: "element", id: element.id, type: element.type, field }, allUnknowns);
        if (oldToNew.has(color) && oldToNew.get(color) !== color) {
          elementFields += 1;
          changedIds.add(element.id);
        }
      }
    }
    changedElements = changedIds.size;
    const imageInstances = 0;
    for (const element of scene.elements.filter((el) => el.type === "image")) {
      const entry = embedded[element.fileId];
      if (!entry) {
        unsupportedImages.push({
          path: item.path,
          id: element.id,
          fileId: element.fileId,
          image: null,
          reason: "image reference is not backed by an Embedded Files wikilink",
        });
        continue;
      }
      const linked = resolveEmbeddedFile(entry.path, item.path);
      if (!linked) {
        unsupportedImages.push({
          path: item.path,
          id: element.id,
          fileId: element.fileId,
          image: entry.path,
          reason: "embedded image target cannot be resolved",
        });
        continue;
      }
      if (isPaletteDrawingPath(linked.path)) {
        const linkedText = await app.vault.read(linked);
        if (!/^---\n[\s\S]*?^excalidraw-plugin:\s*parsed\s*$[\s\S]*?^---$/m.test(linkedText)) {
          unsupportedImages.push({
            path: item.path,
            id: element.id,
            fileId: element.fileId,
            image: linked.path,
            reason: "embedded Knowledge drawing is not a parsed Excalidraw Markdown file",
          });
        }
        continue;
      }
      if (
        !linked.path.startsWith("Knowledge/Assets/Excalidraw/Icon - ") ||
        !linked.path.endsWith(".excalidraw")
      ) {
        unsupportedImages.push({
          path: item.path,
          id: element.id,
          fileId: element.fileId,
          image: linked.path,
          reason: "image references must point to parsed Knowledge drawings or traced native .excalidraw icons",
        });
        continue;
      }
      let componentScene = componentSceneCache.get(linked.path);
      if (!componentScene) {
        componentScene = await ea.getSceneFromFile(linked);
        componentSceneCache.set(linked.path, componentScene);
      }
      const componentElements = (componentScene.elements || []).filter(
        (nested) => nested && !nested.isDeleted,
      );
      if (!componentElements.length) {
        unsupportedImages.push({
          path: item.path,
          id: element.id,
          fileId: element.fileId,
          image: linked.path,
          reason: "traced icon component has no native elements",
        });
        continue;
      }
      let commonGroups = new Set(componentElements[0].groupIds || []);
      for (const nested of componentElements.slice(1)) {
        const groups = new Set(nested.groupIds || []);
        commonGroups = new Set([...commonGroups].filter((group) => groups.has(group)));
      }
      if (commonGroups.size !== 1) {
        unsupportedImages.push({
          path: item.path,
          id: element.id,
          fileId: element.fileId,
          image: linked.path,
          reason: "traced icon component must have one public group",
        });
      }
      for (const nested of componentElements) {
        if (["image", "frame", "embeddable"].includes(nested.type) || nested.frameId != null) {
          unsupportedImages.push({
            path: item.path,
            id: element.id,
            fileId: element.fileId,
            image: linked.path,
            reason: `nested ${nested.type || "framed element"} is not a native flat icon component`,
          });
        }
      }
    }
    const expectedBackground = newPalette[item.backgroundRole];
    const currentBackground = normalizeHex(scene.appState?.viewBackgroundColor);
    auditColor(currentBackground, { path: item.path, kind: "appState", field: "viewBackgroundColor" }, allUnknowns);
    preflight.push({
      path: item.path,
      file,
      text,
      knowledge: text.split("# Excalidraw Data", 1)[0],
      elementCount: scene.elements.length,
      elementIds: scene.elements.map((el) => el.id),
      changedElements,
      elementFields,
      imageInstances,
      imageMappings: 0,
      backgroundFrom: currentBackground,
      backgroundTo: expectedBackground,
      backgroundChanged: currentBackground !== expectedBackground,
      needsWrite: elementFields > 0 || imageInstances > 0 || currentBackground !== expectedBackground,
    });
  }

  if (unsupportedImages.length) {
    const sample = unsupportedImages
      .slice(0, 12)
      .map((x) => `${x.path}: image ${x.id} (${x.image || x.fileId}): ${x.reason}`)
      .join("\n");
    throw new Error(`Icon structure check stopped: ${unsupportedImages.length} non-native image references found.\n${sample}`);
  }
  if (config.strict !== false && allUnknowns.length) {
    const sample = allUnknowns.slice(0, 12).map((x) => {
      const owner = x.component ? ` ${x.component}:${x.componentElement || "appState"}` : "";
      return `${x.path}: ${x.kind}.${x.field}${owner}=${x.color}`;
    }).join("\n");
    throw new Error(`Palette sync stopped: ${allUnknowns.length} non-palette color fields found.\n${sample}`);
  }

  const mode = options.apply ? "apply" : "check";
  const report = {
    schemaVersion: 1,
    mode,
    scope: targeted ? "targeted" : "managed",
    paletteCss: config.paletteCss,
    roleChanges,
    managedFiles: preflight.length,
    filesNeedingWrite: preflight.filter((x) => x.needsWrite).length,
    changesPending: targeted
      ? preflight.some((x) => x.needsWrite)
      : roleChanges.length > 0 || preflight.some((x) => x.needsWrite),
    plannedElementFields: preflight.reduce((sum, x) => sum + x.elementFields, 0),
    plannedImageInstances: preflight.reduce((sum, x) => sum + x.imageInstances, 0),
    plannedBackgrounds: preflight.filter((x) => x.backgroundChanged).length,
    unknownColors: allUnknowns,
    unsupportedImages,
    files: preflight.map(({ file, text, knowledge, elementIds, ...x }) => x),
    applied: false,
    stateUpdated: false,
    registeredFiles: [],
    updatedRegisteredFiles: [],
    alreadyRegisteredFiles: [],
  };

  const waitForView = async (path) => {
    for (let i = 0; i < 240; i += 1) {
      const view = plugin.activeExcalidrawView;
      if (view?.file?.path === path && view.excalidrawAPI && view.excalidrawAPI.getSceneElements().length) {
        await sleep(500);
        return view;
      }
      await sleep(100);
    }
    throw new Error(`Timed out opening Excalidraw view: ${path}`);
  };

  if (options.apply && report.changesPending) {
    const leaf = app.workspace.getLeaf(false);
    const originalFile = leaf?.view?.file || null;
    try {
      for (const plan of preflight.filter((x) => x.needsWrite)) {
        await leaf.openFile(plan.file, { active: true });
        const view = await waitForView(plan.path);
        ea.setView(view);
        const current = view.excalidrawAPI.getSceneElements();
        const beforeIds = new Set(current.map((el) => el.id));
        const updated = current.map((element) => {
          if (element.type === "image") return element;
          let next = element;
          let changed = false;
          for (const field of ["strokeColor", "backgroundColor"]) {
            const color = normalizeHex(element[field]);
            const replacement = oldToNew.get(color);
            if (replacement && replacement !== color) {
              if (!changed) next = { ...element };
              next[field] = replacement;
              changed = true;
            }
          }
          if (changed) {
            next.version = element.version + 1;
            next.versionNonce = Math.floor(Math.random() * 2147483647);
            next.updated = Date.now();
          }
          return next;
        });
        view.excalidrawAPI.updateScene({
          elements: updated,
          appState: { viewBackgroundColor: plan.backgroundTo },
        });
        await sleep(150);

        await view.forceSave(true);
        await sleep(450);

        const afterText = await app.vault.read(plan.file);
        if (afterText.split("# Excalidraw Data", 1)[0] !== plan.knowledge) throw new Error(`Knowledge body changed: ${plan.path}`);
        const after = await ea.getSceneFromFile(plan.file);
        if (after.elements.length !== plan.elementCount) throw new Error(`Element count changed: ${plan.path}`);
        const afterIds = new Set(after.elements.map((el) => el.id));
        if ([...beforeIds].some((id) => !afterIds.has(id))) throw new Error(`Element IDs changed: ${plan.path}`);
        if (normalizeHex(after.appState?.viewBackgroundColor) !== plan.backgroundTo) throw new Error(`Background sync failed: ${plan.path}`);
        for (const element of after.elements) {
          if (element.type === "image") continue;
          for (const field of ["strokeColor", "backgroundColor"]) {
            const color = normalizeHex(element[field]);
            if (!isIgnoredColor(color) && (!isHex(color) || !allowedAfterApply.has(color))) {
              throw new Error(`Post-sync non-palette color: ${plan.path} ${element.id}.${field}=${color}`);
            }
          }
        }
        ea.clear();
      }
    } finally {
      ea.clear();
      if (originalFile && app.vault.getAbstractFileByPath(originalFile.path)) {
        try { await leaf.openFile(originalFile, { active: true }); } catch (_) {}
      }
    }

    if (!targeted) {
      config.lastApplied = Object.fromEntries(roles.map((role) => [role, newPalette[role]]));
      config.lastAppliedAt = new Date().toISOString();
      fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`);
      report.stateUpdated = true;
    }
    report.applied = true;
  }

  if (targeted && options.register) {
    for (const item of managedItems) {
      const existing = configuredByPath.get(item.path);
      if (existing) {
        if (existing.backgroundRole !== item.backgroundRole) {
          existing.backgroundRole = item.backgroundRole;
          report.updatedRegisteredFiles.push(item.path);
        } else {
          report.alreadyRegisteredFiles.push(item.path);
        }
        continue;
      }
      config.managedFiles.push({
        path: item.path,
        backgroundRole: "--concept-color-canvas",
      });
      configuredByPath.set(item.path, item);
      report.registeredFiles.push(item.path);
    }
    if (report.registeredFiles.length || report.updatedRegisteredFiles.length) {
      fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`);
      report.stateUpdated = true;
    }
  }

  report.noOp = !report.changesPending;
  report.completedAt = new Date().toISOString();
  if (options.reportPath) fs.writeFileSync(options.reportPath, `${JSON.stringify(report, null, 2)}\n`);
  ea.clear();
  return JSON.stringify(report);
})()
