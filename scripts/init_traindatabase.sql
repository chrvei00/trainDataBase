CREATE TABLE
    Jernbanestasjon (
        navn TEXT NOT NULL,
        moh INTEGER NOT NULL,
        PRIMARY KEY (navn)
    );

CREATE TABLE
    Delstrekning (
        startstasjon_navn TEXT NOT NULL,
        endestasjon_navn TEXT NOT NULL,
        lengde INTEGER CHECK (lengde >= 0),
        antall_spor INTEGER CHECK (
            antall_spor = 1
            OR antall_spor = 2
        ),
        FOREIGN KEY (startstasjon_navn) REFERENCES Jernbanestasjon (navn),
        FOREIGN KEY (endestasjon_navn) REFERENCES Jernbanestasjon (navn),
        PRIMARY KEY (startstasjon_navn, endestasjon_navn)
    );

CREATE TABLE
    Banestrekning (
        navn TEXT PRIMARY KEY NOT NULL,
        startstasjon_navn TEXT NOT NULL,
        endestasjon_navn TEXT NOT NULL,
        fremdriftenergi TEXT CHECK (
            fremdriftenergi = 'elektrisk'
            OR fremdriftenergi = 'diesel'
        ),
        FOREIGN KEY (startstasjon_navn) REFERENCES Jernbanestasjon (navn),
        FOREIGN KEY (endestasjon_navn) REFERENCES Jernbanestasjon (navn)
    );

CREATE TABLE
    Strekker_over (
        banestrekning_navn TEXT NOT NULL,
        delstrekning_startstasjon TEXT NOT NULL,
        delstrekning_endestasjon TEXT NOT NULL,
        FOREIGN KEY (banestrekning_navn) REFERENCES Banestrekning (navn),
        FOREIGN KEY (
            delstrekning_startstasjon,
            delstrekning_endestasjon
        ) REFERENCES Delstrekning (startstasjon_navn, endestasjon_navn),
        PRIMARY KEY (
            banestrekning_navn,
            delstrekning_startstasjon,
            delstrekning_endestasjon
        )
    );

CREATE TABLE
    Togrute (
        togrute_id INTEGER NOT NULL,
        operator_navn TEXT NOT NULL,
        startstasjon TEXT NOT NULL,
        endestasjon TEXT NOT NULL,
        banestrekning_navn TEXT NOT NULL,
        FOREIGN KEY (operator_navn) REFERENCES Operator (operator_navn),
        FOREIGN KEY (startstasjon) REFERENCES Jernbanestasjon (navn),
        FOREIGN KEY (endestasjon) REFERENCES Jernbanestasjon (navn),
        FOREIGN KEY (banestrekning_navn) REFERENCES Banestrekning (navn),
        PRIMARY KEY (togrute_id)
    );

CREATE TABLE
    Togruteforekomst (
        togrute_id INTEGER NOT NULL,
        dato DATE NOT NULL,
        FOREIGN KEY (togrute_id) REFERENCES Togrute (togrute_id),
        PRIMARY KEY (togrute_id, dato)
    );

CREATE TABLE
    Rute_tid (
        ankomst_tid TIME NOT NULL,
        avgang_tid TIME NOT NULL,
        togrute_id INTEGER NOT NULL,
        jernbanestasjon_id TEXT NOT NULL,
        FOREIGN KEY (togrute_id) REFERENCES Togrute (togrute_id),
        FOREIGN KEY (jernbanestasjon_id) REFERENCES Jernbanestasjon (navn),
        PRIMARY KEY (
            ankomst_tid,
            avgang_tid,
            togrute_id,
            jernbanestasjon_id
        )
    );

CREATE TABLE
    Vognoppsett (
        vognoppsett_id INTEGER NOT NULL,
        PRIMARY KEY (vognoppsett_id)
    );

CREATE TABLE
    Operator (
        operator_navn TEXT NOT NULL,
        vogn_type TEXT CHECK (
            vogn_type = 'sitte'
            OR vogn_type = 'sove'
        ),
        PRIMARY KEY (operator_navn, vogn_type)
    );

CREATE TABLE
    Vogn (
        vogn_nummer INTEGER NOT NULL,
        vognoppsett_id INTEGER NOT NULL,
        vogn_type TEXT CHECK (
            vogn_type = 'sitte'
            OR vogn_type = 'sove'
        ),
        antall_plasser INTEGER CHECK (antall_plasser >= 0),
        antall_inndelinger INTEGER CHECK (antall_inndelinger >= 0),
        FOREIGN KEY (vognoppsett_id) REFERENCES Vognoppsett (vognoppsett_id),
        PRIMARY KEY (vogn_nummer, vognoppsett_id)
    );

CREATE TABLE
    Billett (
        vognoppsett_id INTEGER NOT NULL,
        vogn_nummer INTEGER NOT NULL,
        plass_nummer INTEGER NOT NULL,
        ordre_nummer INTEGER NOT NULL,
        FOREIGN KEY (vognoppsett_id) REFERENCES Vognoppsett (vognoppsett_id),
        FOREIGN KEY (vogn_nummer) REFERENCES Vogn (vogn_nummer),
        FOREIGN KEY (plass_nummer) REFERENCES Plass (plass_nummer),
        FOREIGN KEY (ordre_nummer) REFERENCES Kundeordre (ordre_nummer),
        PRIMARY KEY (
            vognoppsett_id,
            vogn_nummer,
            plass_nummer,
            ordre_nummer
        )
    );

CREATE TABLE
    Plass (
        vognoppsett_id INTEGER NOT NULL,
        vogn_nummer INTEGER NOT NULL,
        plass_nummer INTEGER CHECK (plass_nummer >= 1),
        er_soveplass INTEGER CHECK (
            er_soveplass = 0
            OR er_soveplass = 1
        ),
        inndeling_nummer INTEGER CHECK (inndeling_nummer >= 1),
        PRIMARY KEY (vognoppsett_id, vogn_nummer, plass_nummer)
    );

CREATE TABLE
    Kundeordre (
        ordre_nummer INTEGER NOT NULL,
        kjop_datotid DATETIME NOT NULL,
        kunde_nummer INTEGER NOT NULL,
        togruteforekomst_dato DATE NOT NULL,
        togrute_id INTEGER NOT NULL,
        pastigningstasjon_navn TEXT NOT NULL,
        avstigningstasjon_navn TEXT NOT NULL,
        FOREIGN KEY (kunde_nummer) REFERENCES Kunde (kunde_nummer),
        FOREIGN KEY (togruteforekomst_dato, togrute_id) REFERENCES Togruteforekomst (dato, togrute_id),
        FOREIGN KEY (pastigningstasjon_navn) REFERENCES Jernbanestasjon (navn),
        FOREIGN KEY (avstigningstasjon_navn) REFERENCES Jernbanestasjon (navn),
        PRIMARY KEY (ordre_nummer)
    );

CREATE TABLE
    Kunde (
        kunde_nummer INTEGER NOT NULL,
        navn TEXT NOT NULL,
        epost TEXT,
        mobilnummer INTEGER,
        PRIMARY KEY (kunde_nummer)
    );