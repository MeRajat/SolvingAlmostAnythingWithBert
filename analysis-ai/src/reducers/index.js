import { combineReducers } from 'redux';
import bioNlp from './bioNlp';
import bc5cdr from './bcdr';
import requestType from './request-type';

export default combineReducers({
  bioNlp,
  bc5cdr,
  requestType
});
