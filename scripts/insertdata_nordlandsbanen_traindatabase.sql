/* Insert Nodrlandsbanen int Database */
--
/* Brukerhistorie a) */
/* Jernbanestasjoner */
INSERT INTO
    Jernbanestasjon (navn, moh)
VALUES
    ('Bodø', 4.1),
    ('Fauske', 34),
    ('Mo i Rana', 3.5),
    ('Mosjøen', 6.8),
    ('Steinkjer', 3.6),
    ('Trondheim S', 5.1);

/* Delstrekninger */
INSERT INTO
    Delstrekning (
        startstasjon_navn,
        endestasjon_navn,
        lengde,
        antall_spor
    )
VALUES
    ('Bodø', 'Fauske', 60, 1),
    ('Fauske', 'Mo i Rana', 170, 1),
    ('Mo i Rana', 'Mosjøen', 90, 1),
    ('Mosjøen', 'Steinkjer', 280, 1),
    ('Steinkjer', 'Trondheim S', 120, 2);

/* Banestrekninger */
INSERT INTO
    Banestrekning (
        navn,
        startstasjon_navn,
        endestasjon_navn,
        fremdriftenergi
    )
VALUES
    ('Nordlandsbanen', 'Bodø', 'Trondheim S', 'diesel');

/* Strekker over */
INSERT INTO
    Strekker_over (
        banestrekning_navn,
        delstrekning_startstasjon,
        delstrekning_endestasjon
    )
VALUES
    ('Nordlandsbanen', 'Bodø', 'Fauske'),
    ('Nordlandsbanen', 'Fauske', 'Mo i Rana'),
    ('Nordlandsbanen', 'Mo i Rana', 'Mosjøen'),
    ('Nordlandsbanen', 'Mosjøen', 'Steinkjer'),
    ('Nordlandsbanen', 'Steinkjer', 'Trondheim S');

--
/* Brukerhistorie b) */
/* Operator */
INSERT INTO
    Operator (operator_navn)
VALUES
    ('SJ');

/* Operator typer */
INSERT INTO
    Operator_typer (operator_navn, vogn_type)
VALUES
    ('SJ', 'sitte'),
    ('SJ', 'sove');

/* Vognoppsett */
INSERT INTO
    Vognoppsett (vognoppsett_id)
VALUES
    (1),
    (2),
    (3);

/* Togruter */
INSERT INTO
    Togrute (
        togrute_id,
        operator_navn,
        startstasjon,
        endestasjon,
        banestrekning_navn,
        togrute_navn,
        vognoppsett_id
    )
VALUES
    (
        1,
        'SJ',
        'Trondheim S',
        'Bodø',
        'Nordlandsbanen',
        'Dagtog',
        1
    ),
    (
        2,
        'SJ',
        'Trondheim S',
        'Bodø',
        'Nordlandsbanen',
        'Nattog',
        2
    ),
    (
        3,
        'SJ',
        "Mo i Rana",
        "Trondheim S",
        "Nordlandsbanen",
        "Morgentog",
        3
    );

--
/* Brukerhistorie f) */
/* Togruteforekomster */
INSERT INTO
    Togruteforekomst (togrute_id, dato)
VALUES
    (1, '2023-04-03'),
    (1, '2023-04-04'),
    (2, '2023-04-03'),
    (2, '2023-04-04'),
    (3, '2023-04-03'),
    (3, '2023-04-04');

/* Rutetid */
INSERT INTO
    Rute_tid (
        ankomst_tid,
        avgang_tid,
        togrute_id,
        jernbanestasjon_navn
    )
VALUES
    -- Dagtog Trondheim Bodø 
    ('07:39', '07:49', 1, 'Trondheim S'),
    ('09:41', '09:51', 1, 'Steinkjer'),
    ('13:10', '13:20', 1, 'Mosjøen'),
    ('14:21', '14:31', 1, 'Mo i Rana'),
    ('16:39', '16:49', 1, 'Fauske'),
    ('17:24', '17:34', 1, 'Bodø'),
    -- Nattog Trondheim Bodø
    ('22:55', '23:05', 2, 'Trondheim S'),
    ('00:47', '00:57', 2, 'Steinkjer'),
    ('04:31', '04:41', 2, 'Mosjøen'),
    ('05:45', '05:55', 2, 'Mo i Rana'),
    ('08:09', '08:19', 2, 'Fauske'),
    ('08:55', '09:05', 2, 'Bodø'),
    -- Morgentog Mo i Rana Trondheim
    ('08:01', '08:11', 3, 'Mo i Rana'),
    ('09:04', '09:14', 3, 'Mosjøen'),
    ('12:21', '12:31', 3, 'Steinkjer'),
    ('14:03', '14:13', 3, 'Trondheim S');