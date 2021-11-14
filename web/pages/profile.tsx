import { Box } from "grommet";
import ProfileForm from "../components/ProfileForm";
import UserLayout from "../components/UserLayout";
import { Profile, UserApi } from "../gen/sdk";
import { withUserApi } from "../lib/session";

interface ProfileProps {
  profile: Profile;
  userApi: UserApi;
}

export const getServerSideProps = withUserApi(async ({ userApi }: any) => {
  const { data: profile } = await userApi.retrieveProfile();

  return {
    props: {
      profile: profile,
    },
  };
});

const ProfilePage = ({ profile }: ProfileProps) => {
  return (
    <UserLayout>
      <Box align="center" justify="center" pad="large">
        <ProfileForm profile={profile}></ProfileForm>
      </Box>
    </UserLayout>
  );
};

export default ProfilePage;
