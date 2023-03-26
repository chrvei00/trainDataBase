/* Test Jernbanestasjon */
INSERT INTO
    Jernbanestasjon (navn, moh)
VALUES
    ('Oslo N', 23),
    ('Bergen stasjon', 3),
    ('Trondheim stasjon', 2),
    ('Stavanger stasjon', 7),
    ('Drammen stasjon', 10),
    ('Kristiansand stasjon', 1);

/* Test Delstrekning */
INSERT INTO
    Delstrekning (
        startstasjon_navn,
        endestasjon_navn,
        lengde,
        antall_spor
    )
VALUES
    ('Oslo S', 'Drammen stasjon', 42, 2),
    ('Drammen stasjon', 'Oslo S', 42, 2),
    ('Bergen stasjon', 'Stavanger stasjon', 213, 1),
    ('Stavanger stasjon', 'Bergen stasjon', 213, 1),
    ('Trondheim stasjon', 'Oslo S', 500, 2),
    ('Oslo S', 'Trondheim stasjon', 500, 2),
    ('Stavanger stasjon', 'Trondheim stasjon', 800, 1),
    ('Bergen stasjon', 'Drammen stasjon', 320, 1),
    ('Drammen stasjon', 'Bergen stasjon', 320, 1),
    ('Drammen stasjon', 'Kristiansand stasjon', 320, 1),
    ('Trondheim stasjon', 'Stavanger stasjon', 800, 1);

/* Test Banestrekning */
INSERT INTO
    Banestrekning (
        navn,
        startstasjon_navn,
        endestasjon_navn,
        fremdriftenergi
    )
VALUES
    (
        'Oslo-Bergen',
        'Oslo S',
        'Bergen stasjon',
        'elektrisk'
    ),
    (
        'Trondheim-Stavanger',
        'Trondheim stasjon',
        'Stavanger stasjon',
        'diesel'
    ),
    (
        'Drammen-Kristiansand',
        'Drammen stasjon',
        'Kristiansand stasjon',
        'elektrisk'
    );

/* Test Strekker over */
INSERT INTO
    Strekker_over (
        banestrekning_navn,
        delstrekning_startstasjon,
        delstrekning_endestasjon
    )
VALUES
    ('Oslo-Bergen', 'Oslo S', 'Drammen stasjon'),
    (
        'Oslo-Bergen',
        'Drammen stasjon',
        'Bergen stasjon'
    ),
    (
        'Drammen-Kristiansand',
        'Drammen stasjon',
        'Kristiansand stasjon'
    );

/* Test Operatør */
INSERT INTO
    Operator (operator_navn)
VALUES
    ('NSB'),
    ('VY'),
    ('YV');

/* Test Operator_types */
INSERT INTO
    Operator_typer (operator_navn, vogn_type)
VALUES
    ('NSB', 'sitte'),
    ('NSB', 'sove'),
    ('VY', 'sitte'),
    ('YV', 'sove');

/* Test Togrute */
INSERT INTO
    Togrute (
        togrute_id,
        operator_navn,
        startstasjon,
        endestasjon,
        banestrekning_navn
    )
VALUES
    (
        1,
        'NSB',
        'Oslo S',
        'Bergen stasjon',
        'Oslo-Bergen'
    ),
    (
        2,
        'VY',
        'Drammen stasjon',
        'Kristiansand stasjon',
        'Drammen-Kristiansand'
    ),
    (
        3,
        'YV',
        'Trondheim stasjon',
        'Stavanger stasjon',
        'Trondheim-Stavanger'
    );

/* Test Togruteforekomst */
INSERT INTO
    Togruteforekomst (togrute_id, dato)
VALUES
    (1, '2023-03-15'),
    (2, '2023-03-16'),
    (3, '2023-03-17');

/* Test Rutetid */
INSERT INTO
    Rute_tid (
        ankomst_tid,
        avgang_tid,
        dager_etter_avgangsdato,
        togrute_id,
        jernbanestasjon_navn
    )
VALUES
    ('08:00', '08:15', 0, 1, 'Oslo S'),
    ('09:30', '09:45', 0, 1, 'Drammen stasjon');

/* Test Vognoppsett */
INSERT INTO
    Vognoppsett (vognoppsett_id)
VALUES
    (1),
    (2),
    (3),
    (4),
    (5);

/* Test Vogn */
INSERT INTO
    Vogn (
        vogn_nummer,
        vognoppsett_id,
        vogn_type,
        antall_plasser,
        antall_inndelinger
    )
VALUES
    (1, 1, 'sitte', 50, 0),
    (2, 1, 'sove', 10, 2),
    (1, 2, 'sitte', 30, 0),
    (2, 2, 'sove', 20, 1),
    (1, 3, 'sitte', 40, 0);

/* Test Plass */
INSERT INTO
    Plass (
        vognoppsett_id,
        vogn_nummer,
        plass_nummer,
        inndeling_nummer
    )
VALUES
    (1, 1, 1, 1),
    (1, 1, 2, 1),
    (1, 1, 3, 1),
    (1, 1, 4, 2),
    (1, 1, 5, 2),
    (1, 2, 1, 1),
    (1, 2, 2, 1),
    (1, 2, 3, 1),
    (1, 2, 4, 2),
    (1, 2, 5, 2);

/* Test Kunde */
INSERT INTO
    Kunde (kunde_nummer, navn, epost, mobilnummer)
VALUES
    (1, 'Ola Nordmann', 'ola@example.com', 12345678),
    (2, 'Kari Nordmann', 'kari@example.com', 87654321),
    (3, 'Per Hansen', 'per@example.com', 12345278),
    (4, 'Lise Olsen', 'lise@example.com', 66665555),
    (5, 'Lise Olsen', 'lise@example2.com', 66665555);

/* Test Kundeordre */
INSERT INTO
    Kundeordre (
        ordre_nummer,
        kjop_datotid,
        kunde_nummer,
        togruteforekomst_dato,
        togrute_id,
        pastigningstasjon_navn,
        avstigningstasjon_navn
    )
VALUES
    (
        1,
        '2023-03-14 15:00:00',
        1,
        '2023-03-15',
        1,
        'Oslo S',
        'Trondheim stasjon'
    ),
    (
        2,
        '2023-03-19 18:00:00',
        4,
        '2023-03-16',
        2,
        'Bergen stasjon',
        'Kristiansand stasjon'
    ),
    (
        3,
        '2023-03-21 10:00:00',
        1,
        '2023-03-17',
        3,
        'Oslo S',
        'Bergen stasjon'
    ),
    (
        4,
        '2023-03-24 16:30:00',
        2,
        '2023-03-15',
        1,
        'Trondheim stasjon',
        'Oslo S'
    );

/* Test Billett */
INSERT INTO
    Billett (
        vognoppsett_id,
        vogn_nummer,
        plass_nummer,
        ordre_nummer
    )
VALUES
    (1, 1, 1, 2),
    (1, 1, 2, 1),
    (1, 1, 3, 3),
    (1, 1, 4, 2),
    (1, 1, 5, 2),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 4),
    (1, 2, 4, 2),
    (1, 2, 5, 3);