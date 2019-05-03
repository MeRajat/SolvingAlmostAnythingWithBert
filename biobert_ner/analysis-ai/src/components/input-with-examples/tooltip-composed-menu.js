import React from 'react';
import Tooltip from '@material-ui/core/Tooltip';
import MenuItem from '@material-ui/core/MenuItem';

import styled from 'styled-components';

const EllipsisText = styled.span`
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
`;

export default props => {
  const {key, selectedKey, ...rest} = props;
  const value = rest['data-value'];
  return <Tooltip title={value.text}>
    <MenuItem selected={value.key === selectedKey} {...rest}>
      <EllipsisText>{value.text}</EllipsisText>
    </MenuItem>
  </Tooltip>
  // return 'Hello World'
}
