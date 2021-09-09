import { format } from "date-fns";
import { Box, Grid, List, Text } from "grommet";
import UserLayout from "../components/UserLayout";
import { Schedule, UserApi } from "../gen/sdk";
import { withUserApi } from "../lib/session";

type ScheduleResult = {
  next: string;
  previous: string;
  results: Array<Schedule>;
};

interface Props {
  schedule: ScheduleResult;
}

export const getServerSideProps = withUserApi(
  async ({ userApi }: { userApi: UserApi }) => {
    const { data: schedule } = await userApi.listSchedules();

    return {
      props: {
        schedule: schedule,
      },
    };
  }
);

const ScheduleItem = ({ item }: { item: Schedule }) => {
  const date = new Date(item.datetime);
  return (
    <Box fill="horizontal" direction="row" gap="small">
      <Box border={{ side: "left", color: "background-contrast" }} pad="medium">
        <Box>
          <Text weight="bold">{format(date, "dd")}</Text>
        </Box>
        <Box>
          <Text>{format(date, "MMM")}</Text>
        </Box>
      </Box>
      <Box border={{ side: "left", color: "background-contrast" }} pad="medium">
        <Box>
          <Text weight="bold">{format(date, "hh:mm aa")}</Text>
        </Box>
        <Box>
          <Text>{format(date, "EEE")}</Text>
        </Box>
      </Box>
      <Box border={{ side: "left", color: "background-contrast" }} pad="medium">
        <Box>
          <Text weight="bold">{item.opponent.name}</Text>
        </Box>
        <Box direction="row-responsive" justify="between">
          <Box>
            <Text>{item.location}</Text>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

const SchedulePage = (props: Props) => {
  return (
    <UserLayout>
      <Box fill as="main">
        <Grid
          fill
          rows={["xxsmall", "flex", "xsmall"]}
          columns={["large", "flex"]}
          areas={[
            ["header", "header"],
            ["sidebar", "main"],
            ["footer", "footer"],
          ]}
          gap="small"
        >
          <Box background="brand" gridArea="header">
            Filter/Search
          </Box>

          <Box background="light-1" gridArea="sidebar">
            <List data={props.schedule.results}>
              {
                // TODO: implement onMore
                (item: Schedule, idx: number) => (
                  <Box
                    key={idx}
                    height="xsmall"
                    margin="medium"
                    direction="row"
                    justify="start"
                    align="center"
                  >
                    <ScheduleItem item={item} />
                  </Box>
                )
              }
            </List>
          </Box>

          <Box background="light-2" gridArea="main">
            Main
          </Box>

          <Box background="brand" gridArea="footer"></Box>
        </Grid>
      </Box>
    </UserLayout>
  );
};

export default SchedulePage;
