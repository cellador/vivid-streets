import Modal from "./Modal.js";
import React, { Component } from 'react';

class SignUp extends Component {

  constructor(props) {
    super(props)
    this.state = {
      show: false
    };
  }

  switch = () => {
    this.setState({ show: !this.state.show });
  };

  render() {
    return (
      <div>
        <button className="bm-item menu-item" onClick={this.switch}>{this.props.children}</button>
        <Modal show={this.state.show}>Moe sucks big black dicks</Modal>
      </div>
    );
  }
}

export default SignUp;
