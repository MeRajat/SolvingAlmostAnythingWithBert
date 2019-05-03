import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const GithubForkWrapper = styled.a`
  position: fixed;
  top: 0;
  right: 0;
  z-index: 1000;
  margin: 10px;
  text-decoration: none;
  font-size: 30px;
  color: rgba(0, 0, 0, 0.5);
  cursor: pointer;

  &:focus {
    outline: none;
  }

  &:hover, &:focus {
    color: rgba(0, 0, 0, 0.8);
  }
`;

export default class GithubFork extends React.PureComponent {
  static propTypes = {
    href: PropTypes.string.isRequired
  };

  render () {
    return <GithubForkWrapper target='_blank' href={this.props.href}>
      <i className='fab fa-github'></i>
    </GithubForkWrapper>
  }
}

