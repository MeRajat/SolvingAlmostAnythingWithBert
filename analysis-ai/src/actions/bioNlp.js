import constants from '../redux-constants/fetch';
import params from '../utils/params';

export const fetchBioNlp = () => async (dispatch, getState) => {
  dispatch({
    type: constants.FETCH_BIO_NLP_REQUEST
  })

  const payload =  params(getState().bioNlp.request);

  try {
    const response = fetch(`${process.env.REACT_APP_DEV_API_URL}/extract-ner?${payload}`);
    console.log(response);
  } catch (error) {

  }
}

export const updateBioNlp = text => {
  return {
    type: constants.UPDATE_BIO_NLP,
    content: text
  }
}
