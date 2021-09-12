import Cors from "cors";
import type { NextApiRequest, NextApiResponse } from "next";
import { Session } from "next-iron-session";
import middleware from "../../lib/middleware";
import oauth from "../../lib/oauth";
import { withSession } from "../../lib/session";

type NextIronRequest = NextApiRequest & { session: Session };

const cors = middleware.init(
  // Config options : https://github.com/expressjs/cors#configuration-options
  Cors({
    // Only allow requests with GET, POST and OPTIONS
    methods: ["GET"],
    origin: true,
    credentials: true,
  })
);

async function handler(
  req: NextIronRequest,
  res: NextApiResponse
): Promise<void> {
  //
  await cors(req, res);

  const { next: _next, ...authQuery } = req.query;
  const next = typeof _next == "object" ? _next[0] : _next;

  const authData = await oauth.auth(authQuery);
  authData.expires_at = Math.round(Date.now() / 1000) + authData.expires_in;

  req.session.set("auth", authData);
  debugger;

  await req.session.save();
  if (next) {
    res.redirect(next as string);
  } else {
    res.json(authData);
  }
}

export default withSession(handler);
