import router from "next/router";
import { head, map, propOr } from "ramda";
import { useState } from "react";
import { ISession, Session } from "../gen/sdk";
import oauth from "../lib/oauth";
import { userApi } from "../lib/sdk";
import { Box, Button, Form, FormField, Text, TextInput } from "./lib";

interface Props {

};

const LoginForm = ({ }:Props) => {
  const [value, setValue] = useState<ISession>({
    username: "",
    password: "",
  });

  const [fieldErrors, setFieldErrors] = useState({});
  const [formErrors, setFormErrors] = useState([]);
  const [blocked, setBlocked] = useState(false);

  return (
    <Box width="medium">
      <Form<ISession>
        value={value}
        errors={fieldErrors}
        onChange={setValue}
        onSubmit={({ value }) => {
          setBlocked(true);

          userApi
            .updateSession(value, {
              withCredentials: true,
              params: { next: oauth.authorize_url },
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
