import constants from '../redux-constants/fetch';

const initialState = {
  response: {},
  request: {
    bionlp3g: 'BIO NLP 13CG',
    text: ''
  },
  loading: false,
  error: null
}

export default (state = initialState, action) => {
  const immutatedState = { ...state };
  switch (action.type) {
    case constants.FETCH_BIO_NLP_REQUEST:
      immutatedState.loading = true;
      return immutatedState;
    case constants.FETCH_BIO_NLP_SUCCESS:
      immutatedState.response = Object.assign({}, action.response);
      immutatedState.loading = false;
      immutatedState.error = null;
      return immutatedState;
    case constants.FETCH_BIO_NLP_FAILURE:
      immutatedState.loading = false;
      immutatedState.error = { ...action.error };
      return immutatedState;
    case constants.UPDATE_BIO_NLP:
      immutatedState.request = {...state.request};
      immutatedState.request.text = action.content;
      return immutatedState;
    default:
      return state;
  }
}
