import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateRequestType } from '../actions/request-type';
import RequestRadio from '../components/request-type-radio';

const mapStateToProps = state => {
  return {
    type: state.requestType.type
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    updateRequestType
  }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(RequestRadio);
