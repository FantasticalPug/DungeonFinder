PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(30) NOT NULL,
    password VARCHAR(256) NOT NULL,
    email VARCHAR(50) NOT NULL,
    age int NOT NULL,
    favorites TEXT NOT NULL,
    bio TEXT NOT NULL,
    exper VARCHAR(20) NOT NULL,
    discord VARCHAR(30) NOT NULL,
    filename VARCHAR(64) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username)
);

CREATE TABLE games(
    gameid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    system VARCHAR(50) NOT NULL,
    tags TEXT NOT NULL,
    slots int NOT NULL,
    description TEXT NOT NULL,
    filename VARCHAR(64) NOT NULL,
    exper VARCHAR(20) NOT NULL,
    avail VARCHAR(120) NOT NULL,
    frequency VARCHAR(10) NOT NULL,
    must_apply int NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE sessions(
    sessionid INTEGER PRIMARY KEY AUTOINCREMENT,
    gameid int NOT NULL,
    player VARCHAR(20) NOT NULL,
    status VARCHAR(10) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(gameid) REFERENCES games(gameid) ON DELETE CASCADE,
    FOREIGN KEY(player) REFERENCES users(username) ON DELETE CASCADE
);
