import { Achievement, Home, Logout, Plan, User } from "grommet-icons";
import Link from "next/link";
import { Anchor, Avatar, Box, Header, Nav } from "../components/lib";

type LayoutProps = {
  children: React.ReactNode;
};

const AppBar = () => (
  <Header direction="row" justify="between" pad="small" background="light-2">
    <Nav align="center" direction="row">
      <Avatar
        src="//s.gravatar.com/avatar/b7fb138d53ba0f573212ccce38a7c43b?s=80"
        round="small"
      />
      <Link href="/home">
        <Anchor label="Home" icon={<Home></Home>} />
      </Link>
      <Link href="/profile">
        <Anchor label="Profile" icon={<User></User>} />
      </Link>
      <Link href="/schedule">
        <Anchor label="Schedule" icon={<Plan></Plan>} />
      </Link>
      <Link href="/standings">
        <Anchor label="Standings" icon={<Achievement></Achievement>} />
      </Link>
    </Nav>
    <Anchor href="/api/logout" label="Logout" icon={<Logout></Logout>} />
  </Header>
);

const UserLayout = ({ children }: LayoutProps): JSX.Element => {
  return (
    <Box fill>
      <AppBar></AppBar>
      {children}
    </Box>
  );
};

export default UserLayout;
