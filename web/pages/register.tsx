import { useState } from "react";
import { Box } from "../components/lib";
import RegistrationFrom from "../components/RegistrationForm";

const RegistrationPage = () => {
  const [value, setValue] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  return (
    <Box fill align="center" justify="center">
      <RegistrationFrom></RegistrationFrom>
    </Box>
  );
};

export default RegistrationPage;
