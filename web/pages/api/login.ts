
import type { NextApiRequest, NextApiResponse } from "next";
import { Session } from "next-iron-session";
import { withSession } from "../../lib/session";
import  oauth from "../../lib/oauth";

type NextIronRequest = NextApiRequest & { session: Session };


async function handler(
  req: NextIronRequest,
  res: NextApiResponse
): Promise<void> {
  res.redirect(302, oauth.authorize_url );
}

export default withSession(handler);