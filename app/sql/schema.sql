create table brands(
    id BIGSERIAL PRIMARY KEY,
    nume TEXT NOT NULL,
    logo TEXT NOT NULL,
    website_url TEXT NOT NULL,
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table produse(
    id BIGSERIAL PRIMARY KEY,
    nume TEXT NOT NULL,
    pret NUMERIC(10,2) NOT NULL,
    descriere TEXT,
    tip_produs TEXT NOT NULL,
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    brand_id BIGINT REFERENCES brands(id) ON DELETE CASCADE,
    durata_garantie INTERVAL NOT NULL DEFAULT '24 months',
    imagini TEXT[] NOT NULL,
    slug TEXT NOT NULL UNIQUE
);

create table laptopuri(
    id BIGINT PRIMARY KEY REFERENCES produse(id) ON DELETE CASCADE,
    procesor TEXT NOT NULL,
    placa_video TEXT NOT NULL,
    capacitate_ram_gb INTEGER NOT NULL CHECK (capacitate_ram > 0),
    capacitate_stocare_gb INTEGER NOT NULL CHECK (capacitate_stocare > 0),
    sistem_de_operare TEXT NOT NULL,
    greutate_kg NUMERIC(5,2) NOT NULL CHECK (greutate_kg > 0),
    dimensiune_ecran_inch NUMERIC(4,2) NOT NULL CHECK (dimensiune_ecran_inch > 0),
    rezolutie_ecran TEXT NOT NULL
);

create table procesoare(
    id BIGINT PRIMARY KEY REFERENCES produse(id) ON DELETE CASCADE,
    numar_nuclee INTEGER NOT NULL CHECK (numar_nuclee > 0),
    frecventa_ghz NUMERIC(4,2) NOT NULL CHECK (frecventa_ghz > 0),
    putere_disipata_watts INTEGER NOT NULL CHECK (putere_disipata_watts > 0)
);

create table placi_video(
    id BIGINT PRIMARY KEY REFERENCES produse(id) ON DELETE CASCADE,
    memorie_gb INTEGER NOT NULL CHECK (memorie_gb > 0),
    tip_memorie TEXT NOT NULL,
    frecventa_memorie_mhz INTEGER NOT NULL CHECK (frecventa_memorie_mhz > 0),
    interfata_memorie TEXT NOT NULL
);

create table categorii(
    id BIGSERIAL PRIMARY KEY,
    nume TEXT NOT NULL,
    descriere TEXT NOT NULL,
    culoare varchar(7) NOT NULL CHECK (culoare ~ '^#[0-9A-Fa-f]{6}$'),
    sigla TEXT NOT NULL,
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table produse_categorii(
    produs_id BIGINT REFERENCES produse(id) ON DELETE CASCADE,
    categorie_id BIGINT REFERENCES categorii(id) ON DELETE CASCADE,
    PRIMARY KEY (produs_id, categorie_id)
);

create table promotii(
    id BIGSERIAL PRIMARY KEY,
    nume TEXT NOT NULL,
    descriere TEXT NOT NULL,
    data_inceput TIMESTAMP NOT NULL,
    data_sfarsit TIMESTAMP NOT NULL,
    discount NUMERIC(3) NOT NULL CHECK (discount >= 0 AND discount <= 100),
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table produse_promotii(
    produs_id BIGINT REFERENCES produse(id) ON DELETE CASCADE,
    promotie_id BIGINT REFERENCES promotii(id) ON DELETE CASCADE,
    PRIMARY KEY (produs_id, promotie_id)
);

create table depozite(
    id BIGSERIAL PRIMARY KEY,
    nume TEXT NOT NULL UNIQUE,
    adresa_id BIGINT REFERENCES adresa(id) ON DELETE CASCADE,
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table adresa(
    id BIGSERIAL PRIMARY KEY,
    strada TEXT NOT NULL,
    oras TEXT NOT NULL,
    judet TEXT NOT NULL,
    cod_postal TEXT NOT NULL,
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table stocuri(
    produs_id BIGINT REFERENCES produse(id) ON DELETE CASCADE,
    depozit_id BIGINT REFERENCES depozite(id) ON DELETE CASCADE,
    cantitate INTEGER NOT NULL CHECK (cantitate >= 0),
    data_adaugare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (produs_id, depozit_id)
);