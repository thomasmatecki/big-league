import { Form, FormField, TextInput, Button, Box, Text } from "./lib";
import { useState } from "react";
import axios from "axios";

import { restApi } from "../lib/sdk";
import oauth from "../lib/oauth";

import { map, head, propOr } from "ramda";
import router from "next/router";
import { Session } from "../gen/sdk";

const LoginForm = () => {
  const [value, setValue] = useState<Session>({
    username: "",
    password: "",
  });

  const [fieldErrors, setFieldErrors] = useState({});
  const [formErrors, setFormErrors] = useState([]);
  const [blocked, setBlocked] = useState(false);

  return (
    <Box width="medium">
      <Form
        value={value}
        errors={fieldErrors}
        onChange={(nextValue) => setValue(nextValue)}
        onSubmit={({ value }) => {
          setBlocked(true);

          restApi
            .createSession(value, { withCredentials: true })
            .then((_ok) => {
              axios.get(oauth.authorize_url, { withCredentials: true });
            })
            .then((_ok) => {
              router.push("/home");
            })
            .catch(({ response }) => {
              setFieldErrors(map(head, response.data));
              setFormErrors(propOr([], "__all__")(response.data));
              setBlocked(false);
            });
        }}
      >
        <FormField
          name="username"
          htmlFor="username-input-id"
          label="Email Address"
          required
        >
          <TextInput id="username-input-id" name="username" />
        </FormField>

        <FormField
          name="password"
          htmlFor="password-input-id"
          label="Password"
          required
        >
          <TextInput id="password-input-id" name="password" type="password" />
        </FormField>

        <Button type="submit" disabled={blocked} primary label="Log in" />

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

export default LoginForm;