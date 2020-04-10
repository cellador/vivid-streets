import React, { Component } from 'react';
import Modal from "./modal/Modal.js";
import LSW_Image from "./tmp_images/LSW.jpg"

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
        <BusinessPage businessID={this.props.businessID} show={this.state.show_page} close={this.switch}/>
      </div>
      )

  }
}

class BusinessPage extends Component {

  constructor(props){
    super(props)
    this.state = {
      name: "",
      header: "",
      description: "",
      website:"",
      paypal:""
    };
  }

  async componentDidMount() {
    this.getData();
  }

  getData() {
    //somehow get data frombackend. For the moment: Fake it till you make it!
    this.setState({name:"Landessternwarte Heidelberg",
                   header:"Save the stars!",
                   description:"Hello fellow star lover! We were already broke before Corona but now we want to seize the chance and make some extra money! Make LSW great again!",
                   website:"https://www.lsw.uni-heidelberg.de/?lang=de",
                   paypal:"https://www.paypal.com/de/home"})
  }

  render(){
    // You probably should do that at another location
    // this.getData();
    return(
      <Modal show={this.props.show}>
        <button onClick={this.props.close}>
          Close this shit!
        </button>

        <header>
          <h1>
            {this.state.name}
          </h1>
          <img src={LSW_Image} width="200" height="200"/>
        </header>


        <div class="mainBusiness">
          <h2>
            {this.state.header}
          </h2>
          <body>
            {this.state.description}
          </body>
        </div>

        <footer>
          <tr>
            <td> Our Website </td>
            <td> <a href={this.state.website}> {this.state.website} </a> <  /td>
          </tr>
          <tr>
            <td> Our PayPal Link </td>
            <td>  <a href={this.state.paypal}> {this.state.paypal} </a> </td>
          </tr>
        </footer>

      </Modal>
    )

  }
}

export default BusinessMarker;
