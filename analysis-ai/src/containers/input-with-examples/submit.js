import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { fetchBc5cdr } from '../../actions/bcdr';
import Submit from '../../components/input-with-examples/submit';

const mapDispatchToProps = dispatch => {
  return bindActionCreators({
    fetchData: fetchBc5cdr
  }, dispatch);
}

export default connect(null, mapDispatchToProps)(Submit);
