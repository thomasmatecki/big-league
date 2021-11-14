import RosterTable, { Props } from "../components/RosterTable";
import { ComponentMeta, ComponentStory } from "@storybook/react";

export default {
  title: "RosterTable",
  component: RosterTable,
} as ComponentMeta<typeof RosterTable>;

const Template: ComponentStory<typeof RosterTable> = (args: any) => (
  <RosterTable {...args} />
);

export const Story = Template.bind({});

Story.args = {
  attendance: [
    {
      display_name: "Thomas M.",
      attending: true,
      record: "12-2-3",
    },
    {
      display_name: "Isaac H.",
      attending: true,
      record: "2-3-12",
    },
    {
      display_name: "Alek h.",
      attending: true,
      record: "3-2-12",
    },
  ],
};
