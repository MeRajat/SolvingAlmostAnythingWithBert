import styled from 'styled-components';
import { withTheme } from '@material-ui/core/styles';

const StyledText = styled.span`
  display: inline-flex;
  flex-direction: column;
  position: relative;
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 5px;
  box-sizing: border-box;
  background: ${props => props.bgColor ? props.bgColor : props.theme.palette.primary.main};

  > span.text {
    padding: 4px 10px;
    background: #fff;
    color: #424242;
    box-sizing: border-box;
    border-radius: 5px;
    line-height: 1.4;
    text-align: center;
  }

  > span.type {
    font-size: 12px;
    background: ${props => props.bgColor ? props.bgColor : props.theme.palette.primary.main};
    color: ${props => props.color ? props.color : props.theme.palette.primary.main};
    line-height: 1;
    padding-top: 5px;
    border-radius: 0 0 5px 5px;
    text-align: center;
  }
`;

export default withTheme()(StyledText)
