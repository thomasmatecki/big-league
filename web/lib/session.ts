import { GetServerSideProps } from "next";
import { Session, withIronSession } from "next-iron-session";
import config from "../config";
import { Configuration, UserApi } from "../gen/sdk";
import oauth, { OAuth } from "../lib/oauth";

// TODO:  ALL the types here is wrong.
type SessionRequest<R> = R & {
  session: Session;
};

export type HasSessionRequest<T, R> = T & {
  req: SessionRequest<R>;
};

/**
 *
 * @param handler
 * @returns
 */
export function withSession(handler: any): any {
  return withIronSession(handler, config.session_cookie);
}

const getAuth = async (session: Session): Promise<OAuth | null> => {
  const authData: OAuth | undefined = await session.get("auth");

  if (!authData) {
    return null;
  }

  // 10 Seconds before it expires
  if (authData.expires_at < Math.round(Date.now() / 1000) - 10) {
    const freshAuthData: OAuth = await oauth.refresh(authData);
    session.set("auth", freshAuthData);
    await session.save();
    return freshAuthData;
  }

  return authData;
};

/**
 *
 * @param handler
 * @returns
 */
export function withUserApi(getServerSideProps: any): GetServerSideProps {
  const _withAPI = async function withApi(context: any) {
    const auth = await getAuth(context.req.session);

    if (!auth) {
      return {
        redirect: {
          destination: "/login",
          permanent: false,
        },
      };
    }

    const apiConfig = new Configuration({
      basePath: config.api_host,
      accessToken: auth.access_token,
    });

    const userApi = new UserApi(apiConfig);
    context = { ...context, userApi };

    return getServerSideProps(context);
  };

  return withSession(_withAPI);
}
