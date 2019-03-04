import React from 'react';
import ExampleSelect from './example-select';
import ExampleText from './example-text';
import Grid from '@material-ui/core/Grid';

export default class InputWithExamples extends React.PureComponent {
  state = {
    content: ''
  };

  handleChange = event => {
    this.setState({ content: event.target.value });
  };

  render () {
    return (
      <Grid item container style={{ marginTop: 24 }} justify='center' alignItems='center' spacing={24}>
        <Grid item xs={3}><ExampleSelect onChange={this.handleChange} /></Grid>
        <Grid item xs={7}><ExampleText onChange={this.handleChange} content={this.state.content} /></Grid>
      </Grid>
    )
  }
}
