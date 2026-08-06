(async () => {
  const options = globalThis.PALETTE_SYNC_OPTIONS || {};
  const fs = require("fs");
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const normalizeHex = (value) => {
    const text = String(value ?? "").trim();
    return /^#[0-9a-f]{6}$/i.test(text) ? text.toUpperCase() : text.toUpperCase();
  };
  const isHex = (value) => /^#[0-9A-F]{6}$/.test(value);
  const isIgnoredColor = (value) => !value || value === "TRANSPARENT";
  const configPath = options.configPath;
  if (!configPath) throw new Error("PALETTE_SYNC_OPTIONS.configPath is required");

  const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
  if (config.schemaVersion !== 1) throw new Error(`Unsupported sync-state schema: ${config.schemaVersion}`);
  if (!Array.isArray(config.managedFiles) || !config.managedFiles.length) throw new Error("No managedFiles configured");

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
    const regex = /^([a-f0-9]+): \[\[([^\]|]+\.svg)(?:\|[^\]]+)?\]\](?:\s+(\{.*\}))?$/gm;
    for (const match of text.matchAll(regex)) {
      let colorMap = {};
      try { colorMap = match[3] ? JSON.parse(match[3]) : {}; } catch (_) {}
      result[match[1]] = { path: match[2], colorMap };
    }
    return result;
  };
  const mappedColorMap = (colorMap) => {
    let changed = false;
    const next = { ...(colorMap || {}) };
    for (const [key, value] of Object.entries(next)) {
      const color = normalizeHex(value);
      if (isHex(color) && oldToNew.has(color) && oldToNew.get(color) !== color) {
        next[key] = oldToNew.get(color);
        changed = true;
      }
    }
    return { changed, colorMap: next };
  };
  const auditColor = (color, context, unknowns) => {
    const normalized = normalizeHex(color);
    if (isIgnoredColor(normalized)) return;
    if (!isHex(normalized) || !allowedDuringMigration.has(normalized)) unknowns.push({ ...context, color: normalized });
  };

  const preflight = [];
  const allUnknowns = [];
  for (const item of config.managedFiles) {
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
    let imageInstances = 0;
    const changedFileIds = new Set();
    for (const element of scene.elements.filter((el) => el.type === "image")) {
      const entry = embedded[element.fileId];
      if (!entry) continue;
      for (const [field, value] of Object.entries(entry.colorMap || {})) {
        auditColor(value, { path: item.path, kind: "imageColorMap", id: element.id, fileId: element.fileId, image: entry.path, field }, allUnknowns);
      }
      if (mappedColorMap(entry.colorMap).changed) {
        imageInstances += 1;
        changedFileIds.add(element.fileId);
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
      imageMappings: changedFileIds.size,
      backgroundFrom: currentBackground,
      backgroundTo: expectedBackground,
      backgroundChanged: currentBackground !== expectedBackground,
      needsWrite: elementFields > 0 || imageInstances > 0 || currentBackground !== expectedBackground,
    });
  }

  if (config.strict !== false && allUnknowns.length) {
    const sample = allUnknowns.slice(0, 12).map((x) => `${x.path}: ${x.kind}.${x.field}=${x.color}`).join("\n");
    throw new Error(`Palette sync stopped: ${allUnknowns.length} non-palette color fields found.\n${sample}`);
  }

  const mode = options.apply ? "apply" : "check";
  const report = {
    schemaVersion: 1,
    mode,
    paletteCss: config.paletteCss,
    roleChanges,
    managedFiles: preflight.length,
    filesNeedingWrite: preflight.filter((x) => x.needsWrite).length,
    changesPending: roleChanges.length > 0 || preflight.some((x) => x.needsWrite),
    plannedElementFields: preflight.reduce((sum, x) => sum + x.elementFields, 0),
    plannedImageInstances: preflight.reduce((sum, x) => sum + x.imageInstances, 0),
    plannedBackgrounds: preflight.filter((x) => x.backgroundChanged).length,
    unknownColors: allUnknowns,
    files: preflight.map(({ file, text, knowledge, elementIds, ...x }) => x),
    applied: false,
    stateUpdated: false,
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

        const latestText = await app.vault.read(plan.file);
        const latestEmbedded = parseEmbeddedFiles(latestText);
        const live = view.excalidrawAPI.getSceneElements();
        const imageTargets = [];
        const imageMaps = [];
        for (const element of live.filter((el) => el.type === "image")) {
          const entry = latestEmbedded[element.fileId];
          if (!entry) continue;
          const mapped = mappedColorMap(entry.colorMap);
          if (mapped.changed) {
            imageTargets.push(element);
            imageMaps.push(mapped.colorMap);
          }
        }
        if (imageTargets.length) {
          await ea.updateViewSVGImageColorMap(imageTargets, imageMaps);
          await sleep(250);
        }
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
          for (const field of ["strokeColor", "backgroundColor"]) {
            const color = normalizeHex(element[field]);
            if (!isIgnoredColor(color) && (!isHex(color) || !allowedAfterApply.has(color))) {
              throw new Error(`Post-sync non-palette color: ${plan.path} ${element.id}.${field}=${color}`);
            }
          }
        }
        const afterEmbedded = parseEmbeddedFiles(afterText);
        for (const entry of Object.values(afterEmbedded)) {
          for (const [field, value] of Object.entries(entry.colorMap || {})) {
            const color = normalizeHex(value);
            if (!isIgnoredColor(color) && (!isHex(color) || !allowedAfterApply.has(color))) {
              throw new Error(`Post-sync image color: ${plan.path} ${entry.path}.${field}=${color}`);
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

    config.lastApplied = Object.fromEntries(roles.map((role) => [role, newPalette[role]]));
    config.lastAppliedAt = new Date().toISOString();
    fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`);
    report.applied = true;
    report.stateUpdated = true;
  }

  report.noOp = !report.changesPending;
  report.completedAt = new Date().toISOString();
  if (options.reportPath) fs.writeFileSync(options.reportPath, `${JSON.stringify(report, null, 2)}\n`);
  ea.clear();
  return JSON.stringify(report);
})()
