import { connect } from 'react-redux';
import NlpTextArea from '../components/nlp-text-area';
import types from '../enums/request-types';

const mapStateToProps = state => {
  if (state.requestType.type === types.BIO_NLP) {
    return {
      tags: state.bioNlp.response.tags,
      loading: state.bioNlp.loading
    }
  } else {
    return {
      tags: state.bc5cdr.response.tagging,
      loading: state.bc5cdr.loading
    }
  }
}

export default connect(mapStateToProps, null)(NlpTextArea);
