import React, { Component } from 'react';
import GithubFork from '../../components/fork';
import { Highlighter } from '../../components/highlighter';
import { Header } from '../../components/header';
import InputWithExamples from '../../components/input-with-examples';
import NlpTextArea from '../../containers/nlp-text-area'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import './index.css';

const theme = createMuiTheme({
  palette: {
    primary: { main: '#827717' }, // Purple and green play nicely together.
    secondary: { main: '#11cb5f' }, // This is just green.A700 as hex.
    text: {
      secondary: '#424242'
    }
  },
  typography: {
    useNextVariants: true,
  },
  props: {
    MuiButtonBase: { // Name of the component ⚛️ / style sheet
      text: { // Name of the rule
        color: '#f2f2f2', // Some CSS
      },
    },
  }
});


class App extends Component {
  render() {
    return (
      <MuiThemeProvider theme={theme}>
        <div className='main-wrapper' style={{ padding: '48px 12px' }}>
          <GithubFork href='https://github.com/MeRajat/SolvingAlmostAnythingWithBert' />
          <Grid container justify='center' alignItems='center' direction='column' spacing={24}>
            <Grid item xs={6}>
              <Header color='#827717' gutterBottom variant="h3" component="h1">
                BioBert Pytorch
              </Header>
              <Typography gutterBottom component="p">
                This App finds <b><Highlighter color='#455a64'>Named Entity Recognition</Highlighter></b> (NER)
              </Typography>
            </Grid>
            <Grid item xs={10}>
              <Card>
                <CardContent>
                  <Header color='#9e9d24' gutterBottom variant="h5" component="h2">
                    Named Entity Recognition
                  </Header>
                  <Typography component="p">
                    The named entity recognition model identifies named entities (people, locations, organizations, and miscellaneous) in the input text. This model is the "baseline" model described in Peters, Ammar, Bhagavatula, and Power 2017 . It uses a Gated Recurrent Unit (GRU) character encoder as well as a GRU phrase encoder, and it starts with pretrained GloVe vectors for its token embeddings. It was trained on the CoNLL-2003 NER dataset. It is not state of the art on that task, but it's not terrible either. (This is also the model constructed in our Creating a Model tutorial.)
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item style={{ marginTop: '24px', width: '100%', textAlign: 'start' }} xs={10}>
              <Header color='#9e9d24' gutterBottom variant="h5" component="h2"> DEMO </Header>
            </Grid>
            <InputWithExamples />
            <Grid item xs={10} style={{ width: '100%' }} >
              <NlpTextArea />
            </Grid>
          </Grid>
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
