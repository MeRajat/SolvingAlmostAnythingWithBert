import { connect } from 'react-redux';
import ResponseTextArea from '../../components/response-text-area';

const mapStateToProps = state => {
  return {
    tags: state.bc5cdr.response.tagging,
    loading: state.bc5cdr.loading
  }
}

export default connect(mapStateToProps, null)(ResponseTextArea);
