import { connect } from 'react-redux';
import ResponseTextArea from '../../components/response-text-area';

const mapStateToProps = state => {
  return {
    tags: state.bioNlp.response.tags,
    loading: state.bioNlp.loading
  }
}

export default connect(mapStateToProps, null)(ResponseTextArea);
