import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { fetchBioNlp } from '../../actions/bioNlp';
import Submit from '../../components/input-with-examples/submit';

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    fetchData: fetchBioNlp
  }, dispatch);
}

export default connect(null, mapDispatchToProps)(Submit);
