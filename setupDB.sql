-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    fecha_union TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tema_stats JSONB -- JSONB para almacenar los porcentajes de aciertos por tema
);

-- Tabla de partidas
CREATE TABLE partidas (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    fecha_partida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tema_stats JSONB -- JSONB para almacenar el número de aciertos y preguntas por tema
);
