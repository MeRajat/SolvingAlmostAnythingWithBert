import React from 'react';
import ExampleSelect from '../../containers/example-select';
import ExampleText from '../../containers/example-text';
import Submit from '../../containers/submit';
import Grid from '@material-ui/core/Grid';

export default class InputWithExamples extends React.PureComponent {
  render () {
    return (
      <Grid container style={{ margin: '-12px', flexGrow: 0, width: '100%' }} justify='center' alignItems='center' spacing={24}>
        <Grid item xs={2}><ExampleSelect /></Grid>
        <Grid item xs={7}><ExampleText /></Grid>
        <Grid item xs={1} style={{ textAlign: 'right' }}>
          <Submit />
        </Grid>
      </Grid>
    )
  }
}
