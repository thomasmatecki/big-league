import config from "../config";
import * as _sdk from "../gen/sdk";

const apiConfig = new _sdk.Configuration({ basePath: config.api_host });

export const restApi = new _sdk.RestApi(apiConfig);
export const profileApi = new _sdk.UserApi(apiConfig);
