import type { AppProps } from "next/app";
import { Grommet } from "../components/lib";
import Head from "next/head";
import theme from "../theme";

function App({ Component, pageProps }: AppProps) {
  return (
    <Grommet full theme={theme}>
      <Head>
        <title>League App</title>
      </Head>
      <Component {...pageProps} />
    </Grommet>
  );
}
export default App;
