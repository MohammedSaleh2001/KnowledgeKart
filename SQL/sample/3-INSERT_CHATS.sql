INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    6,
    4,
    '2024-03-12 06:00:00'::TIMESTAMP,
    'Hi Alice, do you still have the ENGL textbook?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    4,
    6,
    '2024-03-12 07:00:00'::TIMESTAMP,
    'Hello Joe, I do.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    6,
    4,
    '2024-03-12 07:30:00'::TIMESTAMP,
    'Great, can we meet in ETLC at noon tomorrow?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    4,
    6,
    '2024-03-12 07:45:00'::TIMESTAMP,
    'Sure. See you then.'
);