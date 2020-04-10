import Modal from "./Modal.js";
import authFetch from '../helper/AuthFetch.jsx'
import React, { Component } from 'react';

class Login extends Component {
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

  login = () => {
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
          Login to your account
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
          <button onClick={() => 
            this.props.setPermissions(
              authFetch("/auth", {
                method: 'POST',
                headers: { 
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                  email: this.state.email,
                  password: this.state.password
                })
              })
            )}>
          Login
          </button>
          {this.state.message}
        </Modal>
      </div>
    );
  }
}

export default Login;
