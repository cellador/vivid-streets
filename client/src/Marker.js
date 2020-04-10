import React, { Component } from 'react';
import Modal from "./modal/Modal.js";

class BusinessMarker extends Component {

  constructor(props) {
    super(props)
    this.state = {
      show_page: false,
    };
  }

  switch = () => {
    this.setState({ show_page: !this.state.show_page});
  };

  render(){
    return (
      <div>
        <button onClick={this.switch}>{this.props.text}</button>
        <BusinessPage show={this.state.show_page} close={this.switch}/>
      </div>
      )

  }
}

class BusinessPage extends Component {

  render(){
    console.log(this.props.show);
    return(
      <Modal show={this.props.show}>
      Welcome to the first BusinessPage!
      <button onClick={this.props.close}>
            Close this shit!
      </button>
      </Modal>
    )

  }
}

export default BusinessMarker;
