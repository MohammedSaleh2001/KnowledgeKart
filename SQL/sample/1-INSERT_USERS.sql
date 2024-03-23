INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    Verified,
                    Politeness,
                    Honesty,
                    Quickness ,
                    NumReviews)
VALUES (
        'joe@ualberta.ca',
        'scrypt:32768:8:1$mqzzrOdVkti91GPx$9ba27b6ffcec3d27f969417c7aaaee1a92cc8146cd23fda4338b7aec3bdbf9c644197e1e526af66e96855c47c66f491c06db7fd014111d123cb29913d294b54c',
        'Joe' ,
        '2024-03-11'::TIMESTAMP,
        True,
        2.0,
        4.0,
        5.0,
        1
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    Verified,
                    Politeness,
                    Honesty,
                    Quickness ,
                    NumReviews)
VALUES (
        'bob@ualberta.ca',
        'scrypt:32768:8:1$CgUw9tiEIWslxXRB$45b21a74e0887546efe76493ab4e3e50f3b6c7badde37271ac345f6dc5a34b4607b18dab17ced187f9e1224479e29c98c52a1b3ba0218dd12b760bc33524b05e',
        'Bob' ,
        '2024-03-11'::TIMESTAMP,
        True,
        2.5,
        3.0,
        3.0,
        2
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    Verified,
                    Politeness,
                    Honesty,
                    Quickness ,
                    NumReviews)
VALUES (
        'alice@ualberta.ca',
        'scrypt:32768:8:1$EvBhwYdiOu755xPh$29c7a0e151dc007162c341bf450db3c03a03bcd0ac312f9a050d5a24c036273048ee709314ca6ee342989cfffbb93cf8b11af4a817768fa10f4d2cce3b62d53c',
        'Alice' ,
        '2024-03-11'::TIMESTAMP,
        True,
        1.0,
        1.0,
        1.0,
        2
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    Verified,
                    Politeness,
                    Honesty,
                    Quickness ,
                    NumReviews)
VALUES (
        'tim@ualberta.ca',
        'scrypt:32768:8:1$TAZ6ReRdnE248DrA$70e200a6acb1aac622b21c34105fdf1364cff2a9b68d20ca4e7c255e8b7e88831355d0c96071dce8fe415984905d9af217a9b21dfe3e8e31e9e939eae5832408',
        'Tim' ,
        '2024-03-11 12:00:00'::TIMESTAMP,
        True,
        4.5,
        4.0,
        5.0,
        2
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    Verified,
                    Politeness,
                    Honesty,
                    Quickness ,
                    NumReviews)
VALUES (
        'mark@ualberta.ca',
        'scrypt:32768:8:1$jzyI37XPkq6Bqwtj$00ae0171b3a25c52f116a5e281df860126d789046e28f6013dc3c27e27c651d5a06a6a3b7b35f026526f4daa05e21074f33278fc802d84bbec1295c01f450d25',
        'Mark' ,
        '2024-03-11 18:00:00'::TIMESTAMP,
        True,
        5.0,
        5.0,
        5.0,
        3
);

/* 

Sale 1 - Alice to Joe
Sale 2 - Bob to Tim
Sale 3 - Bob to Mark
Sale 4 - Mark to Tim
Sale 5 - Mark to Alice

*/
