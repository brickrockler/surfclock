with open("shared_assets/unified_museum_ui.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update buildProvenanceMarkup to include Binomial Nomenclature (*Genus species*), Family, and Common Name for Plants / Shells, and "🗑️ Delete Specimen" button
old_prov_start = """    const rows = [];
    // 1. Physical Size
    rows.push(`<div class="mopt-curatorial-row"><span class="mopt-curatorial-label">Size</span><span class="mopt-curatorial-val">${w} &times; ${h} &times; ${d} cm</span></div>`);"""

new_prov_start = """    const rows = [];
    // 0. Botanical / Marine Shell Taxonomic Classification (Binomial Nomenclature, Family, Common Name)
    const taxInfo = (window.PhotoTo3DEngine && window.PhotoTo3DEngine.inferBotanicalOrShellTaxonomy)
      ? window.PhotoTo3DEngine.inferBotanicalOrShellTaxonomy(obj)
      : null;
    const binomial = obj.binomialNomenclature || (taxInfo && taxInfo.binomialNomenclature) || '';
    const botFamily = obj.botanicalFamily || (taxInfo && taxInfo.family) || '';
    const commonName = obj.commonName || (taxInfo && taxInfo.commonName) || '';
    if (binomial) {
      rows.push(`<div class="mopt-curatorial-row"><span class="mopt-curatorial-label">Binomial Nomenclature</span><span class="mopt-curatorial-val"><em>${escapeHtml(binomial)}</em></span></div>`);
    }
    if (botFamily) {
      rows.push(`<div class="mopt-curatorial-row"><span class="mopt-curatorial-label">Family</span><span class="mopt-curatorial-val">${escapeHtml(botFamily)}</span></div>`);
    }
    if (commonName) {
      rows.push(`<div class="mopt-curatorial-row"><span class="mopt-curatorial-label">Common Name</span><span class="mopt-curatorial-val">${escapeHtml(commonName)}</span></div>`);
    }

    // 1. Physical Size
    rows.push(`<div class="mopt-curatorial-row"><span class="mopt-curatorial-label">Size</span><span class="mopt-curatorial-val">${w} &times; ${h} &times; ${d} cm</span></div>`);"""

assert old_prov_start in code, "old_prov_start not found"
code = code.replace(old_prov_start, new_prov_start, 1)

old_del_btn = """    const deleteBtnHtml = obj && obj.id
      ? `<button type="button" class="mopt-prov-pill" id="mopt-placard-delete-custom-btn" data-custom-id="${escapeHtml(obj.id)}" style="background:rgba(180,35,24,0.12);color:#B42318;border-color:rgba(180,35,24,0.34);font-weight:700;cursor:pointer;">🗑️ Delete 3D Model from Library</button>`
      : '';"""

new_del_btn = """    const deleteBtnHtml = obj && obj.id
      ? `<button type="button" class="mopt-prov-pill" id="mopt-placard-delete-custom-btn" data-custom-id="${escapeHtml(obj.id)}" style="background:rgba(180,35,24,0.12);color:#B42318;border-color:rgba(180,35,24,0.34);font-weight:700;cursor:pointer;">🗑️ Delete Specimen</button>`
      : '';"""

assert old_del_btn in code, "old_del_btn not found"
code = code.replace(old_del_btn, new_del_btn, 1)

# 2. Replace #mopt-3d-recon-editor-box HTML & JS wiring with Option A / Option B / Option C + Sliders + 2D Mask Refinement Canvas (and NO Heat Map button!)
old_recon_html = """      <div class="mopt-3d-recon-editor-box" id="mopt-3d-recon-editor-box" style="margin:8px 0 10px;padding:10px 11px;border-radius:8px;background:rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.16);font-family:'Google Sans Code',monospace;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <span style="font-size:9.5px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">3D MODEL RECONSTRUCTION EDITOR</span>
          <span id="mopt-3d-tech-active-badge" style="font-size:9px;font-weight:700;color:#1D6F42;">● Hybrid 4-View + Depth</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:5px;">
          <button type="button" class="mopt-3d-tech-btn" data-tech="nanobanana_4view" style="text-align:left;padding:6px 9px;border-radius:6px;border:1px solid rgba(0,0,0,0.22);background:#FFFFFF;color:#111111;font-family:inherit;font-size:10px;font-weight:600;cursor:pointer;line-height:1.3;">
            🍌 Regenerate: Nano Banana 4-View Orthographic Turnaround
          </button>
          <div style="display:flex;gap:4px;">
            <button type="button" class="mopt-3d-tech-btn" data-tech="depth_heatmap" style="flex:1;text-align:left;padding:6px 9px;border-radius:6px;border:1px solid rgba(0,0,0,0.22);background:#FFFFFF;color:#111111;font-family:inherit;font-size:10px;font-weight:600;cursor:pointer;line-height:1.3;">
              🔥 Toggle: Depth / Heat Map 3D Version
            </button>
            <button type="button" id="mopt-3d-thermal-shader-btn" title="Toggle Thermal Depth Heat Map surface shader on the 3D object" style="padding:6px 8px;border-radius:6px;border:1px solid rgba(0,0,0,0.22);background:#FFFFFF;color:#111111;font-family:inherit;font-size:9.5px;font-weight:600;cursor:pointer;white-space:nowrap;">
              🌡️ Heat Map
            </button>
          </div>
          <button type="button" class="mopt-3d-tech-btn active" data-tech="hybrid_depth_4view" style="text-align:left;padding:6px 9px;border-radius:6px;border:1px solid #000000;background:#000000;color:#FFFFFF;font-family:inherit;font-size:10px;font-weight:700;cursor:pointer;line-height:1.3;">
            ⚡ Hybrid: 3D Depth Map + 4-View Nano Banana Turnaround
          </button>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:7px;">
          <div style="border:1px solid rgba(0,0,0,0.14);border-radius:5px;padding:3px;background:#E8E8E2;cursor:pointer;" id="mopt-placard-4view-wrap" title="Click to enlarge 4-View Orthographic Turnaround">
            <div style="font-size:8px;font-weight:700;color:#333;margin-bottom:2px;">4-VIEW TURNAROUND</div>
            <img id="mopt-placard-4view-thumb" src="" alt="4-View Orthographic Turnaround" style="width:100%;height:56px;object-fit:contain;display:block;" />
          </div>
          <div style="border:1px solid rgba(0,0,0,0.14);border-radius:5px;padding:3px;background:#161618;cursor:pointer;" id="mopt-placard-depth-wrap" title="Click to enlarge 3D Depth / Heat Map">
            <div style="font-size:8px;font-weight:700;color:#EAE6DF;margin-bottom:2px;">3D DEPTH / HEAT MAP</div>
            <img id="mopt-placard-depth-thumb" src="" alt="3D Depth / Heat Map" style="width:100%;height:56px;object-fit:contain;display:block;" />
          </div>
        </div>
        <div style="display:flex;gap:5px;margin-top:7px;">
          <button type="button" id="mopt-placard-update-gallery-3d-btn" style="flex:1;padding:7px 9px;border-radius:6px;border:none;background:#1D6F42;color:#FFFFFF;font-family:inherit;font-size:10px;font-weight:700;cursor:pointer;">
            ✓ Update Chosen 3D Model to My Gallery
          </button>
          <button type="button" id="mopt-placard-delete-library-btn" style="padding:7px 9px;border-radius:6px;border:1px solid rgba(180,35,24,0.38);background:rgba(180,35,24,0.10);color:#B42318;font-family:inherit;font-size:10px;font-weight:700;cursor:pointer;" title="Delete this 3D model from your library">
            🗑️ Delete
          </button>
        </div>
      </div>"""

new_recon_html = """      <div class="mopt-3d-recon-editor-box" id="mopt-3d-recon-editor-box" style="margin:8px 0 10px;padding:10px 11px;border-radius:0px;background:rgba(0,0,0,0.035);border:1px solid rgba(0,0,0,0.22);font-family:'Google Sans Code',monospace;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
          <span style="font-size:9.5px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">TRI-MODAL 3D RECONSTRUCTION ENGINE</span>
          <span id="mopt-3d-tech-active-badge" style="font-size:9px;font-weight:700;color:#1D6F42;">● Option C · Hybrid</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:5px;">
          <button type="button" class="mopt-3d-tech-btn" data-tech="nanobanana_4view" style="text-align:left;padding:6px 9px;border-radius:0px;border:1px solid rgba(0,0,0,0.28);background:#FFFFFF;color:#111111;font-family:inherit;font-size:9.8px;font-weight:600;cursor:pointer;line-height:1.3;">
            Option A · Restored Nano Banana 4-View Turnaround
          </button>
          <button type="button" class="mopt-3d-tech-btn" data-tech="depth_heatmap" style="text-align:left;padding:6px 9px;border-radius:0px;border:1px solid rgba(0,0,0,0.28);background:#FFFFFF;color:#111111;font-family:inherit;font-size:9.8px;font-weight:600;cursor:pointer;line-height:1.3;">
            Option B · Jack&#39;s MiDaS Neural Depth &amp; Watertight Manifold
          </button>
          <button type="button" class="mopt-3d-tech-btn active" data-tech="hybrid_depth_4view" style="text-align:left;padding:6px 9px;border-radius:0px;border:1px solid #000000;background:#000000;color:#FFFFFF;font-family:inherit;font-size:9.8px;font-weight:700;cursor:pointer;line-height:1.3;">
            Option C · Hybrid Profile Fusion &amp; Thin-Shell Relief
          </button>
        </div>

        <!-- Real-Time Parametric Adjustments: Inflation Depth & Shininess / Roughness -->
        <div style="margin-top:8px;padding:7px 8px;border:1px solid rgba(0,0,0,0.14);background:#F8F8F4;display:flex;flex-direction:column;gap:6px;">
          <div>
            <div style="display:flex;justify-content:space-between;font-size:8.8px;font-weight:700;color:#222;">
              <span>INFLATION DEPTH (DISPLACEMENT SCALE)</span>
              <span id="mopt-3d-inflation-val">1.00&times;</span>
            </div>
            <input type="range" id="mopt-3d-inflation-slider" min="0.15" max="2.20" step="0.05" value="1.00" style="width:100%;accent-color:#000;cursor:pointer;height:14px;" />
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;font-size:8.8px;font-weight:700;color:#222;">
              <span>SHININESS / ROUGHNESS</span>
              <span id="mopt-3d-roughness-val">0.38</span>
            </div>
            <input type="range" id="mopt-3d-roughness-slider" min="0.05" max="0.95" step="0.02" value="0.38" style="width:100%;accent-color:#000;cursor:pointer;height:14px;" />
          </div>
        </div>

        <!-- Interactive 2D Mask Refinement Canvas (Lasso, Brush, Eraser + Regenerate 3D Mesh) -->
        <details id="mopt-2d-mask-refiner-details" style="margin-top:7px;border:1px solid rgba(0,0,0,0.16);background:#FFFFFF;padding:6px 8px;">
          <summary style="font-size:9px;font-weight:700;letter-spacing:0.05em;cursor:pointer;user-select:none;display:flex;justify-content:space-between;align-items:center;">
            <span>✂️ 2D MASK REFINEMENT (LASSO · BRUSH · ERASER)</span>
            <span>&#9662;</span>
          </summary>
          <div style="margin-top:7px;display:flex;flex-direction:column;gap:6px;">
            <div style="display:flex;gap:4px;flex-wrap:wrap;">
              <button type="button" class="mopt-mask-tool-btn active" data-mask-tool="eraser" style="flex:1;padding:4px 6px;border:1px solid #000;background:#000;color:#FFF;font-family:inherit;font-size:8.8px;font-weight:700;cursor:pointer;">Eraser</button>
              <button type="button" class="mopt-mask-tool-btn" data-mask-tool="brush" style="flex:1;padding:4px 6px;border:1px solid rgba(0,0,0,0.3);background:#FFF;color:#000;font-family:inherit;font-size:8.8px;font-weight:600;cursor:pointer;">Brush</button>
              <button type="button" class="mopt-mask-tool-btn" data-mask-tool="lasso" style="flex:1;padding:4px 6px;border:1px solid rgba(0,0,0,0.3);background:#FFF;color:#000;font-family:inherit;font-size:8.8px;font-weight:600;cursor:pointer;">Lasso</button>
              <button type="button" id="mopt-mask-reset-btn" style="padding:4px 6px;border:1px solid rgba(0,0,0,0.3);background:#F4F4F0;color:#000;font-family:inherit;font-size:8.8px;cursor:pointer;">Reset</button>
            </div>
            <div style="display:flex;align-items:center;gap:6px;font-size:8.5px;">
              <span>Radius:</span>
              <input type="range" id="mopt-mask-brush-size" min="4" max="36" step="2" value="14" style="flex:1;accent-color:#000;" />
              <span id="mopt-mask-brush-val">14px</span>
            </div>
            <div style="position:relative;width:100%;height:190px;background:repeating-conic-gradient(#E5E5E0 0% 25%, #F8F8F4 0% 50%) 50% / 14px 14px;border:1px solid rgba(0,0,0,0.2);display:flex;align-items:center;justify-content:center;overflow:hidden;">
              <canvas id="mopt-2d-mask-canvas" width="220" height="220" style="width:186px;height:186px;cursor:crosshair;touch-action:none;"></canvas>
            </div>
            <button type="button" id="mopt-mask-regen-3d-btn" style="width:100%;padding:6px 8px;border:1px solid #000;background:#000;color:#FFF;font-family:inherit;font-size:9.5px;font-weight:700;cursor:pointer;">
              ↻ Regenerate 3D Mesh from Refined Mask
            </button>
          </div>
        </details>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:7px;">
          <div style="border:1px solid rgba(0,0,0,0.14);padding:3px;background:#F4F4F4;cursor:pointer;" id="mopt-placard-4view-wrap" title="Click to enlarge 4-View Orthographic Turnaround">
            <div style="font-size:8px;font-weight:700;color:#333;margin-bottom:2px;">4-VIEW TURNAROUND (#F4F4F4)</div>
            <img id="mopt-placard-4view-thumb" src="" alt="4-View Orthographic Turnaround" style="width:100%;height:56px;object-fit:contain;display:block;" />
          </div>
          <div style="border:1px solid rgba(0,0,0,0.14);padding:3px;background:#161618;cursor:pointer;" id="mopt-placard-depth-wrap" title="Click to enlarge MiDaS Neural Depth Map">
            <div style="font-size:8px;font-weight:700;color:#EAE6DF;margin-bottom:2px;">MIDAS NEURAL DEPTH</div>
            <img id="mopt-placard-depth-thumb" src="" alt="MiDaS Neural Depth Map" style="width:100%;height:56px;object-fit:contain;display:block;" />
          </div>
        </div>
        <div style="display:flex;gap:5px;margin-top:7px;">
          <button type="button" id="mopt-placard-update-gallery-3d-btn" style="flex:1;padding:7px 9px;border-radius:0px;border:none;background:#1D6F42;color:#FFFFFF;font-family:inherit;font-size:9.8px;font-weight:700;cursor:pointer;">
            ✓ Update Chosen 3D Model to My Gallery
          </button>
          <button type="button" id="mopt-placard-delete-library-btn" style="padding:7px 9px;border-radius:0px;border:1px solid rgba(180,35,24,0.45);background:rgba(180,35,24,0.10);color:#B42318;font-family:inherit;font-size:9.8px;font-weight:700;cursor:pointer;" title="Delete this 3D model from your library">
            🗑️ Delete 3D Model from Library
          </button>
        </div>
      </div>"""

assert old_recon_html in code, "old_recon_html not found"
code = code.replace(old_recon_html, new_recon_html, 1)

# 3. Replace JS wiring of #mopt-3d-recon-editor-box (lines 891-1002)
old_recon_js = """      // Wire 3D Model Reconstruction Technique Switcher & Gallery Updater (note_1791893273797_73bb)
      const reconBox = document.getElementById('mopt-3d-recon-editor-box');
      if (reconBox && window.PhotoTo3DEngine) {
        let chosenTech = obj.reconstructionTechnique || obj.analysis?.reconstructionTechnique || 'hybrid_depth_4view';
        let showThermal = Boolean(obj.analysis?.showThermalHeatmapOnMesh);
        const badgeEl = document.getElementById('mopt-3d-tech-active-badge');
        const thumb4View = document.getElementById('mopt-placard-4view-thumb');
        const thumbDepth = document.getElementById('mopt-placard-depth-thumb');
        const thermalBtn = document.getElementById('mopt-3d-thermal-shader-btn');
        const updateGalBtn = document.getElementById('mopt-placard-update-gallery-3d-btn');

        const techLabels = {
          nanobanana_4view: '🍌 Nano Banana 4-View',
          depth_heatmap: '🔥 3D Depth / Heat Map',
          hybrid_depth_4view: '⚡ Hybrid 4-View + Depth'
        };

        const syncTechUI = () => {
          if (badgeEl) badgeEl.textContent = '● ' + (techLabels[chosenTech] || 'Hybrid 4-View + Depth');
          reconBox.querySelectorAll('.mopt-3d-tech-btn').forEach(b => {
            const isAct = b.getAttribute('data-tech') === chosenTech;
            b.classList.toggle('active', isAct);
            b.style.background = isAct ? '#000000' : '#FFFFFF';
            b.style.color = isAct ? '#FFFFFF' : '#111111';
            b.style.borderColor = isAct ? '#000000' : 'rgba(0,0,0,0.22)';
            b.style.fontWeight = isAct ? '700' : '600';
          });
          if (thermalBtn) {
            thermalBtn.style.background = showThermal ? '#D4A359' : '#FFFFFF';
            thermalBtn.style.color = '#111111';
            thermalBtn.style.fontWeight = showThermal ? '700' : '600';
          }
        };
        syncTechUI();

        // Populate 4-View Turnaround & 3D Depth Heat Map thumbnails asynchronously
        window.PhotoTo3DEngine.ensureObjectAnalysis(obj).then(an => {
          if (window.CURRENT_SELECTED_OBJECT !== obj) return;
          const vUrl = (an && an.turnaroundSheetDataUrl) || obj.turnaroundSheetDataUrl || obj.nanoBananaViews || obj.cutoutPhoto || obj.sourcePhoto || '';
          const dUrl = (an && an.depthHeatmapDataUrl) || (an && an.depthDataUrl) || obj.cutoutPhoto || '';
          if (thumb4View && vUrl) thumb4View.src = vUrl;
          if (thumbDepth && dUrl) thumbDepth.src = dUrl;
        }).catch(() => {});

        document.getElementById('mopt-placard-4view-wrap').onclick = () => {
          if (thumb4View && thumb4View.src) openSourcePhotoLightbox(thumb4View.src, `${obj.title} · Nano Banana 4-View Orthographic Turnaround`);
        };
        document.getElementById('mopt-placard-depth-wrap').onclick = () => {
          if (thumbDepth && thumbDepth.src) openSourcePhotoLightbox(thumbDepth.src, `${obj.title} · 3D Depth / Heat Map`);
        };

        const previewTechniqueLive = async (tech, forceRegen = false) => {
          chosenTech = tech;
          syncTechUI();
          if (badgeEl) badgeEl.textContent = '⏳ Rebuilding 3D Model...';
          try {
            await window.PhotoTo3DEngine.ensureObjectAnalysis(obj, { forceRegenerate: forceRegen });
            if (obj.analysis) {
              obj.analysis.reconstructionTechnique = chosenTech;
              obj.analysis.showThermalHeatmapOnMesh = showThermal;
              if (thumb4View && obj.analysis.turnaroundSheetDataUrl) thumb4View.src = obj.analysis.turnaroundSheetDataUrl;
              if (thumbDepth && obj.analysis.depthHeatmapDataUrl) thumbDepth.src = obj.analysis.depthHeatmapDataUrl;
            }
            obj.reconstructionTechnique = chosenTech;
            obj.isCustomReconstructed = true;
            obj.modelGlb = '__procedural__';
            obj.glbFile = '__procedural__';
            // Immediately hot-swap in active gallery / Portal turntable
            window.dispatchEvent(new CustomEvent('museum-custom-object-updated', {
              detail: { object: obj, technique: chosenTech, previewOnly: true }
            }));
            syncTechUI();
          } catch (e) {
            syncTechUI();
          }
        };

        reconBox.querySelectorAll('.mopt-3d-tech-btn').forEach(btn => {
          btn.onclick = (ev) => {
            ev.stopPropagation();
            const t = btn.getAttribute('data-tech') || 'hybrid_depth_4view';
            if (t !== 'depth_heatmap') showThermal = false;
            previewTechniqueLive(t, t === 'nanobanana_4view');
          };
        });

        if (thermalBtn) {
          thermalBtn.onclick = (ev) => {
            ev.stopPropagation();
            showThermal = !showThermal;
            if (showThermal) chosenTech = 'depth_heatmap';
            previewTechniqueLive(chosenTech, false);
          };
        }

        if (updateGalBtn) {
          updateGalBtn.onclick = async (ev) => {
            ev.stopPropagation();
            const origText = updateGalBtn.textContent;
            updateGalBtn.textContent = '⏳ Updating Gallery...';
            saveInfoOverrideForObject(obj.id, {
              reconstructionTechnique: chosenTech,
              reconstructionMode: (chosenTech === 'nanobanana_4view' || chosenTech === 'hybrid_depth_4view' || chosenTech === 'depth_heatmap') && obj.reconstructionMode === 'vessel'
                ? 'sculpture'
                : (obj.reconstructionMode || 'sculpture')
            });
            await window.PhotoTo3DEngine.applyTechniqueToGalleryObject(obj, chosenTech, { showThermalHeatmap: showThermal });
            updateGalBtn.textContent = '✓ Updated to My Gallery!';
            setTimeout(() => { updateGalBtn.textContent = origText; }, 1800);
          };
        }
      }"""

new_recon_js = """      // Wire Tri-Modal 3D Reconstruction Engine (Options A/B/C), Parametric Sliders & 2D Mask Refinement (chat_msg_1791899437312_imyi)
      const reconBox = document.getElementById('mopt-3d-recon-editor-box');
      if (reconBox && window.PhotoTo3DEngine) {
        const taxDefault = window.PhotoTo3DEngine.inferBotanicalOrShellTaxonomy ? window.PhotoTo3DEngine.inferBotanicalOrShellTaxonomy(obj) : null;
        let chosenTech = obj.reconstructionTechnique || obj.analysis?.reconstructionTechnique || (taxDefault ? taxDefault.defaultTechnique : 'hybrid_depth_4view');
        const badgeEl = document.getElementById('mopt-3d-tech-active-badge');
        const thumb4View = document.getElementById('mopt-placard-4view-thumb');
        const thumbDepth = document.getElementById('mopt-placard-depth-thumb');
        const updateGalBtn = document.getElementById('mopt-placard-update-gallery-3d-btn');
        const infSlider = document.getElementById('mopt-3d-inflation-slider');
        const infValEl = document.getElementById('mopt-3d-inflation-val');
        const roughSlider = document.getElementById('mopt-3d-roughness-slider');
        const roughValEl = document.getElementById('mopt-3d-roughness-val');

        const curInf = typeof obj.inflationDepthScale === 'number' ? obj.inflationDepthScale : (typeof obj.analysis?.inflationDepthScale === 'number' ? obj.analysis.inflationDepthScale : 1.0);
        const curRough = typeof obj.roughnessOverride === 'number' ? obj.roughnessOverride : (typeof obj.analysis?.roughnessOverride === 'number' ? obj.analysis.roughnessOverride : 0.38);
        if (infSlider) infSlider.value = String(curInf);
        if (infValEl) infValEl.textContent = `${Number(curInf).toFixed(2)}×`;
        if (roughSlider) roughSlider.value = String(curRough);
        if (roughValEl) roughValEl.textContent = Number(curRough).toFixed(2);

        const techLabels = {
          nanobanana_4view: 'Option A · 4-View Turnaround',
          depth_heatmap: 'Option B · MiDaS Neural Depth',
          hybrid_depth_4view: 'Option C · Hybrid & Thin-Shell'
        };

        const syncTechUI = () => {
          if (badgeEl) badgeEl.textContent = '● ' + (techLabels[chosenTech] || 'Option C · Hybrid & Thin-Shell');
          reconBox.querySelectorAll('.mopt-3d-tech-btn').forEach(b => {
            const isAct = b.getAttribute('data-tech') === chosenTech;
            b.classList.toggle('active', isAct);
            b.style.background = isAct ? '#000000' : '#FFFFFF';
            b.style.color = isAct ? '#FFFFFF' : '#111111';
            b.style.borderColor = isAct ? '#000000' : 'rgba(0,0,0,0.28)';
            b.style.fontWeight = isAct ? '700' : '600';
          });
        };
        syncTechUI();

        // Setup 2D Mask Refinement Canvas (Lasso, Brush, Eraser)
        const maskCanvas = document.getElementById('mopt-2d-mask-canvas');
        const maskCtx = maskCanvas ? maskCanvas.getContext('2d', { willReadFrequently: true }) : null;
        let origCutoutImg = null;
        let activeMaskTool = 'eraser';
        let brushRadius = 14;
        let isDrawingMask = false;
        let lassoPts = [];

        const drawMaskSourceToCanvas = (srcUrl) => {
          if (!maskCanvas || !maskCtx || !srcUrl) return;
          const im = new Image();
          im.crossOrigin = 'anonymous';
          im.onload = () => {
            origCutoutImg = im;
            maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
            maskCtx.drawImage(im, 0, 0, maskCanvas.width, maskCanvas.height);
          };
          im.src = srcUrl;
        };

        window.PhotoTo3DEngine.ensureObjectAnalysis(obj).then(an => {
          if (window.CURRENT_SELECTED_OBJECT !== obj) return;
          const vUrl = (an && an.turnaroundSheetDataUrl) || obj.turnaroundSheetDataUrl || obj.nanoBananaViews || obj.cutoutPhoto || obj.sourcePhoto || '';
          const dUrl = (an && an.depthHeatmapDataUrl) || (an && an.depthDataUrl) || obj.cutoutPhoto || '';
          if (thumb4View && vUrl) thumb4View.src = vUrl;
          if (thumbDepth && dUrl) thumbDepth.src = dUrl;
          drawMaskSourceToCanvas((an && an.cutoutDataUrl) || obj.cutoutPhoto || obj.sourcePhoto || '');
        }).catch(() => {});

        reconBox.querySelectorAll('.mopt-mask-tool-btn').forEach(tb => {
          tb.onclick = (ev) => {
            ev.stopPropagation();
            activeMaskTool = tb.getAttribute('data-mask-tool') || 'eraser';
            reconBox.querySelectorAll('.mopt-mask-tool-btn').forEach(b => {
              const act = b.getAttribute('data-mask-tool') === activeMaskTool;
              b.classList.toggle('active', act);
              b.style.background = act ? '#000' : '#FFF';
              b.style.color = act ? '#FFF' : '#000';
              b.style.fontWeight = act ? '700' : '600';
            });
          };
        });

        const brushSizeIn = document.getElementById('mopt-mask-brush-size');
        const brushSizeVal = document.getElementById('mopt-mask-brush-val');
        if (brushSizeIn) {
          brushSizeIn.oninput = () => {
            brushRadius = Number(brushSizeIn.value) || 14;
            if (brushSizeVal) brushSizeVal.textContent = `${brushRadius}px`;
          };
        }

        const resetMaskBtn = document.getElementById('mopt-mask-reset-btn');
        if (resetMaskBtn) {
          resetMaskBtn.onclick = (ev) => {
            ev.stopPropagation();
            if (origCutoutImg && maskCtx) {
              maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
              maskCtx.drawImage(origCutoutImg, 0, 0, maskCanvas.width, maskCanvas.height);
            }
          };
        }

        if (maskCanvas && maskCtx) {
          const getCanvasPt = (e) => {
            const r = maskCanvas.getBoundingClientRect();
            return {
              x: ((e.clientX - r.left) / Math.max(1, r.width)) * maskCanvas.width,
              y: ((e.clientY - r.top) / Math.max(1, r.height)) * maskCanvas.height
            };
          };
          const applyBrushOrEraserAt = (pt) => {
            maskCtx.save();
            if (activeMaskTool === 'eraser') {
              maskCtx.globalCompositeOperation = 'destination-out';
              maskCtx.beginPath();
              maskCtx.arc(pt.x, pt.y, brushRadius, 0, Math.PI * 2);
              maskCtx.fill();
            } else if (activeMaskTool === 'brush' && origCutoutImg) {
              maskCtx.globalCompositeOperation = 'source-over';
              maskCtx.beginPath();
              maskCtx.arc(pt.x, pt.y, brushRadius, 0, Math.PI * 2);
              maskCtx.clip();
              maskCtx.drawImage(origCutoutImg, 0, 0, maskCanvas.width, maskCanvas.height);
            }
            maskCtx.restore();
          };
          maskCanvas.onpointerdown = (e) => {
            e.stopPropagation();
            isDrawingMask = true;
            maskCanvas.setPointerCapture(e.pointerId);
            const pt = getCanvasPt(e);
            if (activeMaskTool === 'lasso') {
              lassoPts = [pt];
            } else {
              applyBrushOrEraserAt(pt);
            }
          };
          maskCanvas.onpointermove = (e) => {
            if (!isDrawingMask) return;
            e.stopPropagation();
            const pt = getCanvasPt(e);
            if (activeMaskTool === 'lasso') {
              lassoPts.push(pt);
              maskCtx.save();
              maskCtx.strokeStyle = '#D4A359';
              maskCtx.lineWidth = 1.5;
              const prev = lassoPts[lassoPts.length - 2] || pt;
              maskCtx.beginPath();
              maskCtx.moveTo(prev.x, prev.y);
              maskCtx.lineTo(pt.x, pt.y);
              maskCtx.stroke();
              maskCtx.restore();
            } else {
              applyBrushOrEraserAt(pt);
            }
          };
          maskCanvas.onpointerup = (e) => {
            if (!isDrawingMask) return;
            isDrawingMask = false;
            if (activeMaskTool === 'lasso' && lassoPts.length >= 3 && origCutoutImg) {
              // Keep strictly inside the closed lasso polygon from origCutoutImg
              const tmp = document.createElement('canvas');
              tmp.width = maskCanvas.width;
              tmp.height = maskCanvas.height;
              const tCtx = tmp.getContext('2d');
              tCtx.drawImage(origCutoutImg, 0, 0, tmp.width, tmp.height);
              maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
              maskCtx.save();
              maskCtx.beginPath();
              maskCtx.moveTo(lassoPts[0].x, lassoPts[0].y);
              for (let i = 1; i < lassoPts.length; i++) maskCtx.lineTo(lassoPts[i].x, lassoPts[i].y);
              maskCtx.closePath();
              maskCtx.clip();
              maskCtx.drawImage(tmp, 0, 0);
              maskCtx.restore();
              lassoPts = [];
            }
          };
        }

        document.getElementById('mopt-placard-4view-wrap').onclick = () => {
          if (thumb4View && thumb4View.src) openSourcePhotoLightbox(thumb4View.src, `${obj.title} · Nano Banana 4-View Orthographic Turnaround`);
        };
        document.getElementById('mopt-placard-depth-wrap').onclick = () => {
          if (thumbDepth && thumbDepth.src) openSourcePhotoLightbox(thumbDepth.src, `${obj.title} · MiDaS Neural Depth Map`);
        };

        const previewTechniqueLive = async (tech, forceRegen = false) => {
          chosenTech = tech;
          syncTechUI();
          if (badgeEl) badgeEl.textContent = '⏳ Rebuilding 3D Model...';
          try {
            await window.PhotoTo3DEngine.ensureObjectAnalysis(obj, { forceRegenerate: forceRegen });
            const infScale = infSlider ? ( parseFloat(infSlider.value) || 1.0 ) : 1.0;
            const roughOvr = roughSlider ? ( parseFloat(roughSlider.value) || 0.38 ) : 0.38;
            if (obj.analysis) {
              obj.analysis.reconstructionTechnique = chosenTech;
              obj.analysis.showThermalHeatmapOnMesh = false;
              obj.analysis.inflationDepthScale = infScale;
              obj.analysis.roughnessOverride = roughOvr;
              if (thumb4View && obj.analysis.turnaroundSheetDataUrl) thumb4View.src = obj.analysis.turnaroundSheetDataUrl;
              if (thumbDepth && obj.analysis.depthHeatmapDataUrl) thumbDepth.src = obj.analysis.depthHeatmapDataUrl;
            }
            obj.reconstructionTechnique = chosenTech;
            obj.inflationDepthScale = infScale;
            obj.roughnessOverride = roughOvr;
            obj.isCustomReconstructed = true;
            obj.modelGlb = '__procedural__';
            obj.glbFile = '__procedural__';
            window.dispatchEvent(new CustomEvent('museum-custom-object-updated', {
              detail: { object: obj, technique: chosenTech, previewOnly: true }
            }));
            syncTechUI();
          } catch (e) {
            syncTechUI();
          }
        };

        reconBox.querySelectorAll('.mopt-3d-tech-btn').forEach(btn => {
          btn.onclick = (ev) => {
            ev.stopPropagation();
            const t = btn.getAttribute('data-tech') || 'hybrid_depth_4view';
            previewTechniqueLive(t, t === 'nanobanana_4view');
          };
        });

        let paramDebounce = null;
        const onParamSliderChange = () => {
          if (infValEl && infSlider) infValEl.textContent = `${Number(infSlider.value).toFixed(2)}×`;
          if (roughValEl && roughSlider) roughValEl.textContent = Number(roughSlider.value).toFixed(2);
          clearTimeout(paramDebounce);
          paramDebounce = setTimeout(() => {
            previewTechniqueLive(chosenTech, false);
          }, 90);
        };
        if (infSlider) infSlider.oninput = onParamSliderChange;
        if (roughSlider) roughSlider.oninput = onParamSliderChange;

        const regenMaskBtn = document.getElementById('mopt-mask-regen-3d-btn');
        if (regenMaskBtn && maskCanvas) {
          regenMaskBtn.onclick = async (ev) => {
            ev.stopPropagation();
            regenMaskBtn.textContent = '⏳ Regenerating 3D Mesh...';
            await window.PhotoTo3DEngine.ensureObjectAnalysis(obj, { forceRegenerate: false });
            if (obj.analysis && window.PhotoTo3DEngine.applyRefinedMaskCanvasToAnalysis) {
              window.PhotoTo3DEngine.applyRefinedMaskCanvasToAnalysis(obj.analysis, maskCanvas);
              obj.cutoutPhoto = obj.analysis.cutoutDataUrl;
            }
            await previewTechniqueLive(chosenTech, false);
            regenMaskBtn.textContent = '✓ 3D Mesh Regenerated!';
            setTimeout(() => { regenMaskBtn.textContent = '↻ Regenerate 3D Mesh from Refined Mask'; }, 1400);
          };
        }

        if (updateGalBtn) {
          updateGalBtn.onclick = async (ev) => {
            ev.stopPropagation();
            const origText = updateGalBtn.textContent;
            updateGalBtn.textContent = '⏳ Updating Gallery...';
            const infScale = infSlider ? (parseFloat(infSlider.value) || 1.0) : 1.0;
            const roughOvr = roughSlider ? (parseFloat(roughSlider.value) || 0.38) : 0.38;
            saveInfoOverrideForObject(obj.id, {
              reconstructionTechnique: chosenTech,
              inflationDepthScale: infScale,
              roughnessOverride: roughOvr,
              reconstructionMode: (chosenTech === 'nanobanana_4view' || chosenTech === 'hybrid_depth_4view' || chosenTech === 'depth_heatmap') && obj.reconstructionMode === 'vessel'
                ? 'sculpture'
                : (obj.reconstructionMode || 'sculpture')
            });
            await window.PhotoTo3DEngine.applyTechniqueToGalleryObject(obj, chosenTech, {
              showThermalHeatmap: false,
              inflationDepthScale: infScale,
              roughnessOverride: roughOvr
            });
            updateGalBtn.textContent = '✓ Updated to My Gallery!';
            setTimeout(() => { updateGalBtn.textContent = origText; }, 1800);
          };
        }
      }"""

assert old_recon_js in code, "old_recon_js not found"
code = code.replace(old_recon_js, new_recon_js, 1)

# 4. Update #mopt-top-type-select options to add "Plants" and rename "Rocks" -> "Rocks and shells"
old_type_opts = """          <select id="mopt-top-type-select" class="mopt-top-sort-select" aria-label="Filter by Object Type">
            <option value="all">All Types</option>
            <option value="ceramic">Ceramics</option>
            <option value="sculpture">Sculptures</option>
            <option value="book">Books</option>
            <option value="lamp">Lamps</option>
            <option value="rock">Rocks</option>
            <option value="painting">Paintings</option>
            <option value="cutout">Cutouts</option>
          </select>"""

new_type_opts = """          <select id="mopt-top-type-select" class="mopt-top-sort-select" aria-label="Filter by Object Type">
            <option value="all">All Types</option>
            <option value="ceramic">Ceramics</option>
            <option value="sculpture">Sculptures</option>
            <option value="plant">Plants</option>
            <option value="rock">Rocks and shells</option>
            <option value="book">Books</option>
            <option value="lamp">Lamps</option>
            <option value="painting">Paintings</option>
            <option value="cutout">Cutouts</option>
          </select>"""

assert old_type_opts in code, "old_type_opts not found"
code = code.replace(old_type_opts, new_type_opts, 1)

# 5. Update applyPortalMosaicArchiveFilterAndSort to match 'plant' and 'rock' ("Rocks and shells") accurately
old_mosaic_match = """          let matchCat = (cat === 'all') || cCat.includes(cat) || cKind.includes(cat);
          if (cat === 'cutout' && cKind.includes('wall_cutout')) matchCat = true;"""

new_mosaic_match = """          const cTitle = (cell.textContent || '').toLowerCase();
          let matchCat = (cat === 'all') || cCat.includes(cat) || cKind.includes(cat);
          if (cat === 'cutout' && cKind.includes('wall_cutout')) matchCat = true;
          if (cat === 'plant' && /plant|botan|flower|blossom|petal|leaf|monstera|ficus|orchid|fern|tree|flora|poppy/i.test(cCat + ' ' + cTitle)) matchCat = true;
          if (cat === 'rock' && /rock|stone|shell|bivalve|scallop|conch|nautilus|mineral|pebble|basalt|travertine|coral|fossil/i.test(cCat + ' ' + cTitle)) matchCat = true;"""

assert old_mosaic_match in code, "old_mosaic_match not found"
code = code.replace(old_mosaic_match, new_mosaic_match, 1)

# 6. Keep #mopt-bottom-archiving-toolbar visible across ALL pages (including Portal) per note_1791900165764_3d6z!
old_portal_hide = """      if (isPortal && bottomArchivingBar) {
        bottomArchivingBar.style.display = 'none';
      }"""

new_portal_hide = """      // Note note_1791900165764_3d6z: Keep Swiss architectural footer bar visible across all pages (including Portal)"""

assert old_portal_hide in code, "old_portal_hide not found"
code = code.replace(old_portal_hide, new_portal_hide, 1)

with open("shared_assets/unified_museum_ui.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully patched shared_assets/unified_museum_ui.js!")
