import type { AppProps } from "next/app";
import Head from "next/head";
import { Grommet } from "../components/lib";
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
