import React from 'react';
import PropTypes from 'prop-types';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';

import types from '../../enums/request-types';

export default class RequestRadio extends React.PureComponent {
  static propTypes = {
    type: PropTypes.string.isRequired,
    updateRequestType: PropTypes.func.isRequired
  }
  handleChange = event => {
    this.props.updateRequestType(event.target.value)
  }
  render () {
    return (
      <RadioGroup
        aria-label="nerType"
        name="nerType"
        value={this.props.type}
        onChange={this.handleChange}
        row
      >
        <FormControlLabel
          value={types.BIO_NLP}
          control={<Radio color="primary" />}
          label="BIO NLP 13CG"
          labelPlacement="end"
        />
        <FormControlLabel
          value={types.BC5CDR}
          control={<Radio color="primary" />}
          label="BC5CDR"
          labelPlacement="end"
        />
      </RadioGroup>
    )
  }
}
