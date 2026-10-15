/**
 * ============================================================================
 * SURF CLOCK — 3D STUDIO CUSTOMIZER CONTROLLER
 * Clean NikeID-style UX + Real-Time 3D Customizer + Google Maps-Style Autocomplete
 * + Interactive Explode Slider + Live 3D Z-Space Oceanographic Wave Telemetry
 * ============================================================================
 */

import { COMPONENT_SWATCHES, CURATED_EDITIONS } from "./materials_and_presets.js?v=66";
import {
  DIAL_SLOTS,
  CURATED_REGIONS,
  ALL_KNOWN_REGIONS,
  formatDialBeachName,
  resolve5BestLocalBeaches,
  fetchLiveMarineTelemetry,
  searchLocationsAutocomplete,
} from "./surf_data.js?v=66";
import { SurfClockStudio3D } from "./studio_3d.js?v=66";
import {
  downloadFullStackCustomKit,
  buildClockwiseSpots,
  customizeWorkerJs,
  generateBuildGuideMarkdown,
} from "./package_generator.js?v=66";

const PART_LABELS = {
  bezel: "Frame",
  dial: "Dial",
  inlay: "Text",
  hands: "Hands",
  deck: "Core",
};

const EDITION_ACCENT_HEX = {
  "gallery-alabaster": "#FF4F00",
  "braun-dn40": "#FF4F00",
  "eucalyptus-sage": "#5E7153",
  "klein-cobalt": "#0D38C4",
  "signal-1972": "#EB3900",
  "obsidian-gold": "#C59B38",
  "skeleton-frost": "#0284C7",
  "smoked-amber": "#DF852C",
};

class SurfClockConfiguratorApp {
  constructor() {
    const defaultRegion = CURATED_REGIONS[0];
    const defaultEdition = CURATED_EDITIONS[0];

    this.state = {
      activeRegion: { ...defaultRegion },
      beaches: defaultRegion.beaches.map((b) => ({ ...b })),
      selectedBeachIndex: defaultRegion.activeSlot ?? 2,
      bestBeachIndex: defaultRegion.activeSlot ?? 2,
      conditionsRating: defaultRegion.worthItScore ?? 8.2,
      activeSwellHeightM: defaultRegion.swellHeightM ?? 1.9,
      activeSwellPeriodS: defaultRegion.swellPeriodS ?? 13,
      activeSwellDir: defaultRegion.swellDir || "SSE",
      subdialMode: defaultEdition.subdialMode || "worth_it",
      liveMarineData: null,

      activePart: "bezel",
      activeEditionId: defaultEdition.id,
      colors: {
        bezel: defaultEdition.bezel,
        dial: defaultEdition.dial,
        inlay: defaultEdition.inlay,
        hands: defaultEdition.hands,
        deck: defaultEdition.deck,
      },

      lightingMode: "daylight",
      cameraView: "front",
      explodeFactor: 0,
      liveDemoRunning: false,
      mobileDrawerOpen: false,
      mobileDrawerTab: "beaches",

      autocompleteItems: [],
      autocompleteIndex: -1,
    };

    this.demoTimer = null;
    this.searchDebounce = null;
    this.toastTimeout = null;
    this.loadingTimeout = null;
    this._acSeq = 0;
    this._regionSeq = 0;
    this._lastFocusedBeforeModal = null;

    if (window.innerWidth === 500 && window.innerHeight === 844) {
      document.documentElement.classList.add("mobile-390-preview");
      document.body.classList.add("mobile-390-preview");
    }
    this._init();
  }

  _init() {
    this._initDOMRefs();
    this._recomputeActiveBeachConditions();
    this._init3DEngine();
    this._renderRegionPills();
    this._renderBeachesList();
    this._renderPresetChips();
    this._renderSwatchGrid();
    this._updateAllLabels();
    this._bindEvents();
    this._startHudWaveLoop();
    this._applyDemoQueryHooks();
    this._fetchLiveWaveTelemetry(
      this.state.activeRegion.lat,
      this.state.activeRegion.lng ?? this.state.activeRegion.lon
    );
  }

  getActiveSwellMetrics() {
    const reg = this.state.activeRegion || {};
    const beaches = this.state.beaches || [];
    const idx = this.state.selectedBeachIndex ?? 0;
    const beach = beaches[idx] || {};

    let bestBeach = beaches[0] || {};
    let maxQ = -1;
    beaches.forEach((b) => {
      const q = typeof b.quality === "number" ? b.quality : 7.5;
      if (q > maxQ) {
        maxQ = q;
        bestBeach = b;
      }
    });

    const beachQ = typeof beach.quality === "number" ? beach.quality : 7.5;
    const bestQ = typeof bestBeach.quality === "number" ? bestBeach.quality : 7.5;
    const qDelta = beachQ - bestQ;

    const exposureFactors = [1.0, 0.90, 0.96, 0.84, 0.92];
    const exp = exposureFactors[idx % 5] || 1.0;

    // Resolve per-beach directional swell so every beach & region drives true 3D wave direction
    const COMPASS_16 = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
    const slotDirShift = [0, 3, -3, 5, -5];
    const resolveBeachDir = (fallbackDir) => {
      if (beach.swellDir) return beach.swellDir;
      const cleanBase = String(fallbackDir || reg.swellDir || "WNW").trim().toUpperCase();
      const bIdx = COMPASS_16.indexOf(cleanBase);
      if (bIdx >= 0) {
        return COMPASS_16[(bIdx + (slotDirShift[idx % 5] || 0) + 16) % 16];
      }
      return cleanBase;
    };

    if (this.state.liveMarineData) {
      const live = this.state.liveMarineData;
      const baseScore = typeof live.worthItScore === "number" ? live.worthItScore : (reg.worthItScore ?? bestQ);
      const modulatedScore = Math.max(1.0, Math.min(10.0, Number((baseScore + qDelta * 0.85).toFixed(1))));
      const baseHeight = live.swellHeightM ?? reg.swellHeightM ?? 1.9;
      const heightMod = Math.max(0.72, Math.min(1.15, exp * (1.0 + qDelta * 0.045)));
      const heightM = Number(Math.max(0.4, baseHeight * heightMod).toFixed(1));
      const periodS = Math.round(live.swellPeriodS ?? reg.swellPeriodS ?? 13);
      const dir = resolveBeachDir(live.swellDir || reg.swellDir || "WNW");
      return {
        worthItScore: modulatedScore,
        heightM,
        periodS,
        dir,
      };
    }

    const rating = typeof beach.quality === "number" ? beach.quality : (reg.worthItScore ?? 8.2);
    const baseHeight = reg.swellHeightM ?? 1.9;
    const qualityMod = 0.85 + (rating / 10) * 0.22;
    const heightM = Number(Math.max(0.4, baseHeight * exp * qualityMod).toFixed(1));
    const periodS = Math.round(reg.swellPeriodS ?? 13);
    const dir = resolveBeachDir(reg.swellDir || "WNW");

    return {
      worthItScore: rating,
      heightM,
      periodS,
      dir,
    };
  }

  _recomputeActiveBeachConditions() {
    const metrics = this.getActiveSwellMetrics();
    this.state.conditionsRating = metrics.worthItScore;
    this.state.activeSwellHeightM = metrics.heightM;
    this.state.activeSwellPeriodS = metrics.periodS;
    this.state.activeSwellDir = metrics.dir;
  }

  _fetchLiveWaveTelemetry(lat, lon) {
    if (lat == null || lon == null) return;
    const seq = this._regionSeq;
    fetchLiveMarineTelemetry(lat, lon).then((live) => {
      if (live && seq === this._regionSeq) {
        const reg = this.state.activeRegion || {};
        if (reg.isIconicGlobal) {
          // Preserve big-wave drama & curated directional variety on the 8 iconic global surf spots
          live.swellHeightM = Number(Math.max((reg.swellHeightM || 2.8) * 0.88, live.swellHeightM || 0).toFixed(1));
          live.swellPeriodS = Math.max((reg.swellPeriodS || 15) - 2, live.swellPeriodS || 12);
          live.swellDir = reg.swellDir || live.swellDir;
          live.worthItScore = Number(Math.max((reg.worthItScore || 9.5) * 0.94, live.worthItScore || 8.5).toFixed(1));
        }
        this.state.liveMarineData = live;
        this.state.activeRegion.swellHeightM = live.swellHeightM;
        this.state.activeRegion.swellPeriodS = live.swellPeriodS;
        this.state.activeRegion.swellDir = live.swellDir;
        if (typeof live.worthItScore === "number") {
          this.state.activeRegion.worthItScore = live.worthItScore;
        }
        this._recomputeActiveBeachConditions();
        this._syncSubdialNeedle();
        this._syncTelemetryToStudio();
        this._updateAllLabels();
        if (this._drawStaticHudWave) this._drawStaticHudWave();
      }
    });
  }

  _applyDemoQueryHooks() {
    const params = new URLSearchParams(window.location.search);
    const demo = params.get("demo");
    if (!demo) return;
    if (demo === "mobile" || demo === "mobile_drawer") {
      document.documentElement.classList.add("mobile-390-preview");
      document.body.classList.add("mobile-390-preview");
      if (demo === "mobile_drawer") {
        this.setMobileDrawerOpen(true, "colors");
      }
      setTimeout(() => {
        if (this.studio) {
          this.studio.resize();
          this.studio.setCameraPreset("front", true);
          this.studio?.setMobileDrawerOffset?.(this.state.mobileDrawerOpen, 0.52);
        }
      }, 50);
    } else if (demo === "kiama") {
      const kiamaReg = ALL_KNOWN_REGIONS.find((r) => r.id === "kiama-south-coast");
      if (kiamaReg) {
        this.dom.searchInput.value = kiamaReg.name;
        this.selectRegionPreset(kiamaReg, true);
      }
    } else if (demo === "search") {
      this.dom.searchInput.value = "Kiama";
      this._updateAutocompleteSuggestions("Kiama");
    } else if (demo === "loading") {
      this.showLoadingOverlay("Loading 5 Best Beaches...", "Analyzing coast geometry & live Open-Meteo swell for Byron Bay, NSW");
    } else if (demo === "explode") {
      if (this.dom.sliderExplode) {
        this.dom.sliderExplode.value = "0.95";
      }
      this.state.explodeFactor = 0.95;
      this._setCameraViewState("exploded");
      this.studio.setCameraPreset("exploded", true);
      this.studio.setExplodeFactor(0.95, true);
    } else if (demo === "night" || demo === "slate") {
      if (demo === "slate") {
        const ed = CURATED_EDITIONS[1];
        if (ed) this.applyEdition(ed);
      }
      this.setLightingMode("nightlight");
    } else if (demo === "surprise") {
      const ed = CURATED_EDITIONS.find((e) => e.id === "klein-cobalt") || CURATED_EDITIONS[3];
      if (ed) this.applyEdition(ed);
    } else if (demo === "subdial") {
      this._setCameraViewState("subdial");
      if (this.dom.swellScaleDatum) this.dom.swellScaleDatum.classList.add("macro-hidden");
      this.studio.setCameraPreset("subdial", true);
    } else if (demo === "macro") {
      this._setCameraViewState("macro");
      if (this.dom.swellScaleDatum) this.dom.swellScaleDatum.classList.add("macro-hidden");
      this.studio.setCameraPreset("macro", true);
    }
  }

  _setCameraViewState(view) {
    this.state.cameraView = view;
    document.body.dataset.cam = view;
    this.dom.camBtns.forEach((b) => {
      const isActive = b.dataset.cam === view;
      b.classList.toggle("active", isActive);
      b.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  _initDOMRefs() {
    const autocompleteEl = document.getElementById("search-autocomplete-dropdown");
    this.dom = {
      viewportStage: document.getElementById("viewport-stage"),
      studioCanvas: document.getElementById("studio-canvas"),

      brandEasterEgg: document.getElementById("brand-easter-egg"),

      hudWaveCanvas: document.getElementById("hud-wave-canvas"),
      hudRegionTitle: document.getElementById("hud-region-title"),
      hudSwellSummary: document.getElementById("hud-swell-summary"),
      hudSwellHeroCard: document.getElementById("hud-swell-hero-card"),
      hudSwellSize: document.getElementById("hud-swell-size"),
      hudSwellFeet: document.getElementById("hud-swell-feet"),
      hudSwellPeriod: document.getElementById("hud-swell-period"),
      stageStatusPill: document.getElementById("stage-status-pill"),
      btnMobileSearchTrigger: document.getElementById("btn-mobile-search-trigger"),
      swellScaleDatum: document.getElementById("swell-scale-datum"),
      datumCaliperLine: document.getElementById("datum-caliper-line"),
      datumSwellVal: document.getElementById("datum-swell-val"),
      datumSwellSub: document.getElementById("datum-swell-sub"),
      customizerPanel: document.getElementById("customizer-panel"),
      mobileDrawerBar: document.getElementById("mobile-drawer-bar"),
      btnMobileDrawerToggle: document.getElementById("btn-mobile-drawer-toggle"),
      btnMobileDrawerClose: document.getElementById("btn-mobile-drawer-close"),
      mobileDrawerSummary: document.getElementById("mobile-drawer-summary"),
      mdTabs: document.querySelectorAll(".md-tab"),

      loadingOverlay: document.getElementById("viewport-loading-overlay"),
      loadingTitle: document.getElementById("loading-overlay-title"),
      loadingSub: document.getElementById("loading-overlay-sub"),

      toastPill: document.getElementById("stage-toast-pill"),
      toastText: document.getElementById("stage-toast-text"),

      searchContainer: document.getElementById("search-container"),
      searchInput: document.getElementById("location-search-input"),
      btnSearchClear: document.getElementById("btn-search-clear"),
      autocompleteDropdown: autocompleteEl,
      searchDropdown: autocompleteEl,
      beachesStatusBadge: document.getElementById("beaches-status-badge"),
      regionPillsContainer: document.getElementById("region-pills-container"),
      beachesList: document.getElementById("beaches-list"),

      presetsRow: document.getElementById("presets-row"),
      partTabs: document.querySelectorAll(".part-tab"),
      swatchGrid: document.getElementById("swatch-grid"),
      activeSwatchLabel: document.getElementById("active-swatch-label"),
      btnSurpriseColor: document.getElementById("btn-surprise-color"),

      subdialBtns: document.querySelectorAll(".seg-btn"),
      sliderCondVal: document.getElementById("slider-cond-val"),
      ltBeachName: document.getElementById("lt-beach-name"),
      ltSwellSize: document.getElementById("lt-swell-size"),
      ltSwellPeriod: document.getElementById("lt-swell-period"),
      ltVerdictText: document.getElementById("lt-verdict-text"),

      lightBtns: document.querySelectorAll(".light-pill"),
      camBtns: document.querySelectorAll(".cam-btn[data-cam]"),
      sliderExplode: document.getElementById("slider-explode"),
      btnLiveDemo: document.getElementById("btn-live-demo"),

      btnOrder: document.getElementById("btn-order"),
      btnTopDownload: document.getElementById("btn-top-download"),
      btnQuickExportStl: document.getElementById("btn-quick-export-stl"),
      btnQuickExportFw: document.getElementById("btn-quick-export-fw"),

      modalBackdrop: document.getElementById("order-modal-backdrop"),
      btnModalClose: document.getElementById("btn-modal-close"),
      modalSummaryCard: document.getElementById("modal-summary-card"),
      btnExportCustomDialStl: document.getElementById("btn-export-custom-dial-stl"),
      btnDownloadFirmware: document.getElementById("btn-download-firmware"),
      btnDownloadWorkerJs: document.getElementById("btn-download-worker-js"),
      btnDownloadGuide: document.getElementById("btn-download-guide"),
      btnDownloadFullKit: document.getElementById("btn-download-full-kit"),
      fullKitBadge: document.getElementById("full-kit-badge"),
    };
  }

  _init3DEngine() {
    this.studio = new SurfClockStudio3D(this.dom.studioCanvas, {
      onBeachClick: (slotIdx) => {
        this.selectBeachIndex(slotIdx);
        const bName = this.state.beaches[slotIdx]?.name || "BEACH";
        this.showToast(`📍 Pointing to ${bName}`);
      },
      onExplodeChange: (fac) => {
        this.state.explodeFactor = fac;
        if (this.dom.sliderExplode) {
          this.dom.sliderExplode.value = String(fac.toFixed(2));
        }
      },
      onReady: () => {
        this._syncAllToStudio();
        this._applyDemoQueryHooks();
      },
    });
    this._syncAllToStudio();
  }

  showLoadingOverlay(title = "Loading 5 Best Beaches...", subtitle = "Scanning coastline & live Open-Meteo marine swell") {
    if (!this.dom.loadingOverlay) return;
    if (this.dom.loadingTitle) this.dom.loadingTitle.textContent = title;
    if (this.dom.loadingSub) this.dom.loadingSub.textContent = subtitle;
    this.dom.loadingOverlay.classList.remove("hidden");
  }

  hideLoadingOverlay() {
    if (!this.dom.loadingOverlay) return;
    this.dom.loadingOverlay.classList.add("hidden");
  }

  showToast(message, durationMs = 2400) {
    if (!this.dom.toastPill || !this.dom.toastText) return;
    this.dom.toastText.textContent = message;
    this.dom.toastPill.classList.remove("hidden");
    clearTimeout(this.toastTimeout);
    this.toastTimeout = setTimeout(() => {
      this.dom.toastPill.classList.add("hidden");
    }, durationMs);
  }

  setLightingMode(mode) {
    const normalized = mode === "nightlight" || mode === "dawn" ? "nightlight" : "daylight";
    this.state.lightingMode = normalized;
    this.dom.lightBtns.forEach((b) => {
      const isActive = b.dataset.light === normalized;
      b.classList.toggle("active", isActive);
      b.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
    const isNight = normalized === "nightlight";
    document.body.classList.toggle("night-mode", isNight);
    this.dom.viewportStage.classList.toggle("night-stage", isNight);
    if (this.studio) {
      this.studio.setLightingMode(normalized);
    }
    if (this._drawStaticHudWave) this._drawStaticHudWave();
  }

  _resolveKeyAccentHex(preferredPart = null) {
    if (!preferredPart && this.state.activeEditionId && EDITION_ACCENT_HEX[this.state.activeEditionId]) {
      return EDITION_ACCENT_HEX[this.state.activeEditionId];
    }
    const paleNeutrals = new Set([
      "#E8E3D9", "#CDC5B4", "#B8B2A8", "#EFECE4", "#F5F3ED", "#D6CBB8",
      "#ECE7DC", "#E4DCD0", "#D6CFC2", "#F2EFE9", "#EAE4D8", "#DDD6C8", "#F7F6F2", "#F4F1EA"
    ]);
    const checkOrder = preferredPart
      ? [preferredPart, "bezel", "hands", "dial", "deck", "inlay"]
      : ["bezel", "hands", "dial", "deck", "inlay"];

    for (const part of checkOrder) {
      const sw = this._getSwatchObj(part, this.state.colors[part]);
      if (sw && sw.hex && !paleNeutrals.has(sw.hex.toUpperCase())) {
        if (part === "inlay" && preferredPart !== "inlay") continue;
        return sw.hex;
      }
    }
    return "#FF4F00";
  }

  _syncSwellKeyColor(preferredPart = null, immediate = false) {
    const hex = this._resolveKeyAccentHex(preferredPart);
    this.state.activeAccentHex = hex;
    document.documentElement.style.setProperty("--swell-key-color", hex);
    if (this.studio && this.studio.setSwellAccentColor) {
      this.studio.setSwellAccentColor(hex, immediate);
    }
    if (this._drawStaticHudWave) this._drawStaticHudWave();
  }

  setMobileDrawerOpen(isOpen, section = null) {
    this.state.mobileDrawerOpen = Boolean(isOpen);
    if (section) {
      this.state.mobileDrawerTab = section;
    }
    const activeTab = this.state.mobileDrawerTab || "beaches";
    document.body.classList.toggle("mobile-drawer-open", this.state.mobileDrawerOpen);
    if (this.dom.btnMobileDrawerToggle) {
      this.dom.btnMobileDrawerToggle.setAttribute("aria-expanded", this.state.mobileDrawerOpen ? "true" : "false");
    }
    if (this.dom.customizerPanel) {
      this.dom.customizerPanel.style.transform = "";
      this.dom.customizerPanel.dataset.activeMdtab = activeTab;
    }
    if (this.dom.mdTabs) {
      this.dom.mdTabs.forEach((t) => {
        const isSelected = t.dataset.mdtab === activeTab;
        t.classList.toggle("active", isSelected);
        t.setAttribute("aria-selected", isSelected ? "true" : "false");
      });
    }
    this.studio?.setMobileDrawerOffset?.(this.state.mobileDrawerOpen, 0.52);
  }

  openMobileDrawer(tabId = null) {
    this.setMobileDrawerOpen(true, tabId || this.state.mobileDrawerTab || "beaches");
  }

  closeMobileDrawer() {
    this.setMobileDrawerOpen(false);
  }

  toggleMobileDrawer() {
    this.setMobileDrawerOpen(!this.state.mobileDrawerOpen, this.state.mobileDrawerTab || "beaches");
  }

  _escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  _scheduleDialRebuild() {
    if (!this.studio) return;
    this.studio.updateDialTypography(
      this.state.beaches.map((b) => b.name),
      this.state.subdialMode,
      this.state.activeRegion.shortName
    );
  }

  _updateSummaryUI() {
    this._updateAllLabels();
  }

  _syncSubdialNeedle() {
    if (!this.studio) return;
    if (this.state.subdialMode === "swell") {
      const hM = Number(this.state.activeSwellHeightM) || 1.9;
      const mapped = Math.max(1.0, Math.min(10.0, 1.0 + (hM / 3.2) * 9.0));
      this.studio.setWorthItScore(mapped);
    } else {
      this.studio.setWorthItScore(this.state.conditionsRating);
    }
  }

  _syncAllToStudio() {
    if (!this.studio) return;
    for (const part of ["bezel", "dial", "inlay", "hands", "deck"]) {
      this.studio.setComponentSwatch(part, this.state.colors[part]);
    }
    const names = this.state.beaches.map((b) => b.name);
    this.studio.updateDialTypography(names, this.state.subdialMode, this.state.activeRegion.shortName);
    this.studio.pointToBeachSlot(this.state.selectedBeachIndex);
    this._syncSubdialNeedle();
    this._syncSwellKeyColor(null, true);
    this._syncTelemetryToStudio();
  }

  _syncTelemetryToStudio() {
    if (!this.studio || !this.studio.setSwellTelemetry) return;
    this.studio.setSwellTelemetry({
      swellHeightM: this.state.activeSwellHeightM,
      swellPeriodS: this.state.activeSwellPeriodS,
      swellDir: this.state.activeSwellDir,
      worthItScore: this.state.conditionsRating,
      activeBeachIndex: this.state.selectedBeachIndex,
    });
  }

  _getSwatchObj(part, swatchId) {
    const list = COMPONENT_SWATCHES[part] || [];
    return list.find((s) => s.id === swatchId) || list[0];
  }

  _renderRegionPills() {
    this.dom.regionPillsContainer.innerHTML = "";
    CURATED_REGIONS.slice(0, 9).forEach((region) => {
      const isActive = region.id === this.state.activeRegion.id;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `region-pill ${isActive ? "active" : ""}`;
      btn.setAttribute("aria-pressed", isActive ? "true" : "false");
      btn.textContent = region.shortName;
      btn.addEventListener("click", () => this.selectRegionPreset(region));
      this.dom.regionPillsContainer.appendChild(btn);
    });
  }

  _computeBestBeachIndex() {
    let bestIdx = 0;
    let bestQ = -1;
    this.state.beaches.forEach((b, i) => {
      const q = b.quality ?? 8.5;
      if (q > bestQ) {
        bestQ = q;
        bestIdx = i;
      }
    });
    this.state.bestBeachIndex = bestIdx;
    return bestIdx;
  }

  _renderBeachesList() {
    this.dom.beachesList.innerHTML = "";
    const bestIdx = this._computeBestBeachIndex();

    this.state.beaches.forEach((beach, idx) => {
      const isSelected = idx === this.state.selectedBeachIndex;
      const isBest = idx === bestIdx;
      const row = document.createElement("div");
      row.className = `beach-row ${isSelected ? "active-beach" : ""}`;

      const num = document.createElement("div");
      num.className = "beach-num";
      num.textContent = String(idx + 1).padStart(2, "0");

      const input = document.createElement("input");
      input.type = "text";
      input.className = "beach-name-input";
      input.value = beach.name;
      input.maxLength = 12;
      input.setAttribute("aria-label", `Beach ${idx + 1} name`);

      input.addEventListener("click", (e) => {
        e.stopPropagation();
        this.selectBeachIndex(idx);
      });

      input.addEventListener("input", (e) => {
        this._stopLiveDemo();
        const raw = e.target.value.toUpperCase();
        if (e.target.value !== raw) {
          const pos = e.target.selectionStart;
          e.target.value = raw;
          try {
            e.target.setSelectionRange(pos, pos);
          } catch (_) {}
        }
        this.state.beaches[idx].name = formatDialBeachName(raw) || `BEACH ${idx + 1}`;
        this._scheduleDialRebuild();
        this._updateSummaryUI();
      });

      input.addEventListener("blur", () => {
        const formatted = formatDialBeachName(input.value) || `BEACH ${idx + 1}`;
        this.state.beaches[idx].name = formatted;
        input.value = formatted;
        this._scheduleDialRebuild();
        this._updateSummaryUI();
      });

      const tag = document.createElement("button");
      tag.type = "button";
      tag.className = `beach-point-tag ${isBest ? "is-best" : ""}`;
      tag.setAttribute("aria-pressed", isSelected ? "true" : "false");
      tag.setAttribute("aria-label", `Point clock hand to ${beach.name || `Beach ${idx + 1}`}`);
      if (isSelected && isBest) {
        tag.textContent = "★ Best Now";
      } else if (isSelected) {
        tag.textContent = "Pointing";
      } else if (isBest) {
        tag.textContent = "Best Now";
      } else {
        tag.textContent = "Select";
      }

      tag.addEventListener("click", (e) => {
        e.stopPropagation();
        this.selectBeachIndex(idx);
      });

      row.addEventListener("click", () => {
        this.selectBeachIndex(idx);
      });

      row.appendChild(num);
      row.appendChild(input);
      row.appendChild(tag);
      this.dom.beachesList.appendChild(row);
    });
  }

  _renderPresetChips() {
    this.dom.presetsRow.innerHTML = "";
    CURATED_EDITIONS.forEach((edition) => {
      const isActive = edition.id === this.state.activeEditionId;
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = `preset-chip ${isActive ? "active" : ""}`;
      chip.setAttribute("aria-pressed", isActive ? "true" : "false");

      const dots = document.createElement("span");
      dots.className = "preset-dots";
      [
        this._getSwatchObj("bezel", edition.bezel),
        this._getSwatchObj("dial", edition.dial),
        this._getSwatchObj("hands", edition.hands),
      ].forEach((sw) => {
        const dot = document.createElement("span");
        dot.className = "preset-dot";
        dot.style.background = sw ? sw.hex : "#ccc";
        dots.appendChild(dot);
      });

      const label = document.createElement("span");
      label.textContent = edition.name;

      chip.appendChild(dots);
      chip.appendChild(label);
      chip.addEventListener("click", () => this.applyEdition(edition));
      this.dom.presetsRow.appendChild(chip);
    });
  }

  _renderSwatchGrid() {
    this.dom.swatchGrid.innerHTML = "";
    const part = this.state.activePart;
    const list = COMPONENT_SWATCHES[part] || [];
    const activeId = this.state.colors[part];

    list.forEach((swatch) => {
      const isActive = swatch.id === activeId;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `swatch-btn ${isActive ? "active" : ""} ${
        swatch.transmission ? "translucent-swatch" : ""
      }`;
      btn.style.backgroundColor = swatch.hex;
      btn.title = swatch.name;
      btn.setAttribute("aria-label", swatch.name);
      btn.setAttribute("aria-pressed", isActive ? "true" : "false");

      btn.addEventListener("click", () => {
        this.setPartSwatch(part, swatch.id);
      });

      this.dom.swatchGrid.appendChild(btn);
    });
  }

  selectRegionPreset(region, silentOverlay = false) {
    this._stopLiveDemo();
    const seq = ++this._regionSeq;
    if (!silentOverlay) {
      this.showLoadingOverlay(
        `Loading 5 Best Beaches...`,
        `Calibrating dial & live swell for ${region.name}`
      );
      clearTimeout(this.loadingTimeout);
      this.loadingTimeout = setTimeout(() => {
        if (seq === this._regionSeq) this.hideLoadingOverlay();
      }, 460);
    }

    this.state.activeRegion = { ...region };
    this.state.liveMarineData = null;
    this.state.beaches = region.beaches.map((b) => ({ ...b }));

    let bestIdx = region.activeSlot ?? 0;
    let maxQ = -1;
    this.state.beaches.forEach((b, i) => {
      if ((b.quality ?? 0) > maxQ) {
        maxQ = b.quality;
        bestIdx = i;
      }
    });
    this.state.selectedBeachIndex = bestIdx;
    this._recomputeActiveBeachConditions();

    this._renderRegionPills();
    this._renderBeachesList();
    this.studio.updateDialTypography(
      this.state.beaches.map((b) => b.name),
      this.state.subdialMode,
      region.shortName
    );
    this.studio.pointToBeachSlot(this.state.selectedBeachIndex);
    this._syncSubdialNeedle();
    if (this.studio.triggerWavePulse) {
      this.studio.triggerWavePulse(1.15);
    }
    this._syncTelemetryToStudio();
    this._updateAllLabels();
    this.dom.beachesStatusBadge.textContent = `5 breaks loaded for ${region.shortName}`;

    this._fetchLiveWaveTelemetry(region.lat, region.lng ?? region.lon);
  }

  selectBeachIndex(idx, fromDemo = false) {
    if (!fromDemo) {
      this._stopLiveDemo();
    }
    this.state.selectedBeachIndex = idx;
    this._recomputeActiveBeachConditions();

    const rows = this.dom.beachesList ? this.dom.beachesList.querySelectorAll(".beach-row") : [];
    if (rows.length === this.state.beaches.length && rows.length > 0) {
      const bestIdx = this._computeBestBeachIndex();
      rows.forEach((row, i) => {
        const isSelected = i === idx;
        const isBest = i === bestIdx;
        row.classList.toggle("active-beach", isSelected);

        const num = row.querySelector(".beach-num");
        if (num) {
          num.textContent = String(i + 1).padStart(2, "0");
        }

        const tag = row.querySelector(".beach-point-tag");
        if (tag) {
          tag.textContent = isSelected ? (isBest ? "★ Best Now" : "Pointing") : (isBest ? "Best Now" : "Select");
          tag.classList.toggle("is-best", isBest);
          tag.setAttribute("aria-pressed", isSelected ? "true" : "false");
        }

        const input = row.querySelector(".beach-name-input");
        if (input && document.activeElement !== input) {
          input.value = this.state.beaches[i].name;
        }
      });
    } else {
      this._renderBeachesList();
    }

    this.studio.pointToBeachSlot(idx);
    this._syncSubdialNeedle();
    if (this.studio.triggerWavePulse) {
      this.studio.triggerWavePulse(0.95);
    }
    this._syncTelemetryToStudio();
    this._updateAllLabels();
  }

  selectPart(part) {
    this.state.activePart = part;
    this.dom.partTabs.forEach((t) => {
      const isSelected = t.dataset.part === part;
      t.classList.toggle("active", isSelected);
      t.setAttribute("aria-selected", isSelected ? "true" : "false");
    });
    this._renderSwatchGrid();
    this._updateAllLabels();
  }

  setPartSwatch(part, swatchId) {
    this.state.colors[part] = swatchId;
    this.state.activeEditionId = "";
    this.studio.setComponentSwatch(part, swatchId);
    this._syncSwellKeyColor(part, false);
    this._renderPresetChips();
    this._renderSwatchGrid();
    this._updateAllLabels();
  }

  applyEdition(edition) {
    this.state.activeEditionId = edition.id;
    this.state.colors = {
      bezel: edition.bezel,
      dial: edition.dial,
      inlay: edition.inlay,
      hands: edition.hands,
      deck: edition.deck,
    };
    if (edition.subdialMode && edition.subdialMode !== this.state.subdialMode) {
      this.state.subdialMode = edition.subdialMode;
      this.dom.subdialBtns.forEach((b) => {
        const isActive = b.dataset.submode === this.state.subdialMode;
        b.classList.toggle("active", isActive);
        b.setAttribute("aria-pressed", isActive ? "true" : "false");
      });
      this.studio.updateDialTypography(
        this.state.beaches.map((b) => b.name),
        this.state.subdialMode,
        this.state.activeRegion.shortName
      );
      this._syncSubdialNeedle();
    }
    for (const part of ["bezel", "dial", "inlay", "hands", "deck"]) {
      this.studio.setComponentSwatch(part, this.state.colors[part]);
    }
    this._syncSwellKeyColor(null, false);
    this._renderPresetChips();
    this._renderSwatchGrid();
    this._updateAllLabels();
  }

  _hexLuminance(hex) {
    const clean = String(hex || "#000000").replace("#", "").trim();
    const expanded = clean.length === 3 ? clean.split("").map((c) => c + c).join("") : clean;
    const num = parseInt(expanded, 16) || 0;
    const srgb = [(num >> 16) & 255, (num >> 8) & 255, num & 255].map((v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2];
  }

  _contrastRatio(hex1, hex2) {
    const l1 = this._hexLuminance(hex1);
    const l2 = this._hexLuminance(hex2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  randomizeColors() {
    const bezelList = COMPONENT_SWATCHES.bezel || [];
    const dialList = COMPONENT_SWATCHES.dial || [];
    const inlayList = COMPONENT_SWATCHES.inlay || [];
    const handsList = COMPONENT_SWATCHES.hands || [];
    const deckList = COMPONENT_SWATCHES.deck || [];

    const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
    const bSw = pick(bezelList);
    const dSw = pick(dialList);
    const kSw = pick(deckList);

    const inlayPool = inlayList.filter((candidate) => this._contrastRatio(dSw.hex, candidate.hex) >= 2.8);
    const fallbackInlay = this._hexLuminance(dSw.hex) > 0.35
      ? (inlayList.find((s) => s.id === "charcoal") || { id: "charcoal", hex: "#141413" })
      : (inlayList.find((s) => s.id === "alabaster") || { id: "alabaster", hex: "#FAF8F5" });
    const iSw = inlayPool.length > 0 ? pick(inlayPool) : fallbackInlay;

    const handPool = handsList.filter(
      (candidate) => candidate.id !== dSw.id && this._contrastRatio(dSw.hex, candidate.hex) >= 2.8
    );
    const fallbackHand = this._hexLuminance(dSw.hex) > 0.35
      ? (handsList.find((s) => s.id === "charcoal") || handsList[0])
      : (handsList.find((s) => s.id === "alabaster") || handsList[0]);
    const hSw = handPool.length > 0 ? pick(handPool) : fallbackHand;

    this.state.activeEditionId = "";
    this.state.colors = {
      bezel: bSw.id,
      dial: dSw.id,
      inlay: iSw.id,
      hands: hSw.id,
      deck: kSw.id,
    };
    for (const part of ["bezel", "dial", "inlay", "hands", "deck"]) {
      this.studio.setComponentSwatch(part, this.state.colors[part]);
    }
    this._syncSwellKeyColor("bezel", false);
    if (this.studio.triggerWavePulse) {
      this.studio.triggerWavePulse(1.1);
    }
    this._renderPresetChips();
    this._renderSwatchGrid();
    this._updateAllLabels();
    this.showToast(`🎲 ${bSw.name} + ${dSw.name} + ${hSw.name}`);
  }

  // ============================================================================
  // GOOGLE MAPS-STYLE LIVE AUTOCOMPLETE DROPDOWN
  // ============================================================================
  _hideAutocomplete() {
    clearTimeout(this.searchDebounce);
    this._acSeq++;
    if (this.dom.autocompleteDropdown) {
      this.dom.autocompleteDropdown.classList.add("hidden");
    }
    if (this.dom.searchInput) {
      this.dom.searchInput.setAttribute("aria-expanded", "false");
    }
  }

  _highlightAutocompleteItem(items) {
    const nodes = items || (this.dom.autocompleteDropdown ? this.dom.autocompleteDropdown.querySelectorAll(".ac-item") : []);
    nodes.forEach((el, idx) => {
      const isSelected = idx === this.state.autocompleteIndex;
      el.classList.toggle("ac-active", isSelected);
      el.setAttribute("aria-selected", isSelected ? "true" : "false");
      if (isSelected && el.scrollIntoView) {
        el.scrollIntoView({ block: "nearest" });
      }
    });
  }

  async _updateAutocompleteSuggestions(query) {
    const q = (query || "").trim();
    this.dom.btnSearchClear.classList.toggle("hidden", q.length === 0);
    const acSeq = ++this._acSeq;

    const results = await searchLocationsAutocomplete(q);
    if (acSeq !== this._acSeq) return results || [];
    this.state.autocompleteItems = results || [];
    this.state.autocompleteIndex = results.length > 0 ? 0 : -1;
    this._lastResolvedQuery = q;
    this._renderAutocompleteDropdown();
    return this.state.autocompleteItems;
  }

  _renderAutocompleteDropdown() {
    const items = this.state.autocompleteItems;
    if (!items || items.length === 0) {
      this.dom.autocompleteDropdown.classList.add("hidden");
      this.dom.autocompleteDropdown.innerHTML = "";
      if (this.dom.searchInput) {
        this.dom.searchInput.setAttribute("aria-expanded", "false");
      }
      return;
    }

    this.dom.autocompleteDropdown.innerHTML = "";
    items.forEach((item, idx) => {
      const isSelected = idx === this.state.autocompleteIndex;
      const row = document.createElement("div");
      row.className = `ac-item ${isSelected ? "ac-active" : ""}`;
      row.setAttribute("role", "option");
      row.setAttribute("aria-selected", isSelected ? "true" : "false");

      row.innerHTML = `
        <svg class="ac-pin" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
          <circle cx="12" cy="10" r="3"></circle>
        </svg>
        <div class="ac-text">
          <div class="ac-main">${this._escapeHtml(item.label)}</div>
          <div class="ac-sub">${this._escapeHtml(item.sublabel || "")}</div>
        </div>
      `;

      row.addEventListener("mousedown", (e) => {
        e.preventDefault();
        this._selectAutocompleteItem(item);
      });
      row.addEventListener("click", (e) => {
        e.preventDefault();
        this._selectAutocompleteItem(item);
      });

      this.dom.autocompleteDropdown.appendChild(row);
    });

    this.dom.autocompleteDropdown.classList.remove("hidden");
    if (this.dom.searchInput) {
      this.dom.searchInput.setAttribute("aria-expanded", "true");
    }
    this._highlightAutocompleteItem();
  }

  async _selectAutocompleteItem(item) {
    if (!item) return;
    this._stopLiveDemo();
    this._hideAutocomplete();
    this.dom.searchInput.value = item.label;
    this.dom.btnSearchClear.classList.remove("hidden");

    if (item.regionId) {
      const reg = ALL_KNOWN_REGIONS.find((r) => r.id === item.regionId);
      if (reg) {
        this.selectRegionPreset(reg);
        return;
      }
    }

    const seq = ++this._regionSeq;
    clearTimeout(this.loadingTimeout);
    this.dom.beachesStatusBadge.textContent = `Finding 5 nearest beaches...`;
    this.showLoadingOverlay(
      "Loading 5 Best Beaches...",
      `Searching surf breaks & live swell near ${item.label}`
    );

    const minOverlayDelay = new Promise((r) => setTimeout(r, 480));
    try {
      const [resolved] = await Promise.all([
        resolve5BestLocalBeaches(item.lat, item.lng, item.label),
        minOverlayDelay,
      ]);

      if (seq !== this._regionSeq) return;
      if (resolved && resolved.beaches?.length === 5) {
        this.state.activeRegion = resolved.region;
        this.state.liveMarineData = null;
        this.state.beaches = resolved.beaches;
        this.state.selectedBeachIndex = 0;
        this._recomputeActiveBeachConditions();
        this._renderRegionPills();
        this._renderBeachesList();
        this.studio.updateDialTypography(
          this.state.beaches.map((b) => b.name),
          this.state.subdialMode,
          resolved.region.shortName
        );
        this.studio.pointToBeachSlot(0);
        this._syncSubdialNeedle();
        if (this.studio.triggerWavePulse) {
          this.studio.triggerWavePulse(1.25);
        }
        this._syncTelemetryToStudio();
        this._updateAllLabels();
        if (resolved.region?.name && (!item.lat && !item.lng)) {
          this.dom.searchInput.value = resolved.region.name;
        }
        this.dom.beachesStatusBadge.textContent = `5 nearest breaks to ${resolved.region.shortName}`;
        this.showToast(`📍 Loaded 5 breaks for ${resolved.region.shortName}`);

        this._fetchLiveWaveTelemetry(resolved.region.lat ?? item.lat, resolved.region.lng ?? item.lng);
      }
    } finally {
      if (seq === this._regionSeq) {
        this.hideLoadingOverlay();
      }
    }
  }

  _updateAllLabels() {
    const reg = this.state.activeRegion;
    const activeBeach = this.state.beaches[this.state.selectedBeachIndex]?.name || "DEE WHY";
    const swellM = this.state.activeSwellHeightM ?? 1.9;
    const swellFt = (swellM * 3.28084).toFixed(1);
    const periodS = this.state.activeSwellPeriodS ?? 13;
    const dir = this.state.activeSwellDir || "SSE";

    this.dom.hudRegionTitle.textContent = (reg.name || reg.shortName || "SYDNEY").toUpperCase();
    this.dom.hudSwellSummary.textContent = `BEST NOW: ${activeBeach} · ${swellM.toFixed(1)}m @ ${periodS}s ${dir}`;

    if (this.dom.hudSwellSize) {
      this.dom.hudSwellSize.textContent = `${swellM.toFixed(1)}m`;
    }
    if (this.dom.hudSwellFeet) {
      this.dom.hudSwellFeet.textContent = `(${swellFt}ft)`;
    }
    if (this.dom.hudSwellPeriod) {
      this.dom.hudSwellPeriod.textContent = `${periodS}s · ${dir}`;
    }
    if (this.dom.datumSwellVal) {
      this.dom.datumSwellVal.textContent = `${swellM.toFixed(1)}m (${swellFt}ft)`;
    }
    if (this.dom.datumSwellSub) {
      this.dom.datumSwellSub.textContent = `CAD FLOOR SWELL · ${periodS}s ${dir}`;
    }
    if (this.dom.datumCaliperLine) {
      const caliperPx = Math.round(Math.max(12, Math.min(44, 10 + swellM * 10.5)));
      this.dom.datumCaliperLine.style.height = `${caliperPx}px`;
    }
    if (this.dom.mobileDrawerSummary) {
      const ed = CURATED_EDITIONS.find((e) => e.id === this.state.activeEditionId);
      const colorName = ed ? ed.name : (this._getSwatchObj("bezel", this.state.colors.bezel)?.name || "Custom");
      this.dom.mobileDrawerSummary.textContent = `${colorName} · ${activeBeach} · STL`;
    }

    const part = this.state.activePart;
    const sw = this._getSwatchObj(part, this.state.colors[part]);
    this.dom.activeSwatchLabel.textContent = `${PART_LABELS[part]} · ${sw ? sw.name : ""}`;

    const v = Number(this.state.conditionsRating);
    if (this.dom.ltBeachName) {
      this.dom.ltBeachName.textContent = activeBeach;
    }
    if (this.dom.ltSwellSize) {
      this.dom.ltSwellSize.textContent = `${swellM.toFixed(1)}m (${swellFt}ft)`;
    }
    if (this.dom.ltSwellPeriod) {
      this.dom.ltSwellPeriod.textContent = `${periodS}s ${dir}`;
    }
    const verdict = v >= 6.5 ? "YEAH" : v >= 4.5 ? "MAYBE" : "NAH";
    if (this.dom.sliderCondVal) {
      if (this.state.subdialMode === "conditions") {
        this.dom.sliderCondVal.textContent = `LIVE: ${v.toFixed(1)} / 10`;
      } else if (this.state.subdialMode === "swell") {
        this.dom.sliderCondVal.textContent = `LIVE: ${swellM.toFixed(1)}m (${swellFt}ft)`;
      } else {
        this.dom.sliderCondVal.textContent = `LIVE: ${verdict} (${v.toFixed(1)}/10)`;
      }
    }
    if (this.dom.ltVerdictText) {
      if (this.state.subdialMode === "conditions") {
        this.dom.ltVerdictText.textContent = `${v.toFixed(1)} / 10`;
      } else if (this.state.subdialMode === "swell") {
        const swellLabel = swellM >= 2.2 ? "EPIC" : swellM >= 1.2 ? "CLEAN" : "SMALL";
        this.dom.ltVerdictText.textContent = `${swellLabel} (${swellFt}ft)`;
      } else {
        this.dom.ltVerdictText.textContent = `${verdict} (${v.toFixed(1)})`;
      }
    }
  }

  // Mini 60fps Retina Oscilloscope Wave Visualizer inside the Top-Left Status Pill
  _startHudWaveLoop() {
    const canvas = this.dom.hudWaveCanvas;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const logicalW = 124;
    const logicalH = 38;

    const syncRetinaSize = () => {
      const dpr = window.devicePixelRatio || 1;
      const targetW = Math.round(logicalW * dpr);
      const targetH = Math.round(logicalH * dpr);
      if (canvas.width !== targetW || canvas.height !== targetH) {
        canvas.width = targetW;
        canvas.height = targetH;
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    syncRetinaSize();

    const drawFrame = (t) => {
      syncRetinaSize();
      ctx.clearRect(0, 0, logicalW, logicalH);

      const hM = this.state.activeSwellHeightM ?? 1.9;
      const amp = Math.min(8.5, Math.max(2.8, hM * 2.9));
      const isNight = this.state.lightingMode === "nightlight";

      const isEastSwell = /^(NNE|NE|ENE|E|ESE|SE|SSE)$/.test(String(this.state.activeSwellDir || "").trim().toUpperCase());
      const dirSign = isEastSwell ? 1.0 : -1.0;

      // Secondary depth wave in HUD oscilloscope
      ctx.beginPath();
      for (let x = 4; x <= logicalW - 4; x++) {
        const env = Math.sin(((x - 4) / (logicalW - 8)) * Math.PI);
        const y = logicalH * 0.5 - Math.sin(x * 0.11 + dirSign * t * 0.75) * (amp * 0.65) * env;
        if (x === 4) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = isNight ? "rgba(56, 189, 248, 0.45)" : "rgba(255, 79, 0, 0.32)";
      ctx.lineWidth = 1.5;
      ctx.lineCap = "round";
      ctx.stroke();

      // Primary directional groundswell wave in HUD oscilloscope
      ctx.beginPath();
      for (let x = 4; x <= logicalW - 4; x++) {
        const env = Math.sin(((x - 4) / (logicalW - 8)) * Math.PI);
        const y = logicalH * 0.5 - Math.sin(x * 0.13 + dirSign * t * 0.95) * (0.75 + 0.25 * Math.cos(t * 0.8)) * amp * env;
        if (x === 4) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = this.state.activeAccentHex || (isNight ? "#38BDF8" : "#FF4F00");
      ctx.lineWidth = 2.2;
      ctx.lineCap = "round";
      ctx.stroke();
    };

    this._drawStaticHudWave = () => drawFrame(0.6);

    if (window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches) {
      drawFrame(0.6);
      return;
    }

    const draw = (now) => {
      requestAnimationFrame(draw);
      if (document.hidden || window.innerWidth <= 960) return;
      if (window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches) {
        drawFrame(0.6);
        return;
      }
      drawFrame(now * 0.0045);
    };
    requestAnimationFrame(draw);
  }

  _bindEvents() {
    this.dom.searchInput.addEventListener("focus", () => {
      this._updateAutocompleteSuggestions(this.dom.searchInput.value);
    });

    this.dom.searchInput.addEventListener("input", (e) => {
      const val = e.target.value;
      this.dom.btnSearchClear.classList.toggle("hidden", !val.trim());
      clearTimeout(this.searchDebounce);
      this.searchDebounce = setTimeout(() => {
        this._updateAutocompleteSuggestions(val);
      }, 110);
    });

    this.dom.searchInput.addEventListener("keydown", async (e) => {
      const items = this.state.autocompleteItems || [];
      const currentVal = (this.dom.searchInput.value || "").trim();
      const isFresh = this._lastResolvedQuery === currentVal;

      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (items.length > 0) {
          this.state.autocompleteIndex = (this.state.autocompleteIndex + 1) % items.length;
          this._highlightAutocompleteItem();
        }
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (items.length > 0) {
          this.state.autocompleteIndex = (this.state.autocompleteIndex - 1 + items.length) % items.length;
          this._highlightAutocompleteItem();
        }
      } else if (e.key === "Enter") {
        e.preventDefault();
        clearTimeout(this.searchDebounce);
        if (isFresh && items.length > 0 && this.state.autocompleteIndex >= 0) {
          this._selectAutocompleteItem(items[this.state.autocompleteIndex]);
        } else if (currentVal) {
          const freshItems = await this._updateAutocompleteSuggestions(currentVal);
          if (freshItems && freshItems.length > 0) {
            this._selectAutocompleteItem(freshItems[0]);
          } else {
            this._selectAutocompleteItem({
              label: currentVal,
              sublabel: `5 Best Local Surf Beaches near ${currentVal}`,
              lat: 0,
              lng: 0,
              regionId: null,
            });
          }
        }
      }
    });

    this.dom.btnSearchClear.addEventListener("click", () => {
      this.dom.searchInput.value = "";
      this.dom.btnSearchClear.classList.add("hidden");
      this.dom.searchInput.focus();
      this._updateAutocompleteSuggestions("");
    });

    document.addEventListener("click", (e) => {
      if (this.dom.searchContainer && !this.dom.searchContainer.contains(e.target)) {
        this._hideAutocomplete();
      }
    });

    this.dom.partTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        this.selectPart(tab.dataset.part);
      });
    });

    if (this.dom.btnSurpriseColor) {
      this.dom.btnSurpriseColor.addEventListener("click", () => {
        this.randomizeColors();
      });
    }

    const triggerPartyWave = () => {
      this._stopLiveDemo();
      if (this.studio && this.studio.triggerPartyWaveSalute) {
        this.studio.triggerPartyWaveSalute();
      }
      this.showToast("🌊 Shaka! Party Wave Salute Activated");
    };
    if (this.dom.brandEasterEgg) {
      this.dom.brandEasterEgg.addEventListener("click", triggerPartyWave);
      this.dom.brandEasterEgg.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          triggerPartyWave();
        }
      });
    }

    const triggerSetPulse = () => {
      if (this.studio && this.studio.triggerWavePulse) {
        this.studio.triggerWavePulse(1.55);
      }
      this.showToast(`🌊 Set Wave Rolling Through (${this.state.activeSwellHeightM.toFixed(1)}m @ ${this.state.activeSwellPeriodS}s)`);
    };
    if (this.dom.hudSwellHeroCard) {
      this.dom.hudSwellHeroCard.style.cursor = "pointer";
      this.dom.hudSwellHeroCard.title = "Click to trigger a rogue wave set pulse";
      this.dom.hudSwellHeroCard.addEventListener("click", triggerSetPulse);
      this.dom.hudSwellHeroCard.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          triggerSetPulse();
        }
      });
    }
    if (this.dom.hudWaveCanvas) {
      this.dom.hudWaveCanvas.addEventListener("click", triggerSetPulse);
    }

    if (this.dom.studioCanvas) {
      this.dom.studioCanvas.addEventListener("dblclick", () => {
        const nextExplode = this.state.explodeFactor > 0.35 ? 0.0 : 0.92;
        this.state.explodeFactor = nextExplode;
        if (this.dom.sliderExplode) {
          this.dom.sliderExplode.value = String(nextExplode);
        }
        const targetCam = nextExplode > 0.35 ? "exploded" : "front";
        this._setCameraViewState(targetCam);
        this.studio.setCameraPreset(targetCam);
        this.studio.setExplodeFactor(nextExplode);
        this.showToast(nextExplode > 0.35 ? "🔧 Exploded Internal Architecture" : "🔩 Assembled Monolith");
      });
    }

    this.dom.subdialBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.dataset.submode;
        this.state.subdialMode = mode;
        this.dom.subdialBtns.forEach((b) => {
          const isActive = b === btn;
          b.classList.toggle("active", isActive);
          b.setAttribute("aria-pressed", isActive ? "true" : "false");
        });
        this.studio.updateDialTypography(
          this.state.beaches.map((b) => b.name),
          mode,
          this.state.activeRegion.shortName
        );
        this._syncSubdialNeedle();
        this._updateAllLabels();
      });
    });

    this.dom.lightBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.dataset.light;
        this.setLightingMode(mode);
      });
    });

    this.dom.camBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const view = btn.dataset.cam;
        this._setCameraViewState(view);
        if (this.dom.swellScaleDatum) {
          this.dom.swellScaleDatum.classList.toggle("macro-hidden", view === "macro" || view === "subdial" || view === "rear");
        }
        this.studio.setCameraPreset(view);
      });
    });

    if (this.dom.btnMobileDrawerToggle) {
      this.dom.btnMobileDrawerToggle.addEventListener("click", () => {
        if (this._suppressNextDrawerClick) {
          this._suppressNextDrawerClick = false;
          return;
        }
        this.toggleMobileDrawer();
      });
    }
    if (this.dom.btnMobileDrawerClose) {
      this.dom.btnMobileDrawerClose.addEventListener("click", (e) => {
        e.stopPropagation();
        this.setMobileDrawerOpen(false);
      });
    }
    if (this.dom.mdTabs) {
      this.dom.mdTabs.forEach((tab) => {
        tab.addEventListener("click", (e) => {
          e.stopPropagation();
          this.setMobileDrawerOpen(true, tab.dataset.mdtab);
        });
      });
    }
    if (this.dom.btnMobileSearchTrigger) {
      this.dom.btnMobileSearchTrigger.addEventListener("click", (e) => {
        e.stopPropagation();
        this.setMobileDrawerOpen(true, "beaches");
        setTimeout(() => this.dom.searchInput && this.dom.searchInput.focus(), 180);
      });
    }
    if (this.dom.stageStatusPill) {
      this.dom.stageStatusPill.addEventListener("click", (e) => {
        if (
          window.innerWidth <= 960 &&
          !e.target.closest("#btn-live-demo") &&
          !e.target.closest("#btn-mobile-search-trigger")
        ) {
          this.setMobileDrawerOpen(true, "beaches");
        }
      });
    }

    // Touch / pointer drag gesture on #mobile-drawer-bar
    if (this.dom.mobileDrawerBar && this.dom.customizerPanel) {
      let dragStartY = null;
      let dragDeltaY = 0;
      let isDraggingDrawer = false;

      const onDragStart = (clientY, target) => {
        if (window.innerWidth > 960) return;
        if (target && (target.closest(".md-tab") || target.closest(".md-close-btn"))) return;
        dragStartY = clientY;
        dragDeltaY = 0;
        isDraggingDrawer = false;
      };

      const onDragMove = (clientY) => {
        if (dragStartY === null || window.innerWidth > 960) return;
        const dy = clientY - dragStartY;
        dragDeltaY = dy;
        if (Math.abs(dy) > 6) {
          isDraggingDrawer = true;
          this.dom.customizerPanel.style.transition = "none";
          if (this.state.mobileDrawerOpen && dy > 0) {
            this.dom.customizerPanel.style.transform = `translateY(${Math.min(dy, 380)}px)`;
          } else if (!this.state.mobileDrawerOpen && dy < 0) {
            this.dom.customizerPanel.style.transform = `translateY(calc(100% - 56px + ${Math.max(dy, -380)}px))`;
          }
        }
      };

      const onDragEnd = () => {
        if (dragStartY === null) return;
        const dy = dragDeltaY;
        const wasDragging = isDraggingDrawer;
        dragStartY = null;
        dragDeltaY = 0;
        isDraggingDrawer = false;
        this.dom.customizerPanel.style.transition = "";
        this.dom.customizerPanel.style.transform = "";

        if (wasDragging) {
          this._suppressNextDrawerClick = true;
          setTimeout(() => {
            this._suppressNextDrawerClick = false;
          }, 80);
          if (this.state.mobileDrawerOpen && dy > 38) {
            this.setMobileDrawerOpen(false);
          } else if (!this.state.mobileDrawerOpen && dy < -28) {
            this.setMobileDrawerOpen(true, this.state.mobileDrawerTab || "beaches");
          }
        }
      };

      this.dom.mobileDrawerBar.addEventListener("touchstart", (e) => {
        if (e.touches && e.touches.length === 1) {
          onDragStart(e.touches[0].clientY, e.target);
        }
      }, { passive: true });
      this.dom.mobileDrawerBar.addEventListener("touchmove", (e) => {
        if (e.touches && e.touches.length === 1) {
          onDragMove(e.touches[0].clientY);
        }
      }, { passive: true });
      this.dom.mobileDrawerBar.addEventListener("touchend", onDragEnd);
      this.dom.mobileDrawerBar.addEventListener("touchcancel", onDragEnd);

      this.dom.mobileDrawerBar.addEventListener("pointerdown", (e) => {
        if (e.pointerType === "touch") return;
        onDragStart(e.clientY, e.target);
      });
      window.addEventListener("pointermove", (e) => {
        if (e.pointerType === "touch" || dragStartY === null) return;
        onDragMove(e.clientY);
      });
      window.addEventListener("pointerup", (e) => {
        if (e.pointerType === "touch" || dragStartY === null) return;
        onDragEnd();
      });
    }

    // Outside-tap dismissal on viewportStage when mobile drawer is open
    if (this.dom.viewportStage) {
      let stageDownX = 0;
      let stageDownY = 0;
      this.dom.viewportStage.addEventListener("pointerdown", (e) => {
        stageDownX = e.clientX;
        stageDownY = e.clientY;
      });
      this.dom.viewportStage.addEventListener("pointerup", (e) => {
        if (window.innerWidth <= 960 && this.state.mobileDrawerOpen) {
          const dist = Math.hypot(e.clientX - stageDownX, e.clientY - stageDownY);
          if (
            dist < 6 &&
            !e.target.closest(".stage-status-pill") &&
            !e.target.closest(".camera-dock")
          ) {
            this.setMobileDrawerOpen(false);
          }
        }
      });
    }

    // Interactive Explode Slider
    if (this.dom.sliderExplode) {
      this.dom.sliderExplode.addEventListener("input", (e) => {
        const val = parseFloat(e.target.value);
        this.state.explodeFactor = val;
        if (val > 0.15 && this.state.cameraView !== "exploded") {
          this._setCameraViewState("exploded");
          if (this.dom.swellScaleDatum) this.dom.swellScaleDatum.classList.add("macro-hidden");
          this.studio.setCameraPreset("exploded");
        } else if (val <= 0.04 && this.state.cameraView === "exploded") {
          this._setCameraViewState("front");
          if (this.dom.swellScaleDatum) this.dom.swellScaleDatum.classList.remove("macro-hidden");
          this.studio.setCameraPreset("front");
        }
        this.studio.setExplodeFactor(val);
      });
    }

    this.dom.btnLiveDemo.addEventListener("click", () => {
      this.toggleLiveDemo();
    });

    const openModal = () => this.openOrderModal();
    this.dom.btnOrder.addEventListener("click", openModal);
    this.dom.btnTopDownload.addEventListener("click", openModal);

    this.dom.btnQuickExportStl.addEventListener("click", () => {
      this.studio.exportCustomDialSTL(this.state.activeRegion.code || "CUSTOM", true);
      this.showToast("⬇ Downloading Custom 3D Dial STL...");
    });
    this.dom.btnQuickExportFw.addEventListener("click", () => {
      this.downloadSpotsJson();
      this.showToast("⬇ Downloading spots.json Firmware Config...");
    });

    this.dom.btnModalClose.addEventListener("click", () => {
      this.closeOrderModal();
    });
    this.dom.modalBackdrop.addEventListener("click", (e) => {
      if (e.target === this.dom.modalBackdrop) {
        this.closeOrderModal();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        if (this.dom.searchDropdown && !this.dom.searchDropdown.classList.contains("hidden")) {
          this._hideAutocomplete();
          e.preventDefault();
          return;
        } else if (this.dom.modalBackdrop && !this.dom.modalBackdrop.classList.contains("hidden")) {
          this.closeOrderModal();
          e.preventDefault();
          return;
        } else if (this.state.mobileDrawerOpen) {
          this.setMobileDrawerOpen(false);
          e.preventDefault();
          return;
        }
      } else if (e.key === "Tab" && this.dom.modalBackdrop && !this.dom.modalBackdrop.classList.contains("hidden")) {
        const focusables = Array.from(
          this.dom.modalBackdrop.querySelectorAll(
            'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
          )
        );
        if (focusables.length > 0) {
          const first = focusables[0];
          const last = focusables[focusables.length - 1];
          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    });

    this.dom.btnExportCustomDialStl.addEventListener("click", () => {
      this.studio.exportCustomDialSTL(this.state.activeRegion.code || "CUSTOM", true);
    });
    this.dom.btnDownloadFirmware.addEventListener("click", () => this.downloadSpotsJson());
    this.dom.btnDownloadWorkerJs.addEventListener("click", () => this.downloadCustomWorkerJs());
    this.dom.btnDownloadGuide.addEventListener("click", () => this.downloadBuildGuideMarkdown());
    if (this.dom.btnDownloadFullKit) {
      this.dom.btnDownloadFullKit.addEventListener("click", () => this.handleDownloadFullKit());
    }
  }

  _stopLiveDemo() {
    if (this.demoTimer) {
      clearInterval(this.demoTimer);
      this.demoTimer = null;
    }
    if (this.state.liveDemoRunning) {
      this.state.liveDemoRunning = false;
      if (this.dom.btnLiveDemo) {
        this.dom.btnLiveDemo.classList.remove("active");
        this.dom.btnLiveDemo.setAttribute("aria-pressed", "false");
        this.dom.btnLiveDemo.innerHTML = `<span class="play-dot"></span> Test Sweep`;
      }
    }
  }

  toggleLiveDemo() {
    if (this.state.liveDemoRunning) {
      this._stopLiveDemo();
      this.showToast("⏸ Swell Cycle Paused");
      return;
    }

    this.state.liveDemoRunning = true;
    if (this.dom.btnLiveDemo) {
      this.dom.btnLiveDemo.classList.add("active");
      this.dom.btnLiveDemo.setAttribute("aria-pressed", "true");
    }
    this.showToast("🌊 Live Swell Cycle Started");
    this.selectBeachIndex((this.state.selectedBeachIndex + 1) % 5, true);
    this.demoTimer = setInterval(() => {
      this.selectBeachIndex((this.state.selectedBeachIndex + 1) % 5, true);
    }, 2200);
  }

  openOrderModal() {
    if (this.dom.modalBackdrop && this.dom.modalBackdrop.classList.contains("hidden")) {
      const active = document.activeElement; this._lastFocusedBeforeModal = (active && active !== document.body && active !== document.documentElement) ? active : this.dom.btnOrder;
    }
    const fSw = this._getSwatchObj("bezel", this.state.colors.bezel);
    const dSw = this._getSwatchObj("dial", this.state.colors.dial);
    const hSw = this._getSwatchObj("hands", this.state.colors.hands);

    this.dom.modalSummaryCard.innerHTML = `
      <div class="sum-row"><span class="sum-label">Coastline</span><span class="sum-val">${this._escapeHtml(this.state.activeRegion.name)}</span></div>
      <div class="sum-row"><span class="sum-label">5 Custom Beaches</span><span class="sum-val">${this.state.beaches.map((b) => this._escapeHtml(b.name)).join(" · ")}</span></div>
      <div class="sum-row"><span class="sum-label">Live Swell Size</span><span class="sum-val">${this.state.activeSwellHeightM.toFixed(1)}m (${(this.state.activeSwellHeightM * 3.28084).toFixed(1)}ft) @ ${this.state.activeSwellPeriodS}s ${this._escapeHtml(this.state.activeSwellDir)}</span></div>
      <div class="sum-row"><span class="sum-label">Outer Frame</span><span class="sum-val">${this._escapeHtml(fSw ? fSw.name : "")}</span></div>
      <div class="sum-row"><span class="sum-label">Dial Faceplate</span><span class="sum-val">${this._escapeHtml(dSw ? dSw.name : "")}</span></div>
      <div class="sum-row"><span class="sum-label">Hands Accent</span><span class="sum-val">${this._escapeHtml(hSw ? hSw.name : "")}</span></div>
    `;
    this.dom.modalBackdrop.classList.remove("hidden");
    this.dom.btnModalClose?.focus?.();
  }

  closeOrderModal() {
    if (this.dom.modalBackdrop) {
      this.dom.modalBackdrop.classList.add("hidden");
    }
    const target = this._lastFocusedBeforeModal || this.dom.btnOrder;
    this._lastFocusedBeforeModal = null;
    if (target && typeof target.focus === "function") {
      target.focus();
    }
  }

  async handleDownloadFullKit() {
    const badge = this.dom.fullKitBadge;
    const origBadge = badge ? badge.textContent : "Full Stack ↓";
    if (badge) badge.textContent = "⏳ Building...";
    this.showToast("📦 Packaging Custom 3D Dial + Hardcoded ESP32 Firmware...");

    try {
      const filename = await downloadFullStackCustomKit({
        state: this.state,
        studio: this.studio,
        onProgress: (msg, pct) => {
          if (badge) badge.textContent = `${pct}% ↓`;
          console.log(`[FullStackKit] ${pct}% - ${msg}`);
        },
      });
      this.showToast(`✅ Downloaded ${filename}!`);
    } catch (err) {
      console.error("[FullStackKit] Error:", err);
      this.showToast("⚠️ Falling back to base package...");
      const a = document.createElement("a");
      a.href = "./downloads/SC01_Surf_Clock_Open_Source_Kit.zip";
      a.download = "SC01_Surf_Clock_Open_Source_Kit.zip";
      document.body.appendChild(a);
      a.click();
      setTimeout(() => document.body.removeChild(a), 200);
    } finally {
      if (badge) badge.textContent = origBadge;
    }
  }

  downloadSpotsJson() {
    const spots = buildClockwiseSpots(this.state.beaches, this.state.activeRegion);
    const blob = new Blob([JSON.stringify(spots, null, 2)], { type: "application/json" });
    this._triggerDownload(blob, "spots.json");
  }

  async downloadCustomWorkerJs() {
    const spots = buildClockwiseSpots(this.state.beaches, this.state.activeRegion);
    let baseWorkerJs = "";
    try {
      const res = await fetch("./downloads/cloudflare-worker/src/index.js");
      if (res.ok) {
        baseWorkerJs = await res.text();
      }
    } catch (err) {
      console.warn("[WorkerDownload] Could not fetch base worker.js:", err);
    }
    const js = customizeWorkerJs(baseWorkerJs, spots);
    const blob = new Blob([js], { type: "application/javascript" });
    this._triggerDownload(blob, "worker.js");
    this.showToast("⬇ Downloading Custom Surf Telemetry worker.js...");
  }

  downloadBuildGuideMarkdown() {
    const spots = buildClockwiseSpots(this.state.beaches, this.state.activeRegion);
    const colorObjs = {
      bezel: this._getSwatchObj("bezel", this.state.colors.bezel),
      dial: this._getSwatchObj("dial", this.state.colors.dial),
      inlay: this._getSwatchObj("inlay", this.state.colors.inlay),
      hands: this._getSwatchObj("hands", this.state.colors.hands),
      deck: this._getSwatchObj("deck", this.state.colors.deck),
    };
    const md = generateBuildGuideMarkdown({
      region: this.state.activeRegion,
      spots,
      colors: colorObjs,
    });
    const blob = new Blob([md], { type: "text/markdown" });
    this._triggerDownload(blob, "BUILD_AND_BOM_GUIDE.md");
    this.showToast("⬇ Downloading Custom Build & BOM Guide...");
  }

  _triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 250);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.surfClockApp = new SurfClockConfiguratorApp();
});
