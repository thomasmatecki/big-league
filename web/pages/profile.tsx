import { Box } from "grommet";
import { GetServerSidePropsContext } from "next";
import ProfileForm from "../components/ProfileForm";
import UserLayout from "../components/UserLayout";
import { Profile } from "../gen/sdk";
import { HasAPISessionRequest, WithAPISession } from "../lib/session";

interface ProfileProps {
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

const ProfilePage = (props: ProfileProps) => {
  return (
    <UserLayout>
      <Box align="center" justify="center" pad="large">
        <ProfileForm profile={props.profile}></ProfileForm>
      </Box>
    </UserLayout>
  );
};

export default ProfilePage;
