import styled from 'styled-components';

export const Highlighter = styled.span`
  color: ${props => props.color};
  border-radius: 5px;
  background-color: ${props => props.bgColor ? props.bgColor : 'transparent'}
`;
