import axios from "axios";
import querystring from "querystring";
import config from "../config";

interface Auth {
  access_token: string;
}

export type OAuth = {
  access_token: string;
  expires_in: number;
  token_type: string;
  scope: string;
  refresh_token: string;
  expires_at: number;
};

class OAuthClient {
  constructor(private api_host: string) {}

  _setExpiresAt({ data: authData }: any): OAuth {
    authData.expires_at = Math.round(Date.now() / 1000) + authData.expires_in;
    return authData;
  }

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
    }).then(this._setExpiresAt);
  }

  async revoke(auth: Auth) {
    return this.post("o/revoke_token/", {
      token: auth.access_token,
      client_id: config.oauth.client_id,
      client_secret: config.oauth.client_secret,
    });
  }

  async refresh(auth: OAuth): Promise<OAuth> {
    return this.post("o/token/", {
      grant_type: "refresh_token",
      client_id: config.oauth.client_id,
      client_secret: config.oauth.client_secret,
      refresh_token: auth.refresh_token,
    }).then(this._setExpiresAt);
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
