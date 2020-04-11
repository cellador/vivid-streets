import { CONFIG } from '../config.js'
import Modal from "./Modal.js";
import objToQueryString from '../helper/objToQueryString'
import React, { Component } from 'react';

const AnyReactComponent = ({ text }) => <div>{text}</div>;

class InnerPanel extends Component {
    constructor (props) {
        super(props);
        this.state = {
            staged_locations: []
        };
    }

    async componentDidMount() {
        const queryString = objToQueryString({
            collection: "public", // TODO this are public locations
            queryType: "loc",
            latMin: -90,
            latMax: 90,
            longMin: -180,
            longMax: 180
        });

        // TODO THIS FETCH IS NOT SECURED AT THE MOMENT
        fetch( CONFIG.API_BASE_URL + '/location?' + queryString)
            .then(async response => {
                const data = await response.json();

                // check for error response
                if (!response.ok) {
                    // get error message from body or default to response statusText
                    const error = (data && data.message) || response.statusText;
                    return Promise.reject(error);
                }

                this.setState({staged_locations: data});
            })
            .catch(error => {
                console.error('There was an error!', error);
            }
        );
    }
    
    render() {
        return(
            this.state.staged_locations.map((loc) => (
                <AnyReactComponent text="My Marker"/>
            ))
        );
    }
}

class AdminPanel extends Component {
    constructor(props) {
        super(props)
        this.state = {
            show: false
        };
    }

    toggleVisibility = () => {
        this.setState({ show: !this.state.show });
    };

    render() {
        return (
            <div>
                <button className="link-looking-button" onClick={this.toggleVisibility}>{this.props.children}</button>
                <Modal toggleVisibility={this.toggleVisibility} width="95%" height="95%" show={this.state.show}>
                    <InnerPanel />
                </Modal>
            </div>
        );
    }
}

export default AdminPanel;
