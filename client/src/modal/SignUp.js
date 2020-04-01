import Modal from "./Modal.js";
import React, { Component } from 'react';


class SignUp extends Component {

  render() {
    return (
      <div>
        <button onClick={Modal.hide}> Button </button>
        <Modal
          html='Moe sucks big black dicks'
        />
      </div>
    );
  }
}

export default SignUp;
