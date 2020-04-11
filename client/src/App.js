import React, { Component } from 'react';
import { CONFIG } from './config.js'
import './App.css';
import GoogleMapReact from 'google-map-react';
import Menu from 'react-burger-menu/lib/menus/slide'
import RequiresMembership from './rbac/RequiresMembership.jsx'
import authFetch from './helper/AuthFetch'
import { setCookie, getCookie } from './helper/Cookie'
import SignUp from './modal/SignUp.js'
import Login from './modal/Login.js'

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
        this.setPermissions = this.setPermissions.bind(this);
        this.state = {
            locations: [],
            permissions: []
        };
    }

    static defaultProps = {
        center: {lat: 49.408508, lng:8.689848},
        zoom: 13
    };

    setPermissions(promise) {
        return promise.then((result) => {
            if(result['ok'] === true) {
                this.setState({permissions: result['roles']});
                return Promise.resolve({'status': true, 'roles': result['roles']});
            } else {
                this.setstate({permissions: []});
                return Promise.reject({'status': false});
            }
        }).catch((error) => {return error});
    }

    async componentDidMount() {

        // Restore old permissions
        const roles = getCookie("vs_roles");
        if(roles !== null) {
            this.setState({permissions: roles});
        }

        const queryString = objToQueryString({
            collection: "public",
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
            <div style={{ height: '100vh', width: '100%' }}>
                <Menu>
                    <SignUp className="menu-item">Sign Up</SignUp>
                    <Login setPermissions={this.setPermissions} className="menu-item">Login</Login>
                    <RequiresMembership permissions={this.state.permissions}>
                    <button className="link-looking-button" onClick={() => 
                        authFetch("/api/location?queryType=loc", {method: 'GET'})}>Need to be logged in</button>
                    </RequiresMembership>
                    <button className="link-looking-button" onClick={() => {
                        setCookie("vs_roles","",0);
                        this.setPermissions(authFetch("/logout", {method: 'POST'}));
                    }}>Logout</button>
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
