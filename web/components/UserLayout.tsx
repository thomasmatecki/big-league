import { Box, Anchor, Header, Nav, Avatar } from "grommet";
import Link from "next/link";
import Head from "next/head";

type LayoutProps = {
  children: React.ReactNode;
};

const AppBar = () => (
  <Header direction="row" justify="between" pad="small" background="light-2">
    <Nav align="center" direction="row">
      <Avatar
        src="//s.gravatar.com/avatar/b7fb138d53ba0f573212ccce38a7c43b?s=80"
        round="small"
        align="center"
        flex={false}
        justify="center"
      />
      <Link href="/home">
        <Anchor>Home</Anchor>
      </Link>
      <Link href="/profile">
        <Anchor>Profile</Anchor>
      </Link>
      <Link href="/schedule">
        <Anchor>Schedule</Anchor>
      </Link>
    </Nav>
    <Anchor href="/api/logout" label="Logout"></Anchor>
  </Header>
);

const UserLayout = ({ children }: LayoutProps): JSX.Element => {
  return (
    <Box>
      <Head>
        <meta property="og:title" content="My new title" key="title" />
      </Head>
      <AppBar></AppBar>
      <main>{children}</main>
    </Box>
  );
};

export default UserLayout;
