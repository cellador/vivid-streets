import Modal from "./Modal.js";
import authFetch from '../helper/AuthFetch.jsx'
import { setCookie } from '../helper/Cookie.jsx'
import React, { Component } from 'react';

class AdminPanel extends Component {
  constructor(props) {
    super(props)
    this.state = {
      show: false
    };
  }

  toggleVisibility = () => {
    this.setState({ show: !this.state.show });
  };

  render() {
    return (
      <div>
        <button className="link-looking-button" onClick={this.toggleVisibility}>{this.props.children}</button>
        <Modal toggleVisibility={this.toggleVisibility} width="95%" height="95%" show={this.state.show}>
            ABC
        </Modal>
      </div>
    );
  }
}

export default AdminPanel;
