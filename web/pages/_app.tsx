import type { AppProps } from "next/app";
import Head from "next/head";
import { QueryClient, QueryClientProvider } from "react-query";
import { Grommet } from "../components/lib";
import theme from "../theme";

// Create a client
const queryClient = new QueryClient();

function App({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <Grommet full theme={theme}>
        <Head>
          <title>League App</title>
        </Head>
        <Component {...pageProps} />
      </Grommet>
    </QueryClientProvider>
  );
}
export default App;
