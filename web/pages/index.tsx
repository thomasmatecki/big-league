import Router from "next/router";
import { Anchor, Box, Spinner } from "../components/lib";
import { useEffect } from "react";
import { GetServerSidePropsContext } from "next";
import Link from "next/link";
import { withSession, HasSessionRequest } from "../lib/session";
interface PageProps {
  loggedIn: boolean;
}

export const getServerSideProps = withSession(
  async ({ req }: GetServerSidePropsContext) => {
    const auth = req.session.get("auth");

    const props: PageProps = {
      loggedIn: Boolean(auth),
    };

    return { props };
  }
);

function IndexPage({ loggedIn }: PageProps) {
  if (loggedIn) {
    useEffect(() => {
      Router.push("/home");
    });
    return (
      <Box
        animation="fadeOut"
        fill="vertical"
        overflow="auto"
        align="center"
        flex="grow"
        justify="center"
        direction="column"
      >
        <Spinner size="xlarge"></Spinner>
      </Box>
    );
  } else {
    return (
      <div>
        <h1>hello Public</h1>
        <Link href="/login">
          <Anchor>Login</Anchor>
        </Link>
      </div>
    );
  }
}
export default IndexPage;
