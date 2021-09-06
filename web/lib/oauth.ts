import axios from "axios";
import querystring from "querystring";
import config from "../config";

interface Auth {
  access_token: string;
}

class OAuthClient {
  constructor(private api_host: string) {}

  async post(path: string, data: any) {
    return axios({
      method: "POST",
      url: `${config.api_host}/${path}`,
      data: querystring.stringify(data),
      headers: {
        "content-type": "application/x-www-form-urlencoded;charset=utf-8",
      },
    });
  }

  async auth(query: object): Promise<any> {
    return this.post("o/token/", {
      ...query,
      grant_type: "authorization_code",
      client_id: config.oauth.client_id,
      client_secret: config.oauth.client_secret,
    }).then(({ data, status, statusText, ...rest }) => data);
  }

  async revoke(auth: Auth) {
    return this.post("o/revoke_token/", {
      token: auth.access_token,
      client_id: config.oauth.client_id,
      client_secret: config.oauth.client_secret,
    });
  }

  get authorize_url(): string {
    const query = querystring.stringify({
      client_id: config.oauth.client_id,
      response_type: "code",
    });
    return `${this.api_host}/o/authorize/?${query}`;
  }
}

export default new OAuthClient(config.api_host);
