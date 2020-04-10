import Modal from "./Modal.js";
import { CONFIG } from '../config.js'
import React, { Component } from 'react';

class SignUp extends Component {

  constructor(props) {
    super(props)
    this.state = {
      show: false,
      email: "",
      password: "",
      confirm_password:"",
    };
  }

  check_available = () => {
    //stub for later, check if email is available or something
    return true;
  }

  switch = () => {
    this.setState({ show: !this.state.show });
  };

  signUp = () => {
    if (this.state.password !== this.state.confirm_password){
        console.log('Passwords do not match')
        return null;
      }
    else {
      console.log('Passwords match');
    }

    if (this.check_available()){
      console.log('Email is Available')
    }
    else {
      console.log('Email is already taken')
      return null;
    }


    const requestOptions = {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          email: this.state.email,
          password: this.state.password
        })
    };

    // Send the information to the database
    fetch( CONFIG.API_BASE_URL + '/register', 
          requestOptions)
        .then(async response => {
            const data = await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.status;
                return Promise.reject(error);
            }

            this.setState({ message: data.message });
            console.log(this.state.message);
        })
        .catch(error => {
            this.setState({ errorMessage: error });
            console.error('There was an error!', error);
        });


  };

  handleChangeEmail = (event) => {
    this.setState({email: event.target.value});
  };

  handleChangePassword = (event) => {
    this.setState({password: event.target.value});
  };

  handleChangeConfirmPassword = (event) => {
    this.setState({confirm_password: event.target.value});
  };

  render() {
    return (
      <div>
        <button className="link-looking-button" onClick={this.switch}>{this.props.children}</button>
        <Modal show={this.state.show}>
          Sign Up for an Account
          <button onClick={this.switch}>
            Close this shit!
          </button>
          <table><thead></thead>
          <tbody>
          <tr>
            <td> Email </td>
            <td>
              <input type="text" name="email" value={this.state.email} onChange={this.handleChangeEmail}>
              </input>
            </td>
          </tr>
          <tr>
            <td> Password </td>
            <td>
              <input type="password" name="password" value={this.state.password} onChange={this.handleChangePassword}>
              </input>
            </td>
          </tr>
          <tr>
            <td> Confirm Password </td>
            <td>
              <input type="password" name="confirm_password" value={this.state.confirm_password} onChange={this.handleChangeConfirmPassword}>
              </input>
            </td>
          </tr>
          </tbody>
          </table>
          <button onClick={this.signUp}>
          Sign Up
          </button>
          {this.state.message}
        </Modal>
      </div>
    );
  }
}

export default SignUp;
