import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateBc5cdr } from '../../actions/bcdr';
import ExampleSelect from '../../components/input-with-examples/example-select';

const mapStateToProps = state => {
  return {
    content: state.bc5cdr.request.text
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    update: updateBc5cdr
  }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(ExampleSelect);
