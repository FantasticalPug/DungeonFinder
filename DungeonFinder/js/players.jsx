import React from 'react';
import PropTypes from 'prop-types';

class PlayerList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            players: [],
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
        let url = `/api/v1/games/players/?gameid=${this.props.gameid}`
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
            let players = []
            for (let i = 0; i < data.players.length; i += 1) {
                let link = `/users/${data.players[i].player}/`
                let keyL = `Player${i}L`
                let keyA = `Player${i}A`
                let keyB = `Player${i}B`
                players.push(
                    <li key={keyL}>
                        <a key={keyA} href={link} className="btn btn-secondary">{data.players[i].player}</a>  <button key={keyB} className="btn btn-danger" onClick={() => this.remove(data.players[i].player)}>Remove Adventurer</button>
                    </li>
                )
            }
            this.setState({
                players,
                avail: data.avail,
                slots: data.slots,
            });
        })
        .catch((error) => {
            console.log(error);
        });
        this.remove = this.remove.bind(this);
    }

    remove(player) {
        let url = `/api/v1/games/remove/?gameid=${this.props.gameid}&user=${player}`
        let method = 'DELETE'
        fetch(url, {
            method,
            credentials: 'same-origin',
        })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            let players = []
            for (let i = 0; i < data.players.length; i += 1) {
                let link = `/users/${data.players[i].player}/`
                let keyL = `Player${i}L`
                let keyA = `Player${i}A`
                let keyB = `Player${i}B`
                players.push(
                    <li key={keyL} className="react-list">
                        <a key={keyA} href={link} className="btn btn-secondary">{data.players[i].player}</a>  <button key={keyB} className="btn btn-danger" onClick={() => this.remove(data.players[i].player)}>Remove Adventurer</button>
                    </li>
                )
            }
            this.setState({
                players,
                avail: data.avail,
                slots: data.slots,
            });
        })
        .catch((error) => {
            console.log(error);
        });
    }

    render() {
        const {
            players,
            avail,
            slots,
        } = this.state;
        if (players.length === 0) {
            return (
                <span>
                    <div id="react-slots">Slots: {avail} / {slots}</div>
                    <h5 id="react-title" className="card-title">
                        Adventurers
                    </h5>
                    <ul>
                        <li className="react-list">No adventurers have joined your campaign yet</li>
                    </ul>
                </span>

            );
        }
        return (
            <span>
                <div id="react-slots">Slots: {avail} / {slots}</div>
                <h5 id="react-title" class="card-title">
                    Adventurers
                </h5>
                <ul>
                    {players}
                </ul>
            </span>
        );
    }

}

PlayerList.propTypes = {
    gameid: PropTypes.string.isRequired,
};

export default PlayerList;
