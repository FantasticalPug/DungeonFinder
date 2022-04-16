import React from 'react';

class UnlinkDiscord extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            user: '',
            discord: '',
        };
    }

    componentDidMount() {
        let url = `/api/v1/users/discord/`
        let method = "GET"
        fetch(url, {
            method,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            this.setState({
                user: data.user,
                discord: data.discord,
            });
        })
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        let url = `/api/v1/users/unlink/`;
        let method = 'POST';
        fetch(url, {
            method,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            this.setState({
                discord: data.discord,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        event.preventDefault();
    }

    render() {
        const {
            discord,
        } = this.state;
        if (discord.length === 0) {
            return (
                <a href="https://discord.com/api/oauth2/authorize?client_id=953184670315589662&redirect_uri=https%3A%2F%2Fwww.thedungeonfinder.com%2Fdiscord%2F&response_type=code&scope=identify" className="btn btn-primary">Link Your Discord</a>
            );
        }
        return (
            <span>{discord} <button className="btn btn-danger" onClick={this.handleSubmit}>Unlink</button></span>
        )
    }

}

export default UnlinkDiscord;
