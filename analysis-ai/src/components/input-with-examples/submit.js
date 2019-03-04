import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';

const Submit = (props) => {
  return (
    <Button variant="contained" color="primary" onClick={props.fetchData}>
      Submit
    </Button>
  )
}

Submit.propTypes = {
  fetchData: PropTypes.func.isRequired
}

export default Submit;
