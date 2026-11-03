import { injectToon } from "../client/src/ui/toon";

injectToon();

const style = document.createElement("style");
style.textContent = `html, body, #storybook-root { min-height: 100%; margin: 0; } body { background: #071422; }`;
document.head.append(style);
