CREATE DATABASE IF NOT EXISTS popular;
use popular;

CREATE TABLE obra (
  idobra int NOT NULL primary key AUTO_INCREMENT,
  idexterno varchar(16) not null,
  titulo varchar(200) not null,
  poster varchar(500) not null,
  ano int not null,
  duracao varchar(32),
  classificacao varchar(32),
  nota int null,
  tipo int not null,
  UNIQUE KEY un_obra_idexterno (idexterno)
);

CREATE TABLE leitura (
	idleitura int not null primary key auto_increment,
  data datetime not null,
  UNIQUE KEY un_leitura_data (data)
);

CREATE TABLE ranking (
	idranking int not null primary key auto_increment,
  idobra int not null,
  idleitura int not null,
  posicao int not null,
  UNIQUE KEY un_ranking_idleitura_idobra (idleitura, idobra),
  KEY ix_ranking_idobra (idobra),
  FOREIGN KEY fk_ranking_idobra (idobra) REFERENCES obra(idobra),
  FOREIGN KEY fk_ranking_idleitura (idleitura) REFERENCES leitura(idleitura)
);

CREATE TABLE favorito (
  idfavorito int NOT NULL primary key AUTO_INCREMENT,
  idobra int not null,
  UNIQUE KEY un_favorito_idobra (idobra),
  FOREIGN KEY fk_favorito_idobra (idobra) REFERENCES obra(idobra)
);
