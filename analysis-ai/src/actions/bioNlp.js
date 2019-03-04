import constants from '../redux-constants/fetch';

export const fetchBioNlp = () => async dispatch => {
  dispatch({
    type: constants.FETCH_BIO_NLP_REQUEST
  })
}

export const updateBioNlp = text => {
  return {
    type: constants.UPDATE_BIO_NLP,
    content: text
  }
}
