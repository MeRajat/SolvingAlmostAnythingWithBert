import constants from '../redux-constants/fetch';
import params from '../utils/params';

export const fetchBioNlp = () => async (dispatch, getState) => {
  dispatch({
    type: constants.FETCH_BIO_NLP_REQUEST
  })

  const payload =  params(getState().bioNlp.request);

  try {
    const response = await fetch(`http://13.72.66.146:9000/extract-ner?${payload}`)
      .then(response => response.json());
    dispatch({
      type: constants.FETCH_BIO_NLP_SUCCESS,
      response
    })
  } catch (error) {
    dispatch({
      type: constants.FETCH_BIO_NLP_FAILURE,
      errorMessage: 'Request Failed'
    })
  }
}

export const updateBioNlp = text => {
  return {
    type: constants.UPDATE_BIO_NLP,
    content: text
  }
}
