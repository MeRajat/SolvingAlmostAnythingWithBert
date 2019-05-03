import constants from '../redux-constants/fetch';
import types from '../enums/request-types';

const initialState = {
  // type: types.BIO_NLP // Default State
  type: types.BC5CDR
}

export default (state = initialState, action) => {
  const immutatedState = { ...state };
  switch (action.type) {
    case constants.REQUEST_TYPE_CHANGE:
      immutatedState.type = action.requestType;
      return immutatedState;
    default:
      return state;
  }
}
