import React from 'react';
import PropTypes from 'prop-types';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import Select from '@material-ui/core/Select';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import styled from 'styled-components';
import RootRef from '@material-ui/core/RootRef';

import TooltipMenu from './tooltip-composed-menu';

const examples = [
  {
    key: 'bnlp#1',
    type: 'bioNlp',
    text: 'Cooccurrence of reduced expression of alpha - catenin and overexpression of p53 is a predictor of lymph node metastasis in early gastric cancer.',
  },
  {
    key: 'bnlp#2',
    type: 'bioNlp',
    text: 'In this review , the role of TSH - R gene alterations in benign and malignant thyroid neoplasia is examined.',
  },
  {
    key: 'bc5cdr#1',
    type: 'bc5cdr',
    text: "The authors describe the case of a 56 - year - old woman with chronic , severe heart failure secondary to dilated cardiomyopathy and absence of significant ventricular arrhythmias who developed QT prolongation and torsade de pointes ventricular tachycardia during one cycle of intermittent low dose ( 2.5 mcg/kg per min ) dobutamine."
  }
];

const Subheader = styled.li`
  font-family: "Roboto", "Helvetica", "Arial", sans-serif;
  line-height: 1.5em;
  padding: 11px 16px;
  color: #827717;
  font-weight: 700;
  border-bottom: 1px solid #e2e2e2;
  pointer-events: none;
`;



export default class ExampleSelect extends React.Component {
  static propTypes = {
    update: PropTypes.func.isRequired
  };

  state = {
    content: '',
    selectedExampleKey: ''
  }

  constructor(props) {
    super(props);
    this.labelRef = React.createRef();
  }


  handleChange = event => {
    const selectedExample = typeof event.target.value === 'string' ? {} : event.target.value;
    this.setState({
      content: selectedExample.text || '',
      selectedExampleKey: selectedExample.key || ''
    })
    this.props.update(selectedExample.text || '');
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
          renderValue={() => {
            return <span>{this.state.content}</span>
          }}
          onChange={this.handleChange}
          input={
            <OutlinedInput
              notched
              labelWidth={110}
              name="example"
              id="outlined-example"
            />
          }
          MenuProps={{
            PaperProps: {
              style: {
                width: 400,
              },
            },
          }}
        >
          <MenuItem selected={!this.state.selectedExampleKey} value=""><em>--</em></MenuItem>
          <Subheader className='subheader'>Bio NLP</Subheader>
            {
              examples.slice(0, 2).map(example => {
                return <TooltipMenu key={example.key} selectedKey={this.state.selectedExampleKey} value={example} />
              })
            }
          <Subheader className='subheader'>BC5 CDR</Subheader>
            {
              examples.slice(2).map(example => {
                return <TooltipMenu key={example.key} selectedKey={this.state.selectedExampleKey} value={example} />
              })
            }
        </Select>
      </FormControl>
    );
  }
}
