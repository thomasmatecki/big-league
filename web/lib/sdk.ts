import { Configuration, RestApi } from "../gen/sdk";
import config from "../config";

const restConfig = new Configuration({ basePath: config.api_host });
export default new RestApi(restConfig);
