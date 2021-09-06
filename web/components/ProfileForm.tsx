import { Avatar, FileInput, Select, TextArea } from "grommet";
import { useState } from "react";
import { Profile } from "../gen/sdk";
import { Box, Button, Form, FormField, Text, TextInput } from "./lib";

type Props = {
  profile: Profile;
};

const ProfileForm = (props: Props) => {
  const [value, setValue] = useState<Profile>(props.profile);
  const [fieldErrors, setFieldErrors] = useState({});
  const [formErrors, setFormErrors] = useState([]);
  const [blocked, setBlocked] = useState(false);

  return (
    <Box width="large">
      <Form<Profile>
        value={value}
        errors={fieldErrors}
        onChange={setValue}
        onSubmit={({ value }) => {
          setBlocked(true);
        }}
      >
        <Box direction="row-responsive" gap="small">
          <Box width="medium">
            <FormField
              name="display_name"
              htmlFor="display-name-input-id"
              label="Display Name"
              required
            >
              <TextInput
                id="display-name-input-id"
                name="display_name"
                placeholder="What should we call you?"
              />
            </FormField>

            <FormField label="Interest">
              <Select
                id="interest-select-id"
                name="interest-select"
                placeholder="Why do you do it?"
                value={value}
                options={["Social", "Fitness", "Competition"]}
                onChange={({ option }) => setValue(option)}
              />
            </FormField>
            <FormField name="biography" label="Bio">
              <TextArea
                placeholder="Say something about yourself"
                resize={false}
              ></TextArea>
            </FormField>
          </Box>
          <Box align="center" gap="small">
            <Avatar background="dark-2" size="5xl"></Avatar>
            <FormField>
              <FileInput
                messages={{
                  dropPrompt: "Upload a picture",
                }}
              />
            </FormField>
          </Box>
        </Box>
        <Button type="submit" disabled={blocked} primary label="Save" />
        <Box pad="small">
          {formErrors.map((error, idx, _errors) => (
            <Text key={idx} color="status-error">
              {error}
            </Text>
          ))}
        </Box>
      </Form>
    </Box>
  );
};

export default ProfileForm;