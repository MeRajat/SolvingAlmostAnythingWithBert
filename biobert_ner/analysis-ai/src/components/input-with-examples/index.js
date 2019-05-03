import React from 'react';
import PropTypes from 'prop-types';
import ExampleSelect from '../../containers/input-with-examples/example-select';
import ExampleText from '../../containers/input-with-examples/example-text';
import Submit from '../../containers/input-with-examples/submit';
import Bc5drSelect from '../../containers/input-with-examples/bc5dr-select';
import Bc5drText from '../../containers/input-with-examples/bc5dr-text';
import Bc5drSubmit from '../../containers/input-with-examples/bc5dr-submit';
import Grid from '@material-ui/core/Grid';

import types from '../../enums/request-types';

export default class InputWithExamples extends React.PureComponent {
  static propTypes = {
    type: PropTypes.string.isRequired
  }

  render () {
    return (
      <Grid container style={{ margin: '-12px', flexGrow: 0, width: '100%' }} justify='center' alignItems='center' spacing={24}>
        <Grid item xs={2}>
          { this.props.type === types.BIO_NLP
            ? <ExampleSelect />
            : <Bc5drSelect />
          }
        </Grid>
        <Grid item xs={7}>
          { this.props.type === types.BIO_NLP
            ? <ExampleText />
            : <Bc5drText />
          }
        </Grid>
        <Grid item xs={1} style={{ textAlign: 'right' }}>
          { this.props.type === types.BIO_NLP
            ? <Submit />
            : <Bc5drSubmit />
          }
        </Grid>
      </Grid>
    )
  }
}
