import { Session, withIronSession } from "next-iron-session";
import config from "../config";
import { Configuration, ProfileApi, RestApi } from "../gen/sdk";

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

export type APISessionRequest<T> = SessionRequest<T> & {
  profileApi: ProfileApi;
  restApi: RestApi;
};

export type HasAPISessionRequest<T> = {
  req: APISessionRequest<T>;
};

/**
 *
 * @param handler
 * @returns
 */
export function WithAPISession<T>(handler: any) {
  const _withAPI = async function withApi(...args: any) {
    const handlerType = args[0] && args[1] ? "api" : "ssr";
    const req = handlerType === "api" ? args[0] : args[0].req;
    const res = handlerType === "api" ? args[1] : args[0].res;

    const auth = await req.session.get("auth");

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

    req.profileApi = new ProfileApi(apiConfig);

    return handler(...args);
  };

  return withSession(_withAPI);
}
