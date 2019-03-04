import React from 'react';
import ExampleSelect from '../../containers/example-select';
import ExampleText from '../../containers/example-text';
import Grid from '@material-ui/core/Grid';

export default class InputWithExamples extends React.PureComponent {
  render () {
    return (
      <Grid container style={{ margin: '24px -12px -12px', flexGrow: 0, width: '100%' }} justify='center' alignItems='center' spacing={24}>
        <Grid item xs={3}><ExampleSelect /></Grid>
        <Grid item xs={7}><ExampleText /></Grid>
      </Grid>
    )
  }
}
