import { connect } from 'react-redux';
import NlpTextArea from '../components/nlp-text-area';

const mapStateToProps = state => {
  return {
    tags: state.bioNlp.response.tags,
    loading: state.bioNlp.loading
  }
}

export default connect(mapStateToProps, null)(NlpTextArea);
