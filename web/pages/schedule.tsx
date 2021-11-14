import { AxiosResponse } from "axios";
import { format } from "date-fns";
import {
  Box,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Grid,
  List,
  Text,
} from "grommet";
import { indexBy, map, prop } from "ramda";
import React, { useState } from "react";
import { useQuery, UseQueryResult } from "react-query";
import RosterTable from "../components/RosterTable";
import UserLayout from "../components/UserLayout";
import {
  AttendanceList,
  MatchTeams,
  Schedule,
  TeamList,
  UserApi,
} from "../gen/sdk";
import { restApi } from "../lib/sdk";
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
      <Box
        border={{
          side: "left",
          color: "background-contrast",
        }}
        pad="medium"
      >
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

const MatchBox = ({ scheduleItem }: { scheduleItem: Schedule }) => {
  const teamIds = [scheduleItem.team.id, scheduleItem.opponent.id];

  // Retrieve the teams for the user and their opponent
  const teamsResult: UseQueryResult<AxiosResponse<TeamList>> = useQuery(
    ["teams", teamIds],
    async (): Promise<AxiosResponse<TeamList>> =>
      await restApi.listTeams(1, teamIds?.join(","))
  );

  // Retrieve the teams for the user and their opponent
  const attendanceResult: UseQueryResult<AxiosResponse<AttendanceList>> =
    useQuery(
      ["attendance", scheduleItem.match.id],
      async (): Promise<AxiosResponse<AttendanceList>> =>
        await restApi.listAttendances(1, `${scheduleItem.match.id}`)
    );

  const { data: teamsData, isSuccess: teamSuccess } = teamsResult;
  const { data: attendanceData, isSuccess: attendanceSuccess } =
    attendanceResult;

  if (teamSuccess && attendanceSuccess) {
    const teamsById = indexBy(
      prop("id"),
      (teamsData as AxiosResponse<TeamList>).data.results
    );

    const attendanceByPlayerId = indexBy(
      prop("player_id"),
      (attendanceData as AxiosResponse<AttendanceList>).data.results
    );

    // Huh? type MatchTeams?
    const playerToAttendance = (player: MatchTeams) => ({
      display_name: player.name,
      attending: attendanceByPlayerId[player.id].attending,
    });

    console.log();

    return (
      <Card background="light-1">
        <CardHeader pad="medium" background="white">
          <Grid
            fill
            columns={["flex", "xsmall", "medium", "xsmall", "flex"]}
            rows={["flex"]}
            areas={[
              ["team", "team-logo", "faceoff", "opponent-logo", "opponent"],
            ]}
            gap="small"
          >
            <Box gridArea="team" align="end">
              {teamsById[scheduleItem.team.id].name}
            </Box>

            <Box gridArea="team-logo" align="end">
              team-logo
            </Box>

            <Box gridArea="faceoff" align="center">
              <Text weight="bold">Long Branch Park -- Field 1</Text>
              <Text>Monday, August 1</Text>
            </Box>
            <Box gridArea="opponent-logo" align="start">
              opplogo
            </Box>

            <Box gridArea="opponent" align="start">
              {teamsById[scheduleItem.opponent.id].name}
            </Box>
          </Grid>
        </CardHeader>

        <CardBody pad="medium">
          <Grid
            fill
            columns={["1/3", "1/3", "1/3"]}
            rows={["flex"]}
            areas={[["team-roster", "opponent-roster", "location"]]}
            gap="small"
          >
            <Box gridArea="team-roster" align="end">
              <RosterTable
                attendance={map(
                  playerToAttendance,
                  teamsById[scheduleItem.team.id].players
                )}
              />
            </Box>
            <Box gridArea="opponent-roster" align="end">
              <RosterTable
                attendance={map(
                  playerToAttendance,
                  teamsById[scheduleItem.opponent.id].players
                )}
              />
            </Box>
          </Grid>
        </CardBody>

        <CardFooter pad={{ horizontal: "small" }} background="white">
          Game {scheduleItem?.match.id}
        </CardFooter>
      </Card>
    );
  } else {
    return <Box />;
  }
};

const SchedulePage = (props: Props) => {
  const [selectedItem, setSelected] = useState(props.schedule.results[0]);

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
        >
          <Box background="brand" gridArea="header">
            Filter/Search
          </Box>

          <Box background="light-1" gridArea="sidebar">
            <List
              data={props.schedule.results}
              pad="none"
              border={{ color: "background-contrast" }}
            >
              {
                // TODO: implement onMore
                (item: Schedule, idx: number) => (
                  <Box
                    key={idx}
                    height="xsmall"
                    direction="row"
                    justify="start"
                    align="center"
                    pad="none"
                    background={{
                      color: selectedItem.id === item.id ? "white" : "light-1",
                    }}
                    onClick={() => setSelected(item)}
                    hoverIndicator="white"
                  >
                    <ScheduleItem item={item} />
                  </Box>
                )
              }
            </List>
          </Box>

          <Box gridArea="main" margin="small">
            {selectedItem ? (
              <MatchBox scheduleItem={selectedItem}></MatchBox>
            ) : (
              <Box />
            )}
          </Box>

          <Box background="brand" gridArea="footer"></Box>
        </Grid>
      </Box>
    </UserLayout>
  );
};

export default SchedulePage;
