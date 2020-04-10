import React, { Component } from 'react';
import './Location.css';

// const Location = ({ text }) => <div>{text}</div>;

class Location extends Component {

  constructor (props) {
    super(props);
    this.state = {
      show_business_card: false
    };

  }

  openLocation = () => {this.setState({ show_business_card: true })}

  test = () => {console.log('IIIIIIIIII')}

  render(){
    if (this.state.show_business_card) {
      return (<BusinessCard></BusinessCard>)
      }
    return (
      <div className='location-button'>{this.props.text}</div>
    )
  }
}


class BusinessCard extends Component {
  render() {
    return (
      <div>This is a business card</div>
    )
  }
}


export default Location;
