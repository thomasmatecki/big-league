import router from "next/router";
import { head, map } from "ramda";
import { useState } from "react";
import {
  Box,
  Button,
  Form,
  FormField,
  Text,
  TextInput,
} from "../components/lib";
import { userApi } from "../lib/sdk";

const RegistrationFrom = () => {
  const [value, setValue] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  return (
    <Box align="start" justify="center">
      <Box
        align="center"
        justify="start"
        direction="row"
        gap="xsmall"
        margin={{ bottom: "large" }}
        pad={{ horizontal: "xsmall" }}
      >
        <Text color="text-strong" size="large">
          Welcome.
        </Text>
        <Text color="text-xweak" size="large">
          We're glad you're here.
        </Text>
      </Box>

      <Form
        value={value}
        errors={errors}
        onChange={(nextValue) => setValue(nextValue)}
        onSubmit={({ value }) => {
          userApi
            .createProfile(value)
            .then((_ok) => {
              router.push("/home");
            })
            .catch(({ response }) => {
              const singleErrors = map(head, response.data);
              setErrors(singleErrors);
            });
        }}
      >
        <Box direction="row-responsive" gap="small">
          <FormField
            name="first_name"
            htmlFor="first-name-input-id"
            label="First Name"
            required
          >
            <TextInput id="first-name-input-id" name="first_name" />
          </FormField>

          <FormField
            name="last_name"
            htmlFor="last-name-input-id"
            label="Last Name"
            required
          >
            <TextInput id="last-name-input-id" name="last_name" />
          </FormField>
        </Box>

        <FormField
          name="email"
          htmlFor="email-input-id"
          label="Email Address"
          required
        >
          <TextInput id="email-input-id" name="email" />
        </FormField>

        <FormField
          name="password"
          htmlFor="password-input-id"
          label="Password"
          required
        >
          <TextInput id="password-input-id" name="password" type="password" />
        </FormField>

        <Button type="submit" primary label="Submit" />
      </Form>
    </Box>
  );
};

export default RegistrationFrom;
