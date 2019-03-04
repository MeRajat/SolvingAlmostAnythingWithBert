export default (params = {}) => {
  return Object.keys(params).reduce((queryString, key, index) => {
    queryString += (index !== 0 ? '&' : '') + window.encodeURIComponent(key) + '=' + window.encodeURIComponent(params[key]);
    return queryString;
  }, '');
}
