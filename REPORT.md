# Kong Royale UI scaling/accessibility spike — evidence and recommendations

Baseline: fork commit `82beb27ac3446025cc705cb669aafc6ab63993f9`, 2026-11-03. Local Vite port 5320, Chrome on macOS, DPR 1, normal zoom. No product code changed. This is a baseline investigation, not a WCAG conformance certification.

## Findings

1. **Confirmed readability problem, high priority:** the lobby scales all typography with `min(height/1080, width/1920)`. There is no floor in the shared Toon canvas. At 1280×720, navigation is 12 CSS px, Edit callsign 10 px, Learn controls 10.67 px. At 567×948 these become 5.32, 4.43, and 4.73 px. This reproduces the reported narrow-window problem and confirms small text on ordinary laptop viewports. Small font size alone is not a WCAG failure.
2. **Confirmed narrow difficulty-target spacing failure; other undersized controls need individual classification:** at 567×948 the navigation targets are approximately 15.9 px tall, callsign 14.7, difficulty 12.8, Learn controls 15.6, and primary Play 23.6. A constructor fixture with the production CSS at 567×948 shows the 24 px circles around Easy and Hard intersect Standard’s target rectangle. No alternative difficulty control was identified in the lobby. Other measured fixture targets did not intersect the tested circles. Do not classify every small control as a 2.5.8 failure: the spacing and equivalent-control exceptions must be checked. Laptop controls sampled at 1280×720 are mostly above 24 px; this is not a blanket desktop target-size failure.
3. **Resize-text risk, high priority:** viewport-proportional font dimensions can cancel browser zoom because zoom reduces the CSS viewport. The formula predicts cancellation until a floor or breakpoint intervenes. Settings' Menu text size is capped at 150% and applies through its local `--ts`; it is not a global 200% text enlargement mechanism. Actual browser zoom and text-only resizing have not been tested, so a definitive 1.4.4 failure is not claimed.
4. **Existing protections should be preserved:** loading uses a 0.5 px canvas-unit floor and several explicit 11–13 px text floors. Settings supports larger text, wrapping, and stacked help at larger text settings; narrow aspect ratios use width/1180. Guide has Escape, Tab wrapping, initial focus, and focus restoration. Inventory already has keyboard commands and click alternatives to dragging; absence of native buttons alone does not establish keyboard failure.
5. **No justification for a global palette change:** opaque Toon text on #12344B measures #FFF8E7 12.25:1, #A9C6DA 7.28:1, #7FA3BC 4.86:1. Dark text on yellow is 13.24:1. These pairs meet normal-text contrast. Rule colors #1D4763 and #2A5C7C against #0E2A3D measure 1.51:1 and 2.06:1; only essential boundaries/state cues need 3:1. Background compositing, opacity, and imagery require separate assessment.
6. **HUD scale differs from menu scale:** `hudUnit = min(height/1440 * hudScale, width/1500)`. Raising HUD size cannot enlarge beyond the width cap. Inventory uses height/1080 with HUD scale, capped at width/1240; shop uses width/1200. A universal menu-unit fix will not solve every gameplay label.

## Viewport matrix (live lobby)

| CSS viewport | Navigation font | Callsign action font | Learn controls font | Learn controls target height |
|---|---:|---:|---:|---:|
|1440×900|13.5|11.25|12|38.5|
|1366×768|12.8|10.67|11.38|36.7|
|1280×720|12|10|10.67|34.6|
|567×948|5.32|4.43|4.73|15.6|

`measurements.json` contains the underlying DOM sizes and computed colors. These are CSS pixels, not screenshot pixels. The final matrix waits for boot readiness and the loading fade, and filters CSS-hidden controls. `states.json` was captured earlier and its first lobby state still includes the fading loading screen; do not count that temporary duplicate as a permanent lobby control.

## Inventory and coverage

`source-inventory.csv` enumerates UI, settings, caster, bug-report/Kongbot, and voice TypeScript modules, their purpose and sizing/accessibility markers. Counts are discovery aids, not proof of accessible behavior.

| Interface family | Evidence obtained | Remaining verification |
|---|---|---|
|Lobby, primary actions|Four live viewports, rendered bounds, screenshots|Actual zoom, target spacing, keyboard sequence|
|Training|Live 1366×768 screenshot/DOM|Narrow layout, text resizing|
|Controls guide|Live 1366×768; source focus handling|All lesson content at narrow/200%; focus test|
|Settings: mouse, controller, audio, video, accessibility|Live category captures at 1366×768; source scaling and key handling|All 13 subsections additionally captured at 1280×720 (100% text) and 567×948 (150% text), plus maximum-text captures. Restore dialog, keyboard sequence and true zoom remain unverified|
|Loading/boot/error cards|Source floors and responsive rules; transitional live capture|Controlled error/loading states, smallest widths|
|Callsign, friends, private/event lobby|Source/module inventory; source controls|Open popovers, validation errors, multiplayer roster/invite/connection states|
|Firing range HUD and pause|Live screenshots/DOM at 1366×768|Dynamic rack labels, analytics, key operation, narrow window|
|Inventory, shop, results|Actual constructors rendered with synthetic data at 1280×720 (`fixture-*`)|Real interaction and network state, populated inventory, victory/squad results|
|HUD: vitals, ammo, hotbar, compass, prompts, notifications|Shared scaling source and live firing-range baseline|Full battle states, storm, downed/revive, vehicle/swimming/flight, damage/medals, variable backgrounds|
|Map/minimap/player/item labels|Source inventory and canvas text paths|Canvas text size/contrast in representative scenes; map keyboard/pointer controls|
|Spectator/player list|Source inventory and scaling declarations|Real spectator transition, navigation and player-list focus|
|Personal bests, bug reporting, fullscreen, voice, caster|Source inventory|Full runtime paths and their dialogs/errors|

Expanded settings evidence is in `expanded-states.json`; the narrow pass inherited the 150% text preference from the preceding maximum-text capture. Its run stopped at a callsign locator mismatch after completing all Settings captures; no later actions from that script are claimed.

The unverified cells are material limitations. This baseline cannot establish that all interfaces meet AA, and does not yet satisfy an exhaustive runtime audit of every menu/overlay/label.

## Minimal-change recommendation

1. Prototype lobby/menu text and control sizing independently from the 1920×1080 decorative canvas. Keep existing palette/art and layout at comfortable widths. Set a product readability target (for discussion: 14 px support text, 16 px primary control text), explicitly not a WCAG-mandated font floor.
2. At the width where readable controls stop fitting, wrap the small action groups and allow menu-panel scrolling. Do not clamp the entire canvas: that can move controls offscreen. Extend existing Settings reflow patterns where useful.
3. Make clickable areas at least 24×24 CSS px where feasible; preserve visual button sizes using padding only when neighboring hit areas do not overlap. Validate spacing exceptions before filing violations.
4. Make a text enlargement mechanism work through 200%, including controls, with no loss of function. First prove actual browser zoom behavior; don't use pinch-zoom or a mere viewport resize as equivalent evidence.
5. Address HUD/layout caps separately. Use variable-background evidence before adding backing plates, outlines, or color changes. Preserve text pairs that already pass.

## Proposed follow-ups and acceptance criteria

- **Menu sizing prototype:** existing desktop composition preserved; 1280×720 and 567×948 retain readable labels and reachable actions; no overlap or clipping; before/after captures reviewed before upstream submission.
- **Text resizing verification/remediation:** true browser zoom and text-only resizing tested at 100/125/150/200%; measure actual rendered enlargement; all menu content/actions remain available; clarify the scope of Menu text size.
- **Target and keyboard audit:** measure hit rectangles plus neighbor spacing on every state; exercise Tab/arrows/Enter/Escape and focus restoration; classify each exception and fix only confirmed failures.
- **Gameplay and transient-state coverage:** complete the remaining coverage cells above, including multiplayer, spectator, world labels, maps and errors; record screenshots, environment and observed contrast on changing backgrounds.

## References and method limits

- https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- https://www.w3.org/TR/WCAG22/

Graph project points to the primary checkout, generation 2026-11-03T18:27:32Z, a different branch. Exact source in the audited worktree was read for material findings. Coverage reported no recorded gaps for the six core sizing files, which is not proof of exhaustive coverage. No simulated CSS zoom is reported as a real browser zoom test. Synthetic panels are labeled as fixtures and do not prove in-game behavior.

## Reproduction scripts

Scripts are preserved under `scripts/`. Run with `NODE_PATH` pointing at the checkout node_modules. They use the existing local Vite server on port 5320 and write to the recorded absolute audit output directory. Main-game scripts require hardware Chrome/Metal and can take several minutes to boot. `audit-fixture` and `audit-panels` abort the game bootstrap and render actual constructors with synthetic data. Only `audit-final` produced the final lobby matrix. Earlier scripts are retained to explain evidence provenance.

## Additional live coverage

`additional-states.json` and corresponding screenshots add callsign popover, empty-name validation error, Friends popover, populated firing-range inventory, map and bug-report overlay. No report was submitted. The final `pause-later` capture still shows the bug overlay: the attempted Escape sequence does not establish successful dismissal. These runs establish presentation evidence, not full keyboard conformance. Multiplayer roster/error states and real spectator transitions remain unverified.

## Actual Chrome zoom and keyboard verification

Native Chrome on macOS was opened in a dedicated local-game tab. The browser menu showed 100%; Command+= raised it through 110/125/150/175 to 200%, with the native accessibility tree reporting `Zoom: 200%` and the browser screenshot displaying 200%. The lobby heading, navigation and action labels remained essentially the same visual size at 100% and 200%, confirming cancellation of browser enlargement in this path. This supersedes the earlier statement that browser zoom was untested. It does not establish every browser/text-only resizing result. Zoom was restored to 100% and the audit tab closed. Screenshots were inspected in the native tool conversation; no unrelated browser content is included in the published evidence files.

`keyboard.json` records actual key traversal: guide Tab cycles across station/action buttons and wraps, Escape returns focus to Learn controls; Settings arrows move/select and adjust, Tab changes subsection, Escape restores the Settings button. Inventory/map key sequences were also recorded. This is a sampled path, not exhaustive keyboard certification. `zoom-probe.json` explicitly records a separate pinch-scale experiment and must not be used as browser-zoom evidence.

## Final spike assessment

The investigation deliverables are available: source inventory with explicit runtime coverage, a four-viewport measurement matrix, screenshot evidence, classified findings, minimal-change recommendations, and actionable follow-ups (#2–#5). This completes the baseline spike deliverables while leaving the broader conformance audit and remediation open in those follow-ups. It is not a claim that every dynamic state was exercised or that the game meets AA.

A local server on 127.0.0.1:3031 (event mode off, admin disabled) successfully exercised private-room creation and leaving (`multiplayer-states.json`, `private-room.png`, `private-left.png`). This does not verify a second participant or reconnect transition. A production spectator/player-list constructor was rendered with synthetic state (`spectator.json`, `fixture-spectator.png`); at 1280×720, arrow targets measured 46×81.34 px and the selectable player row 236.67×25 px. Real spectator transitions remain follow-up coverage.

Inventory keyboard verification selected empty slot 2 and dismissed with Escape; map opened with M and dismissed with Escape. Pressing R on an empty slot does not prove moving an occupied item, so that operation remains unverified.

Recommended order: #4 text-resizing remediation/proof, #2 bounded lobby sizing prototype, #3 difficulty targets (coordinate with #2), and #5 remaining dynamic-state coverage. Preserve passing text colors and existing Settings reflow. Review visual proposals before product changes; upstream PRs remain Draft pending Kyle's sign-off.
