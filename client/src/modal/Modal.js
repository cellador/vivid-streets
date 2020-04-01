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
      show: this.props.show
    };
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    if (!prevState.show && nextProps.show) {
      return {
        show: true,
      };
    } else {
      return {
        show: false,
      };
    }
  }

  render() {
    if (!this.state.show) return null;
    return ReactDOM.createPortal(
      <ModalInner show={this.state.show}> {this.props.children} </ModalInner>,
      document.querySelector("#modal")                      //target DOM element
    );
  }
}

export default Modal;
