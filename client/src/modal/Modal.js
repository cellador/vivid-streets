import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './Modal.css';

const ModalInner = ({toggleVisibility,width,height,children}) =>
  <div className="modal-wrapper">
    <div className="modal-inner" style={{width: width || "", height: height || ""}}>
      <button className="modal-close" onClick={toggleVisibility}>X</button>
      {children}
    </div>
  </div>
;

class Modal extends Component {
  render() {
    if (!this.props.show) return null;
    return ReactDOM.createPortal(
      <ModalInner {...this.props}> {this.props.children} </ModalInner>,
      document.querySelector("#modal")
    );
  }
}

export default Modal;
