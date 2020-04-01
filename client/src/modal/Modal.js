import React, { Component } from 'react';
import ReactDOM from "react-dom";

const ModalInner = ({children, show}) =>
  <div className={show ? "display-block" : "display-none"}>
    {children}
  </div>
;

class Modal extends Component {

  constructor (props) {
    super(props);
    this.state = {
      show: true
    };
  }

  show = () => {
    this.setState({ show: true });
  };

  hide = () => {
    this.setState({ show: false });
  };

  render() {
    return ReactDOM.createPortal(
      <ModalInner show={this.state.show}> {this.props.html} </ModalInner>,
      document.querySelector("#modal")                      //target DOM element
    );
  }
}

export default Modal;
