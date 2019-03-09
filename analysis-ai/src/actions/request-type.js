import constants from '../redux-constants/fetch';

export const updateRequestType = (type) => {
  return {
    type: constants.REQUEST_TYPE_CHANGE,
    requestType: type
  }
}
