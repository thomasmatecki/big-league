import { Box, Anchor, Header, Button, Nav, Avatar } from "../components/lib";
import { GetServerSidePropsContext } from "next";
import { WithAPISession, HasAPISessionRequest } from "../lib/session";
import { Profile } from "../gen/sdk";
import UserLayout from "../components/UserLayout";

interface HomeProps {
  profile: Profile;
}

export const getServerSideProps = WithAPISession(
  async ({ req }: HasAPISessionRequest<GetServerSidePropsContext>) => {
    const { data: profile } = await req.profileApi.retrieveProfile();

    return {
      props: {
        profile: profile,
      },
    };
  }
);

const HomePage = (props: HomeProps) => (
  <UserLayout>
    <h3>Home</h3>
  </UserLayout>
);

export default HomePage;
