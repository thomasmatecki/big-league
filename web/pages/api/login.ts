import type { NextApiRequest, NextApiResponse } from "next";
import { Session } from "next-iron-session";
import oauth from "../../lib/oauth";
import { withSession } from "../../lib/session";

type NextIronRequest = NextApiRequest & { session: Session };

async function handler(
  req: NextIronRequest,
  res: NextApiResponse
): Promise<void> {
  res.redirect(302, oauth.authorize_url);
}

export default withSession(handler);
