import { GetServerSideProps } from "next";
import { Session, withIronSession } from "next-iron-session";
import config from "../config";
import { Configuration, UserApi } from "../gen/sdk";

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

/**
 *
 * @param handler
 * @returns
 */
export function withUserApi(getServerSideProps: any): GetServerSideProps {
  const _withAPI = async function withApi(context: any) {
    const auth = await context.req.session.get("auth");

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
