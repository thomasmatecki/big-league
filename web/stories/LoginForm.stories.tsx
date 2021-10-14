import LoginForm from "../components/LoginForm";
import {ComponentMeta , ComponentStory} from '@storybook/react';

export default {
  title: 'Login',
  component: LoginForm,
} as ComponentMeta<typeof LoginForm>;

const Template: ComponentStory<typeof LoginForm> = (args) => <LoginForm {...args} />;

export const Story = Template.bind({});
Story.args = {};