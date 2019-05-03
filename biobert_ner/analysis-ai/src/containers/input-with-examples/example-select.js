import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateBioNlp } from '../../actions/bioNlp';
import ExampleSelect from '../../components/input-with-examples/example-select';

const mapStateToProps = state => {
  return {
    content: state.bioNlp.request.text
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    update: updateBioNlp
  }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(ExampleSelect);
