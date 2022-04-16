import React from 'react';
import PropTypes from 'prop-types';

class ToggleJoin extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            joined: false,
            gameid: '',
            avail: '',
            slots: '',
        };
    }

    componentDidMount() {
        const {
            gameid,
        } = this.props;
        this.setState({
            gameid,
        });
        let url = `/api/v1/games/status/?gameid=${this.props.gameid}`
        let method = 'GET'
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
                joined: data.joined,
                avail: data.avail,
                slots: data.slots,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        this.join = this.join.bind(this);
        this.leave = this.leave.bind(this);
    }

    join(event) {
        let url = `/api/v1/games/join/?gameid=${this.state.gameid}`
        let method = 'POST'
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
                joined: data.joined,
                avail: data.avail,
                slots: data.slots,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        event.preventDefault();
    }

    leave(event) {
        let url = `/api/v1/games/leave/?gameid=${this.state.gameid}`
        let method = 'POST'
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
                joined: data.joined,
                avail: data.avail,
                slots: data.slots,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        event.preventDefault();
    }

    render() {
        const {
            joined,
            avail,
            slots,
        } = this.state;
        if (joined) {
            return (
                <span>Adventurers: {avail} / {slots} <button className="btn btn-danger" onClick={this.leave}>Leave</button></span>
            );
        }
        return (
            <span>Adventurers: {avail} / {slots} <button className="btn btn-primary" onClick={this.join}>Join</button></span>
        );
    }

}

ToggleJoin.propTypes = {
    gameid: PropTypes.string.isRequired,
};

export default ToggleJoin;
