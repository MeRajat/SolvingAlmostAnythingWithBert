import { connect } from 'react-redux';
import ResponseTextAreaContainer from '../../components/response-text-area/container';

const mapStateToProps = state => {
  return {
    type: state.requestType.type
  }
}

export default connect(mapStateToProps, null)(ResponseTextAreaContainer);
