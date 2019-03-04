import React from 'react';
import PropTypes from 'prop-types';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import Select from '@material-ui/core/Select';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import RootRef from '@material-ui/core/RootRef';

const examples = [
  'AllenNLP is a PyTorch-based natural language processing library developed at the Allen Institute for Artificial Intelligence in Seattle.',
  'Did Uriah honestly think he could beat The Legend of Zelda in under three hours?',
  'Michael Jordan is a professor at Berkeley.',
  "My preferred candidate is Cary Moon, but she won't be the next mayor of Seattle.",
  'If you like Paul McCartney you should listen to the first Wings album.',
  'If you like Paul McCartney you should listen to the first Wings album.'
]

export default class ExampleSelect extends React.Component {
  static propTypes = {
    updateBioNlp: PropTypes.func.isRequired
  };

  state = {
    content: ''
  }

  constructor(props) {
    super(props);
    this.labelRef = React.createRef();
  }


  handleChange = event => {
    this.setState({
      content: event.target.value
    })
    this.props.updateBioNlp && this.props.updateBioNlp(event.target.value);
  };

  render () {
    return (
      <FormControl variant="outlined" style={{ width: '100%' }}>
        <RootRef rootRef={this.labelRef}>
          <InputLabel
            style={{ whiteSpace: 'nowrap' }}
            htmlFor="outlined-example"
          >
            Example Texts
          </InputLabel>
        </RootRef>
        <Select
          value={this.state.content}
          onChange={this.handleChange}
          input={
            <OutlinedInput
              notched
              labelWidth={110}
              name="example"
              id="outlined-example"
            />
          }
        >
          <MenuItem value=""><em>--</em></MenuItem>
          {
            examples.map((example, i) => (
              <MenuItem key={i} value={example}>{example}</MenuItem>
            ))
          }
        </Select>
      </FormControl>
    );
  }
}
