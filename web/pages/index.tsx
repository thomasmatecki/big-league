import Router from "next/router";
import { useEffect } from "react";
import { GetServerSidePropsContext } from "next";

import { withSession, WithSessionRequest } from "../lib/session";

interface PageProps {
  loggedIn: boolean;
}

export const getServerSideProps = withSession(
  async ({ req }: GetServerSidePropsContext & WithSessionRequest) => {
    const auth = req.session.get("auth");

    const props: PageProps = {
      loggedIn: Boolean(auth),
    };

    return { props };
  }
);

function IndexPage({ loggedIn }: PageProps) {
  useEffect(() => {
    if (loggedIn) {
      Router.push("/home");
    }
  });

  return (
    <div>
      <h1>hello Public</h1>
      <a href="/api/login">Login</a>
    </div>
  );
}
export default IndexPage;
