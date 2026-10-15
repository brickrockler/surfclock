with open("shared_assets/shared_ui.css", "r", encoding="utf-8") as f:
    css = f.read()

old_toolbar_css = """/* 3. Persistent Edge-to-Edge Bottom Floating Archiving Toolbar Across All Views */
.mopt-bottom-archiving-toolbar {
  position: fixed !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  z-index: 99995 !important;
  background: rgba(255, 255, 255, 0.50) !important;
  backdrop-filter: blur(20px) saturate(135%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(135%) !important;
  border-top: 1px solid rgba(0, 0, 0, 0.16) !important;
  padding: 7px 16px !important;
  box-sizing: border-box !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 10px !important;
  overflow-x: auto !important;
  scrollbar-width: none !important;
}

.mopt-bottom-archiving-toolbar::-webkit-scrollbar {
  display: none;
}

.mopt-bottom-archiving-toolbar #mopt-top-sorting-dynamics {
  position: static !important;
  top: auto !important;
  left: auto !important;
  right: auto !important;
  transform: none !important;
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: nowrap !important;
  gap: 12px !important;
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sorting-cluster {
  display: inline-flex !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
  gap: 5px !important;
  white-space: nowrap !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sort-label {
  font-family: 'Google Sans Code', monospace !important;
  font-size: 9.5px !important;
  font-weight: 700 !important;
  color: #000000 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sort-select,
.mopt-bottom-archiving-toolbar .mopt-top-filter-pill,
.mopt-bottom-archiving-toolbar #mopt-open-tag-nav-btn,
.mopt-bottom-archiving-toolbar .desktop-color-mode-btn {
  font-family: 'Google Sans Code', monospace !important;
  font-size: 10px !important;
  font-weight: 600 !important;
  color: #000000 !important;
  background: rgba(255, 255, 255, 0.52) !important;
  border: 1px solid rgba(0, 0, 0, 0.18) !important;
  border-radius: 999px !important;
  padding: 4px 9px !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
  height: 25px !important;
  box-sizing: border-box !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-filter-pill.active,
.mopt-bottom-archiving-toolbar .desktop-color-mode-btn.active {
  background: #000000 !important;
  color: #FFFFFF !important;
  border-color: #000000 !important;
}"""

new_toolbar_css = """/* 3. Persistent Edge-to-Edge Swiss Architectural Grid Footer Bar Across All Pages (note_1791900165764_3d6z) */
.mopt-bottom-archiving-toolbar {
  position: fixed !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 36px !important;
  min-height: 36px !important;
  z-index: 99995 !important;
  background: #ECECE7 !important;
  border-top: 1px solid rgba(18, 18, 16, 0.28) !important;
  border-bottom: 1px solid rgba(18, 18, 16, 0.28) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  display: flex !important;
  align-items: stretch !important;
  justify-content: stretch !important;
  gap: 0 !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  scrollbar-width: none !important;
  font-family: 'Google Sans Code', monospace !important;
}

.mopt-bottom-archiving-toolbar::-webkit-scrollbar {
  display: none;
}

.mopt-bottom-archiving-toolbar #mopt-top-sorting-dynamics {
  position: static !important;
  top: auto !important;
  left: auto !important;
  right: auto !important;
  transform: none !important;
  width: 100% !important;
  height: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  display: flex !important;
  align-items: stretch !important;
  justify-content: stretch !important;
  flex-wrap: nowrap !important;
  gap: 0 !important;
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sorting-cluster,
.mopt-bottom-archiving-toolbar #desktop-color-mode-bar.in-bottom-bar {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  flex-wrap: nowrap !important;
  flex: 1 0 auto !important;
  height: 100% !important;
  padding: 0 18px !important;
  margin: 0 !important;
  gap: 8px !important;
  background: transparent !important;
  border: none !important;
  border-right: 1px solid rgba(18, 18, 16, 0.28) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  white-space: nowrap !important;
  box-sizing: border-box !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sorting-cluster:last-child,
.mopt-bottom-archiving-toolbar #desktop-color-mode-bar.in-bottom-bar:last-child {
  border-right: none !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sort-label {
  font-family: 'Google Sans Code', monospace !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  color: #121210 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  padding: 0 !important;
}

/* Rectangular Swiss buttons & dropdowns inside the footer (matching note_1791900165764_3d6z_ref_4.jpg) */
.mopt-bottom-archiving-toolbar .mopt-top-sort-select,
.mopt-bottom-archiving-toolbar .mopt-top-filter-pill,
.mopt-bottom-archiving-toolbar #mopt-open-tag-nav-btn,
.mopt-bottom-archiving-toolbar .desktop-color-mode-btn {
  font-family: 'Google Sans Code', monospace !important;
  font-size: 0.66rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  color: #121210 !important;
  background: transparent !important;
  border: 1px solid rgba(18, 18, 16, 0.42) !important;
  border-radius: 0px !important;
  box-shadow: none !important;
  padding: 0 10px !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 5px !important;
  height: 23px !important;
  box-sizing: border-box !important;
  transition: background-color 0.14s ease, color 0.14s ease, border-color 0.14s ease !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-sort-select:hover,
.mopt-bottom-archiving-toolbar .mopt-top-filter-pill:hover,
.mopt-bottom-archiving-toolbar #mopt-open-tag-nav-btn:hover,
.mopt-bottom-archiving-toolbar .desktop-color-mode-btn:hover {
  background: rgba(18, 18, 16, 0.08) !important;
  border-color: #121210 !important;
}

.mopt-bottom-archiving-toolbar .mopt-top-filter-pill.active,
.mopt-bottom-archiving-toolbar .desktop-color-mode-btn.active {
  background: #121210 !important;
  color: #ECECE7 !important;
  border-color: #121210 !important;
  font-weight: 700 !important;
}"""

assert old_toolbar_css in css, "old_toolbar_css not found"
css = css.replace(old_toolbar_css, new_toolbar_css, 1)

with open("shared_assets/shared_ui.css", "w", encoding="utf-8") as f:
    f.write(css)

print("Successfully patched shared_assets/shared_ui.css!")
