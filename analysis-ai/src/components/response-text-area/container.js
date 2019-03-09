import React from 'react';
import BioNlpTextArea from '../../containers/response-text-area/bioNlp-text-area'
import Bc5drTextArea from '../../containers/response-text-area/bc5dr-text-area'

import types from '../../enums/request-types';

export default props => {
  if (props.type === types.BIO_NLP) {
    return <BioNlpTextArea />
  }
  return <Bc5drTextArea />
}
