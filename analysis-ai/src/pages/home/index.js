import React, { Component } from 'react';
import GithubFork from '../../components/fork';
import { Highlighter } from '../../components/highlighter';
import { Header } from '../../components/header';
import InputWithExamples from '../../containers/input-with-examples';
import ResponseTextAreaContainer from '../../containers/response-text-area/container';
import RequestRadio from '../../containers/request-type-radio'
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
            <Grid item xs={6} className='text-center'>
              <Header color='#827717' gutterBottom variant="h3" component="h1">
                Solving BioNLP problems
              </Header>
              <Typography gutterBottom component="p">
                This App solves <b><Highlighter color='#455a64'>BioNLP</Highlighter></b> problems using <b><Highlighter color='#455a64'>Bert(BioBert Pytorch)</Highlighter></b>
              </Typography>
            </Grid>
            <Grid item xs={10}>
              <Card>
                <CardContent>
                  <Header color='#9e9d24' gutterBottom variant="h5" component="h2">
                    Description
                  </Header>
                  <Typography component="p">
                    This app demonstrates how Bert(BioBert) can be finetuned and used to beat any state of the art result. In this we have trained it discover entites in medical text. In <b><Highlighter color='#455a64'>BioNLP13CG</Highlighter></b> it finds entites like <b><Highlighter color='#455a64'>'Anatomical_system'</Highlighter></b>, <b><Highlighter color='#455a64'>'Cancer'</Highlighter></b>, <b><Highlighter color='#455a64'>'Cell'</Highlighter></b>,  <b><Highlighter color='#455a64'>'Cellular_component'</Highlighter></b>, <b><Highlighter color='#455a64'>'Developing_anatomical_structure'</Highlighter></b>, <b><Highlighter color='#455a64'>'Gene_or_gene_product'</Highlighter></b>, <b><Highlighter color='#455a64'>'Immaterial_anatomical_entity'</Highlighter></b>, <b><Highlighter color='#455a64'>'Multi-tissue_structure'</Highlighter></b>, <b><Highlighter color='#455a64'>'Organ'</Highlighter></b>, <b><Highlighter color='#455a64'>'Organism'</Highlighter></b>, <b><Highlighter color='#455a64'>'Organism_subdivision'</Highlighter></b>, <b><Highlighter color='#455a64'>'Organism_substance'</Highlighter></b>, <b><Highlighter color='#455a64'>'Pathological_formation'</Highlighter></b>, <b><Highlighter color='#455a64'>'Simple_chemical'</Highlighter></b>, <b><Highlighter color='#455a64'>'Tissue'</Highlighter></b>  and in <b><Highlighter color='#455a64'>BC5CDR</Highlighter></b> it finds <b><Highlighter color='#455a64'>Disease and Chemicals</Highlighter></b>.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item style={{ marginTop: '24px', width: '100%', textAlign: 'start' }} xs={10}>
              <Header color='#9e9d24' gutterBottom variant="h5" component="h2"> DEMO </Header>
            </Grid>
            <Grid item style={{ width: '100%', textAlign: 'start' }} xs={10}>
              <RequestRadio />
            </Grid>
            <InputWithExamples />
            <Grid item xs={10} style={{ width: '100%' }} >
              <ResponseTextAreaContainer />
            </Grid>
          </Grid>
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
