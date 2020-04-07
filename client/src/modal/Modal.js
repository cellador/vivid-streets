import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './Modal.css';

const ModalInner = ({children}) =>
  <div class="modal-wrapper">
    <div class="modal-inner">
      {children}
    </div>
  </div>
;

class Modal extends Component {
  // constructor (props) {
  //   super(props);
  //   this.state = {
  //     show: this.props.show
  //   };
  // }

  // static getDerivedStateFromProps(nextProps, prevState) {
  //   if (!prevState.show && nextProps.show) {
  //     return {
  //       show: true,
  //     };
  //   } else {
  //     return {
  //       show: false,
  //     };
  //   }
  // }

  render() {
    if (!this.props.show) return null;
    return ReactDOM.createPortal(
      <ModalInner> {this.props.children} </ModalInner>,
      document.querySelector("#modal")                      //target DOM element
    );
  }
}

export default Modal;
