import React, {Fragment} from 'react';
import styled from 'styled-components';
import Tooltip from '@material-ui/core/Tooltip';
import CircularProgress from '@material-ui/core/CircularProgress';
import StyledText from './styled-text';

import mapCodeToColors from '../../utils/mapCodeToColors';

const Wrapper = styled.div`
  background: #fafafa;
  padding: 24px;
  border-radius: 5px;
  border: 1px solid #efefef;
  line-height: 1.4;
`;

const renderWrapper = (tags) => {
  return <Wrapper>
    {
      tags.map((tag, i) => {
        let space = ' ';
        if (i === 0) {
          space = '';
        }
        if (tag[1] === 'O') {
          return <span key={i}>{space + tag[0]}</span>
        }
        return <Fragment key={i}>
          {space}
          <Tooltip title={tag[1]}>
            <StyledText
              bgColor={mapCodeToColors[tag[1]].bg}
              color={mapCodeToColors[tag[1]].fg}
            >
              <span className='text'>
                {tag[0]}
              </span>
              <span className='type'>
                {tag[1]}
              </span>
            </StyledText>
          </Tooltip>
        </Fragment>
      })
    }
  </Wrapper>
}

export default props => {
  if (props.tags && !props.loading) {
    return renderWrapper(props.tags);
  }
  if (props.loading) {
    return <Wrapper style={{ textAlign: 'center' }}>
      <CircularProgress />
    </Wrapper>
  }
  return null;
}
