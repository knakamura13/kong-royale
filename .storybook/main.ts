import type { StorybookConfig } from "@storybook/html-vite";

const config: StorybookConfig = {
  framework: "@storybook/html-vite",
  stories: ["../client/src/**/*.stories.@(js|ts)"],
  staticDirs: ["../public"],
};

export default config;
