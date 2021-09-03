import "../styles/globals.css";
import type { AppProps } from "next/app";
import { Grommet } from 'grommet';


const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '20px',
      height: '20px',
    },
  },
   colors: {
     'light-2': '#f5f5f5',
     'text': {
       light: 'rgba(0, 0, 0, 0.87)',
     },
   },
   edgeSize: {
     small: '14px',
   },
   elevation: {
     light: {
       medium: '0px 2px 4px -1px rgba(0, 0, 0, 0.2), 0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12)',
     },
   },
};

function App({ Component, pageProps }: AppProps) {
  return (
    <Grommet full theme={theme}>
      <Component {...pageProps} />
    </Grommet>
  );
}
export default App;
