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
    methods: ["GET", "POST", "OPTIONS"],
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

  const data = await oauth.auth(req.query);

  req.session.set("auth", data);

  await req.session.save();

  res.json({ message: "Ok" });
}

export default withSession(handler);
