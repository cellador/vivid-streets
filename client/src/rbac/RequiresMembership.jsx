import React, { Component } from "react";

export default class RequiresMembership extends Component {
    render() {
        if (!this.props.permissions.includes("member")) return null;
        return(
            <div>
                {this.props.children}
            </div>
        );
    };
}