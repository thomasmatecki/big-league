import { GetServerSidePropsContext } from "next";
import UserLayout from "../components/UserLayout";
import { Profile } from "../gen/sdk";
import { HasAPISessionRequest, WithAPISession } from "../lib/session";

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
