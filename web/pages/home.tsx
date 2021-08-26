import { useRouter } from "next/router";
import { useEffect } from "react";
import { GetServerSidePropsContext } from "next";
import { withSession, WithSessionRequest } from "../lib/session";
interface HomeProps {}

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

    const props: HomeProps = {};
    return { props: props };
  }
);

const HomePage = () => {
  return (
    <div>
    <div>
      <h1>Welcome Home</h1>
    </div>
    <a href="api/logout">Logout</a>
    </div>
  );
};

export default HomePage;
