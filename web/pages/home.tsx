
import { Box } from 'grommet';
import { GetServerSidePropsContext } from "next";
import { withSession, WithSessionRequest } from "../lib/session";
interface HomeProps { }

export const getServerSideProps = withSession(
  async ({ req, res }: GetServerSidePropsContext & WithSessionRequest) => {
    const auth = req.session.get("auth");

    if (!auth) {
      return {
        redirect: {
          destination: "/api/login",
          permanent: false,
        },
      };
    }

    const props: HomeProps = { };
    return { props: props };

  }
);


const AppBar = (props: any) => (
  <Box
    tag='header'
    direction='row'
    align='center'
    justify='between'
    background='light-2'
    pad={{ vertical: 'small', horizontal: 'medium' }}
    elevation='medium'
    {...props}
  />
);

const HomePage = () => {
  return (
    <AppBar>
      Welcome Home
      <Box direction='row'>
      </Box>
    </AppBar>
  );
};

export default HomePage;
