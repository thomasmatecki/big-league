import type { NextApiRequest, NextApiResponse } from "next";
import { Session } from "next-iron-session";
import { withSession } from "../../lib/session";
import  oauth from "../../lib/oauth";

type NextIronRequest = NextApiRequest & { session: Session };

async function handler(
  req: NextIronRequest,
  res: NextApiResponse
): Promise<void> {
  const data = await oauth.auth(req.query);

  req.session.set("auth", data);

  await req.session.save();

  res.redirect(302, "/home");
}

export default withSession(handler);
