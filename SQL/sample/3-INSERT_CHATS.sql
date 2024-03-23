/* Sale 1 - Alice (6) to Joe (4) */ 

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

/* Sale 2 - Bob (5) to Tim (7) */

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    5,
    7,
    '2024-03-14 12:00:00'::TIMESTAMP,
    'Hi Bob, is this still available?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    7,
    5,
    '2024-03-14 12:05:00'::TIMESTAMP,
    'Yes it is. Come to HUB at 10 and buy it.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    5,
    7,
    '2024-03-14 12:30:00'::TIMESTAMP,
    'Um... ok? See you then I guess.'
);

/* Sale 3 - Bob (5) to Mark (8) */

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    5,
    8,
    '2024-03-15 14:00:00'::TIMESTAMP,
    'Hi Bob, is this still available?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    8,
    5,
    '2024-03-15 14:05:00'::TIMESTAMP,
    'Yes it is. Come to HUB at 10 and buy it.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    5,
    8,
    '2024-03-14 14:30:00'::TIMESTAMP,
    'Great! See you then.'
);

/* Sale 4 - Mark (8) to Tim (7) */

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    8,
    7,
    '2024-03-14 22:00:00'::TIMESTAMP,
    'Hey, do you still have the lab kit? Would you take 16?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    7,
    8,
    '2024-03-14 22:30:00'::TIMESTAMP,
    'Yes and yes. I will be in SUB tomorrow at 10. Swing by and it is yours.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    8,
    7,
    '2024-03-14 22:45:00'::TIMESTAMP,
    'Great! See you then.'
);

/* Sale 5 - Mark (8) to Alice (6) */

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    8,
    6,
    '2024-03-15 16:00:00'::TIMESTAMP,
    'I want the clothes.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    6,
    8,
    '2024-03-15 16:15:00'::TIMESTAMP,
    'Okay? How much are willing to pay?'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    8,
    6,
    '2024-03-15 16:20:00'::TIMESTAMP,
    '60.'
);

INSERT INTO chat (
    MessageTo,
    MessageFrom,
    DateSent,
    Message
) VALUES (
    6,
    8,
    '2024-03-15 16:22:00'::TIMESTAMP,
    'Deal! I will be on campus tomorrow. I will be sure to find you.'
);