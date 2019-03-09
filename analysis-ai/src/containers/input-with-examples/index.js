import { connect } from 'react-redux';
import ExampleSelect from '../../components/input-with-examples';

const mapStateToProps = state => {
  return {
    type: state.requestType.type
  }
}

export default connect(mapStateToProps, null)(ExampleSelect);
