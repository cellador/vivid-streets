import React, { Component } from 'react';
import { CONFIG } from './config.js'
import './App.css';
import GoogleMapReact from 'google-map-react';
import Menu from 'react-burger-menu/lib/menus/slide'
import SignUp from './modal/SignUp.js'

const AnyReactComponent = ({ text }) => <div>{text}</div>;

function objToQueryString(obj) {
  const keyValuePairs = [];
  for (const key in obj) {
    keyValuePairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(obj[key]));
  }
  return keyValuePairs.join('&');
}

class App extends Component {
    constructor (props) {
        super(props);
        this.state = {
            locations: []
        };
    }

    static defaultProps = {
        center: {lat: 49.408508, lng:8.689848},
        zoom: 13
    };

    async componentDidMount() {

        const queryString = objToQueryString({
            queryType: "loc",
            latMin: -90,
            latMax: 90,
            longMin: -180,
            longMax: 180
        });

        fetch( CONFIG.API_BASE_URL + '/location?' + queryString)
            .then(async response => {
                const data = await response.json();

                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response statusText
                    const error = (data && data.message) || response.statusText;
                    return Promise.reject(error);
                }

                this.setState({locations: data});
            })
            .catch(error => {
                console.error('There was an error!', error);
            }
        );
    }

    render() {
        return (
            // Important! Always set the container height explicitly
            <div style={{ height: '80vh', width: '100%' }}>
                <Menu>
                    <a id="home" className="menu-item" href="/">Home</a>
                    <SignUp>Sign Up</SignUp>
                    <a id="about" className="menu-item" href="/about">About</a>
                    <a id="contact" className="menu-item" href="/contact">Contact</a>
                    <a onClick={ this.showSettings } className="menu-item--small" href="">Settings</a>
                </Menu>


                <GoogleMapReact
                    bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAPS_API_KEY }}
                    defaultCenter={this.props.center}
                    defaultZoom={this.props.zoom}
                >
                {this.state.locations.map((loc) => (
                    <AnyReactComponent key={loc._id}
                        lat={loc.latitude}
                        lng={loc.longitude}
                        text="My Marker"
                    />
                ))}
                </GoogleMapReact>


            </div>
        );
    }
}

export default App;
