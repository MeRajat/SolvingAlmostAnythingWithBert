import styled from 'styled-components';
import Typography from '@material-ui/core/Typography';

export const Header = styled(Typography)`
  color: ${props => props.color ? props.color: '#4f4f4f'} !important;
`;
