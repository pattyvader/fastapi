CREATE TABLE musics (
    id serial PRIMARY KEY,
    title VARCHAR (200) NOT NULL,
    author TEXT [] NOT NULL,
    release_data DATE,
    keywords TEXT []
);

INSERT INTO musics(title,author,release_data,keywords) VALUES('Mr. Brightside','{"Flowers","Keuning"}','2003-01-01','{"indie","rock","post-punk","killers"}');
