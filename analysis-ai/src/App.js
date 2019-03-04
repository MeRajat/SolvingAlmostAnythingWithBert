import React, { Component } from 'react';
import GithubFork from './components/fork';
import { Highlighter } from './components/highlighter';
import { Header } from './components/header';
import InputWithExamples from './components/input-with-examples';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import './App.css';

class App extends Component {
  render() {
    console.log(process.env.REACT_APP_DEV_API_URL);
    return (
      <>
        <GithubFork href='https://github.com/MeRajat/SolvingAlmostAnythingWithBert' />
        <Grid container className='main-wrapper' justify='center' alignItems='center' direction='column' spacing={24}>
          <Grid item xs={6}>
            <Header color='#827717' gutterBottom variant="h3" component="h1">
              BioBert Pytorch
            </Header>
            <Typography gutterBottom component="p">
              This App finds <b><Highlighter color='#455a64'>Named Entity Recognition</Highlighter></b> (NER)
            </Typography>
          </Grid>
          <Grid item xs={6}>
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
          <InputWithExamples />
        </Grid>
      </>
    );
  }
}

export default App;
