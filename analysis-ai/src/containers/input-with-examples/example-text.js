import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateBioNlp } from '../../actions/bioNlp';
import ExampleText from '../../components/input-with-examples/example-text';

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

export default connect(mapStateToProps, mapDispatchToProps)(ExampleText);
