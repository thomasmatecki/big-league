import type { NextApiRequest, NextApiResponse } from "next";
import { Session } from "next-iron-session";
import { withSession } from "../../lib/session";
import  oauth from "../../lib/oauth";
import config from "../../config";

type NextIronRequest = NextApiRequest & { session: Session };


async function handler(
  req: NextIronRequest,
  res: NextApiResponse
): Promise<void> {
  const auth = req.session.get("auth");

  oauth.revoke(auth);
  
  req.session.unset("auth");

  await req.session.save();

  res.redirect(302, config.logout_url);
}

export default withSession(handler);