import type { Meta, StoryObj } from "@storybook/html-vite";
import { createControlsGuide } from "./onboarding";

interface GuideArgs { practiceMode: boolean }

const meta = {
  title: "Game UI/Controls guide",
  args: { practiceMode: false as boolean },
  argTypes: { practiceMode: { control: "boolean", description: "Show the firing-range action." } },
  render: ({ practiceMode }: GuideArgs) => {
    const guide = createControlsGuide(undefined, practiceMode ? () => alert("Firing range is not part of this isolated preview.") : undefined);
    guide.open();
    return guide.el;
  },
} satisfies Meta<GuideArgs>;

export default meta;
type Story = StoryObj<GuideArgs>;

export const Default: Story = {};
export const WithFiringRangeAction: Story = { args: { practiceMode: true } };
