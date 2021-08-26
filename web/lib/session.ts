import { Handler } from "next-iron-session";

import type { NextApiRequest, NextApiResponse } from "next";
import { withIronSession, Session } from "next-iron-session";

import { GetServerSidePropsContext } from "next";

type SessionRequest = NextApiRequest & { session: Session };
export type WithSessionRequest = {
  req: SessionRequest;
};

export function withSession(handler: any) {
  return withIronSession(handler, {
    password: "complex_password_at_least_32_characters_long",
    cookieName: "myapp_cookiename",
    // if your localhost is served on http:// then disable the secure flag
    cookieOptions: {
      secure: process.env.NODE_ENV === "production",
    },
  });
}
