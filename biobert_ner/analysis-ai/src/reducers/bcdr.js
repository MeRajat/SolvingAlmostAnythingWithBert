import constants from '../redux-constants/fetch';

const initialState = {
  response: {},
  request: {
    bc5cdr: 'BC5CDR',
    text: ''
  },
  loading: false,
  error: null
}

export default (state = initialState, action) => {
  const immutatedState = { ...state };
  switch (action.type) {
    case constants.FETCH_BC5CDR_REQUEST:
      immutatedState.loading = true;
      return immutatedState;
    case constants.FETCH_BC5CDR_SUCCESS:
      immutatedState.response = Object.assign({}, action.response);
      immutatedState.loading = false;
      immutatedState.error = null;
      return immutatedState;
    case constants.FETCH_BC5CDR_FAILURE:
      immutatedState.loading = false;
      immutatedState.error = { ...action.error };
      return immutatedState;
    case constants.UPDATE_BC5CDR:
      immutatedState.request = {...state.request};
      immutatedState.request.text = action.content;
      return immutatedState;
    default:
      return state;
  }
}
