import config from "../config";
import * as _sdk from "../gen/sdk";

const apiConfig = new _sdk.Configuration({
  basePath: config.api_host,
  baseOptions: {
    /**
     * These are the default django xsrf values.
     *
     * If serving the API and UI on different domains, the cookie domain may
     * need to be adjusted in django settings.
     */
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
    withCredentials: true,
  },
});

export const restApi = new _sdk.RestApi(apiConfig);
export const userApi = new _sdk.UserApi(apiConfig);
