
CREATE TABLE IF NOT EXISTS users(
    id integer primary key autoincrement,
    nome text not null
);

CREATE TABLE IF NOT EXISTS books(
    id integer primary key autoincrement,
    titulo text not null,
    user_id integer references users
);

CREATE TABLE IF NOT EXISTS filmes(
    id integer primary key autoincrement,
    titulo text not null,
    user_id integer references users
);