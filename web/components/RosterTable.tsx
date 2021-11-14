import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../components/lib";

interface Attendance {
  display_name: string;
  attending: boolean | null;
}

export type Props = {
  attendance: Attendance[];
};

const RosterTable = ({ attendance }: Props) => (
  <Box>
    <Table>
      <TableHeader>
        <TableRow>
          <TableCell scope="col" border="bottom">
            Name
          </TableCell>
          <TableCell scope="col" border="bottom">
            Attending?
          </TableCell>
        </TableRow>
      </TableHeader>
      <TableBody>
        {attendance.map((attend, idx, attendance) => (
          <TableRow key={idx}>
            <TableCell scope="row" width="xsmall">
              <strong>{attend.display_name}</strong>
            </TableCell>
            <TableCell align="center">
              {attend.attending ? "Yes" : "No"}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </Box>
);

export default RosterTable;
