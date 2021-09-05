import { GetServerSidePropsContext } from "next";
import { WithAPISession, HasAPISessionRequest } from "../lib/session";
import UserLayout from "../components/UserLayout";
import { Profile } from "../gen/sdk";

interface ProfileProps {
  profile: Profile;
}

export const getServerSideProps = WithAPISession(
  async ({ req }: HasAPISessionRequest<GetServerSidePropsContext>) => {
    const { data: profile } = await req.profileApi.retrieveProfile();
    debugger;

    return {
      props: {
        profile: profile,
      },
    };
  }
);

const ProfilePage = (props: ProfileProps) => {
  return (
    <UserLayout>
      <h3>Profile</h3>
    </UserLayout>
  );
};

export default ProfilePage;
