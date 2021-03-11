--======================================= 
-- ATIVIDADE 1 - AZURE (equivalente a Atividade 09)
-- Autor: Stephany Mackyne
-- Turma: Turma 5 - Engenharia de Dados. Accademia Accenture.
-- Data de entrega: até 06/03/2020
-- Descrição da atividade: Leitura de dados da API do IBGE, com o uso do package requests, para escrever em Banco de Dados 
-- relacional alocado no Azure os seguintes dados: UFs, Municípios (relacionados com UFs) e Distritos (relacionados com Municípios).
-- ======================================= 

use db2;

create table estados
(
	id int not null,
	sigla varchar(3) not null,
	nome varchar(25) not null,
	constraint pk_estados primary key (id)
);

create table municipios
(
	id int not null,
	nome varchar(45) not null,
	id_estado int not null,
	constraint pk_municipios primary key (id),
	constraint fk_municipios_estados foreign key (id_estado) 
	references estados (id)
);

create table distritos
(
	id int not null,
	nome varchar(45) not null,
	id_municipio int not null,
	constraint pk_distritos primary key (id),
	constraint fk_distritos_municipios foreign key (id_municipio) 
	references municipios (id)
);


