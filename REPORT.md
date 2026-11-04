# Kong Royale UI scaling/accessibility spike — evidence and recommendations

Baseline: fork commit `82beb27ac3446025cc705cb669aafc6ab63993f9`, 2026-11-03. Local Vite port 5320, Chrome on macOS, DPR 1, normal zoom. No product code changed. This is a baseline investigation, not a WCAG conformance certification.

## Findings

1. **Confirmed readability problem, high priority:** the lobby scales all typography with `min(height/1080, width/1920)`. There is no floor in the shared Toon canvas. At 1280×720, navigation is 12 CSS px, Edit callsign 10 px, Learn controls 10.67 px. At 567×948 these become 5.32, 4.43, and 4.73 px. This reproduces the reported narrow-window problem and confirms small text on ordinary laptop viewports. Small font size alone is not a WCAG failure.
2. **Confirmed narrow difficulty-target spacing failure; other undersized controls need individual classification:** at 567×948 the navigation targets are approximately 15.9 px tall, callsign 14.7, difficulty 12.8, Learn controls 15.6, and primary Play 23.6. A constructor fixture with the production CSS at 567×948 shows the 24 px circles around Easy and Hard intersect Standard’s target rectangle. No alternative difficulty control was identified in the lobby. Other measured fixture targets did not intersect the tested circles. Do not classify every small control as a 2.5.8 failure: the spacing and equivalent-control exceptions must be checked. Laptop controls sampled at 1280×720 are mostly above 24 px; this is not a blanket desktop target-size failure.
3. **Resize-text problem, high priority:** in native Chrome at 200% browser zoom, lobby heading, navigation and action labels remained visually essentially the same size as at 100%. Viewport-proportional sizing can cancel zoom because zoom reduces the CSS viewport. Settings' Menu text size is capped at 150% and applies through its local `--ts`; it is not a global 200% text enlargement mechanism. Other browsers and text-only resizing remain untested; this observation alone does not establish a definitive 1.4.4 failure.
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
|Lobby, primary actions|Four live viewports and bounds; native Chrome 100% and 200% zoom; difficulty target spacing fixture|Other browsers and text-only resize; remaining target exceptions, spacing and keyboard paths|
|Training|Live 1366×768 screenshot/DOM|Narrow layout, text resizing|
|Controls guide|Live 1366×768; sampled Tab loop and Escape focus restoration|All lesson content at narrow/200%; broader focus visibility and occlusion|
|Settings: mouse, controller, audio, video, accessibility|Category captures at 1366×768; all 13 subsections at 1280×720 (100% text) and 567×948 (150% text), maximum-text captures, and sampled keyboard navigation|Restore dialog, comprehensive keyboard/focus checks, and native browser zoom|
|Loading/boot/error cards|Source floors and responsive rules; transitional live capture|Controlled error/loading states, smallest widths|
|Callsign, friends, private/event lobby|Live callsign and Friends popovers, empty-name error, local two-session private-room invitation/join/leave, nonexistent invite and simulated private disconnect; local event join and simulated room reconnect|Real network failures, event match reconnect, additional viewport/keyboard/focus paths and validation variants|
|Firing range HUD and pause|Live screenshots/DOM at 1366×768|Dynamic rack labels, analytics, key operation, narrow window|
|Inventory, shop, results|Actual constructors with synthetic data at 1280×720 (`fixture-*`); live populated range inventory; sampled empty-slot selection, Escape and occupied-item keyboard move|Other inventory flows, real shop interaction/network state and victory/squad results|
|HUD: vitals, ammo, hotbar, compass, prompts, notifications|Shared scaling source and live firing-range baseline|Full battle states, storm, downed/revive, vehicle/swimming/flight, damage/medals, variable backgrounds|
|Map/minimap/player/item labels|Live range map; sampled M/Escape; source inventory and canvas text paths|Canvas text size/contrast in representative scenes; map pointer controls and broader keyboard checks|
|Spectator/player list|Synthetic constructor fixture at 1280×720, including arrow and player-row bounds; source scaling declarations|Real spectator transition, navigation and player-list focus|
|Personal bests, bug reporting, fullscreen, voice, caster|Live bug-report overlay capture; source inventory|Dialog dismissal and full runtime paths and errors|

Expanded settings evidence is in `expanded-states.json`; the narrow pass inherited the 150% text preference from the preceding maximum-text capture. Its run stopped at a callsign locator mismatch after completing all Settings captures; no later actions from that script are claimed.

The unverified cells are material limitations. This baseline cannot establish that all interfaces meet AA, and does not yet satisfy an exhaustive runtime audit of every menu/overlay/label.

## Minimal-change recommendation

1. Prototype lobby/menu text and control sizing independently from the 1920×1080 decorative canvas. Keep existing palette/art and layout at comfortable widths. Set a product readability target (for discussion: 14 px support text, 16 px primary control text), explicitly not a WCAG-mandated font floor.
2. At the width where readable controls stop fitting, wrap the small action groups and allow menu-panel scrolling. Do not clamp the entire canvas: that can move controls offscreen. Extend existing Settings reflow patterns where useful.
3. Make clickable areas at least 24×24 CSS px where feasible; preserve visual button sizes using padding only when neighboring hit areas do not overlap. Validate spacing exceptions before filing violations.
4. Make a text enlargement mechanism work through 200%, including controls, with no loss of function. Extend the native Chrome zoom observation to other paths and text-only resizing; do not use pinch-zoom or a mere viewport resize as equivalent evidence.
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

Scripts are preserved under `scripts/`. Run with `NODE_PATH` pointing at the checkout node_modules. Most use a local Vite server on port 5320 and write to the audit output directory; multiplayer scripts require a local game server with Vite proxying to that server. The event reconnect script starts and stops its own isolated local server on 3032 and Vite on 5321, and refuses to run if either port is occupied. Main-game scripts require hardware Chrome/Metal and can take several minutes to boot. `audit-fixture` and `audit-panels` abort the game bootstrap and render actual constructors with synthetic data. Only `audit-final` produced the final lobby matrix. Earlier scripts are retained to explain evidence provenance.

## Additional live coverage

`additional-states.json` and corresponding screenshots add callsign popover, empty-name validation error, Friends popover, populated firing-range inventory, map and bug-report overlay. No report was submitted. The final `pause-later` capture still shows the bug overlay: the attempted Escape sequence does not establish successful dismissal. These runs establish presentation evidence, not full keyboard conformance. At the time of those captures, multiplayer roster/error states and real spectator transitions were unverified; the subsequent two-player run below covers one roster path.

## Actual Chrome zoom and keyboard verification

Native Chrome on macOS was opened in a dedicated local-game tab. The browser menu showed 100%; Command+= raised it through 110/125/150/175 to 200%, with the native accessibility tree reporting `Zoom: 200%` and the browser screenshot displaying 200%. The lobby heading, navigation and action labels remained essentially the same visual size at 100% and 200%, confirming cancellation of browser enlargement in this path. It does not establish every browser/text-only resizing result. Zoom was restored to 100% and the audit tab closed. Screenshots were inspected in the native tool conversation; no unrelated browser content is included in the published evidence files.

`keyboard.json` records actual key traversal: guide Tab cycles across station/action buttons and wraps, Escape returns focus to Learn controls; Settings arrows move/select and adjust, Tab changes subsection, Escape restores the Settings button. Inventory/map key sequences were also recorded. This is a sampled path, not exhaustive keyboard certification. `zoom-probe.json` explicitly records a separate pinch-scale experiment and must not be used as browser-zoom evidence.

## Additional runtime probes

At 1366×768, two isolated Chrome sessions used the local server and same-origin Vite proxy. The invited guest joined the host, both room views displayed two players, and the host returned to one after the guest left. See `two-player-states.json` and `two-player-*.png`; the snapshots record no `window.__kr.errors`. This is a real local roster path, not a test of reconnect, gameplay, or accessibility conformance. The live status line still displayed one online player in the two-player snapshot; no conclusion about its accuracy or update timing is drawn from this capture.

A user-style override applied `line-height: 1.5`, `letter-spacing: .12em`, `word-spacing: .16em` and paragraph bottom margin `2em` to the lobby. At 1280×720, the Firing Range and Learn Controls buttons initially extended to y=727.6, about 7.6 CSS px below the viewport; baseline buttons were within it. Focusing Learn Controls and invoking `scrollIntoView` moved its bounds to y=685.0–719.6. This demonstrates a layout sensitivity but does not establish loss of content or function, keyboard-only discoverability, or a WCAG failure. At 567×948 no sampled button bounds exceeded the viewport. Screenshots and button measurements are in `text-spacing-*.png` and `text-spacing.json`; this is one injected-style probe of the lobby, not exhaustive text-spacing, other-screen, or browser testing.

### Local connection and event-room probes

With a local private server and Vite proxy at 1366×768, joining nonexistent invite `ZZZZ` displayed “NO SUCH LOBBY” in an element with `role="alert"` (11.38 CSS px computed font); the browser reported no `window.__kr.errors`. Closing the private room’s game WebSocket with a scripted close code and reason returned to the home lobby and rendered the **test-supplied** reason in an alert. The wording was supplied by the probe, not observed from an actual network outage. `network-error-states.json` and `network-error-*.png` record the states. An earlier attempt also closed Vite’s development socket and reloaded the page; those observations were discarded and are not the published captures.

An isolated local event used an ephemeral administrator credential to create a solo event. After joining as AUDIT, the probe closed only the game WebSocket and temporarily closed new game sockets as they opened. The room displayed “Connection lost. Reconnecting…” in `role="status"`; after the probe stopped interrupting connections, it returned to “Waiting for the host to start.” Four primary game sockets were constructed over the final run; the screenshots and snapshots record no `window.__kr.errors`. See `event-reconnect-states.json` and `event-reconnect-*.png`. At 1366×768, one Tab from the focused name field moved focus to Join Game and its focus outline was visible in the captured frame. At 567×948, the event join screen showed Settings at 5.32 px and the name input at 8.86 px; Settings was 45.14×15.88 px, the input 151.19×20.08 px and Join Game 151.19×23.63 px. These are readability and target-size concerns; spacing and other exceptions were not assessed. This tests a short scripted room interruption at 1366×768 and one join-screen focus transition, not an actual network outage, in-match reconnection, timeout/give-up, screen-reader announcement, or a conformance verdict.

## Final spike assessment

The investigation deliverables are available: source inventory with explicit runtime coverage, a four-viewport measurement matrix, screenshot evidence, classified findings, minimal-change recommendations, and actionable follow-ups (#2–#5). This completes the baseline spike deliverables while leaving the broader conformance audit and remediation open in those follow-ups. It is not a claim that every dynamic state was exercised or that the game meets AA.

A local server on 127.0.0.1:3031 (event mode off, admin disabled) exercised private-room creation and leaving (`multiplayer-states.json`, `private-room.png`, `private-left.png`). The `SERVER OFFLINE` banner in those captures came from the cross-origin health request associated with the direct `?ws=` override; it does not by itself establish the WebSocket connection failed. A subsequent two-session run used Vite with `KR_PORT=3031` and the same-origin proxy: the guest opened an invite, both clients displayed two players, and the host displayed one after the guest left (`two-player-states.json`, `two-player-*.png`). It captures a real local room path, not reconnect, error, match start, keyboard, or a complete accessibility assessment. A production spectator/player-list constructor was rendered with synthetic state (`spectator.json`, `fixture-spectator.png`); at 1280×720, arrow targets measured 46×81.34 px and the selectable player row 236.67×25 px. Real spectator transitions remain follow-up coverage.

Inventory keyboard verification selected empty slot 2 and dismissed with Escape; map opened with M and dismissed with Escape. A later firing-range run opened the populated inventory, pressed R on the Bunchgun in slot 1, then 2. The visible cards and `window.__kr.game.state()` both showed it move to slot 2 (`inventory-move-states.json`, `inventory-move-*.png`); this does not verify other inventory operations or multiplayer behavior.

Recommended order: #4 text-resizing remediation/proof, #2 bounded lobby sizing prototype, #3 difficulty targets (coordinate with #2), and #5 remaining dynamic-state coverage. Preserve passing text colors and existing Settings reflow. Review visual proposals before product changes; upstream PRs remain Draft pending Kyle's sign-off.
