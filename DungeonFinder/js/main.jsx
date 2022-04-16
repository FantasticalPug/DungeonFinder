import React from 'react';
import ReactDOM from 'react-dom';
import UnlinkDiscord from './unlink';
import ToggleJoin from './join';
import PlayerList from './players';
import Application from './application';

if (document.getElementById('unlink-react') != null) {
    ReactDOM.render(
        <UnlinkDiscord/>,
        document.getElementById('unlink-react'),
    );
} else if (document.getElementById('toggle-join') != null) {
    let gameid = window.location.href;
    gameid = gameid.split('/games/');
    gameid = gameid[1];
    gameid = gameid.replace('/', '');
    ReactDOM.render(
        <ToggleJoin gameid={gameid}/>,
        document.getElementById('toggle-join'),
    );
} else if (document.getElementById('players-react') != null) {
    let gameid = window.location.href;
    gameid = gameid.split('/games/');
    gameid = gameid[1];
    gameid = gameid.replace('/', '');
    ReactDOM.render(
        <PlayerList gameid={gameid}/>,
        document.getElementById('players-react'),
    );
} else if (document.getElementById('application-react') != null) {
    let gameid = window.location.href;
    gameid = gameid.split('/games/');
    gameid = gameid[1];
    gameid = gameid.replace('/apply/create/', '');
    ReactDOM.render(
        <Application gameid={gameid}/>,
        document.getElementById('application-react'),
    );
}
