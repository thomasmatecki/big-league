import UserLayout from "../components/UserLayout";
import { Profile, UserApi } from "../gen/sdk";
import { withUserApi } from "../lib/session";

interface HomeProps {
  profile: Profile;
}

export const getServerSideProps = withUserApi(
  async ({ userApi }: { userApi: UserApi }) => {
    const { data: profile } = await userApi.retrieveProfile();

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
