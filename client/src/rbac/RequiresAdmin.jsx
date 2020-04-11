import React, { Component } from "react";

export default class RequiresAdmin extends Component {
    render() {
        if (!this.props.permissions.includes("admin")) return null;
        return(
            <div>
                {this.props.children}
            </div>
        );
    };
}