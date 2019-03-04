import React from 'react';
import PropTypes from 'prop-types';
import TextField from '@material-ui/core/TextField';

export default class ExampleText extends React.Component {
  static propTypes = {
    content: PropTypes.string,
    onChange: PropTypes.func.isRequired
  }

  render () {
    return (
      <TextField
        id="standard-full-width"
        style={{ margin: 0 }}
        placeholder="Placeholder"
        fullWidth
        margin="normal"
        onChange={this.props.onChange}
        value={this.props.content}
        multiline
      />
    )
  }
}
