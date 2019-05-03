import constants from '../redux-constants/fetch';
import params from '../utils/params';

export const fetchBc5cdr = () => async (dispatch, getState) => {
  dispatch({
    type: constants.FETCH_BC5CDR_REQUEST
  })

  const payload =  params(getState().bc5cdr.request);

  try {
    const response = await fetch(`http://13.72.66.146:9000/extract-ner?${payload}`)
      .then(response => response.json());
    dispatch({
      type: constants.FETCH_BC5CDR_SUCCESS,
      response
    })
  } catch (error) {
    dispatch({
      type: constants.FETCH_BC5CDR_FAILURE,
      errorMessage: 'Request Failed'
    })
  }
}

export const updateBc5cdr = text => {
  return {
    type: constants.UPDATE_BC5CDR,
    content: text
  }
}
