import type { NextApiRequest, NextApiResponse } from "next";

export type Middleware = (
  req: NextApiRequest,
  res: NextApiResponse,
  next: any
) => Promise<void> | void;

/**
 * Wait for a middleware to execute before continuing
 * and to throw an error when an error happens in a middleware
 */
export default {
  init: (middleware: Middleware) => {
    return (req: NextApiRequest, res: NextApiResponse) =>
      new Promise((resolve, reject) => {
        middleware(req, res, (result: unknown) => {
          if (result instanceof Error) {
            return reject(result);
          }
          return resolve(result);
        });
      });
  },
};
