CREATE TABLE IF NOT EXISTS kkuser (
    UserID SERIAL PRIMARY KEY,
    Email varchar UNIQUE, 
    HashPass varchar NOT NULL,
    FirstName varchar NOT NULL,
    DateJoined timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    UserRole char NOT NULL DEFAULT 'U', /* A (Admin), M (Moderator), O (Owner), U (User) */
    Verified boolean NOT NULL DEFAULT False,
    Blacklist boolean NOT NULL DEFAULT False,
    BlacklistedUntil timestamp,

    Politeness numeric NOT NULL DEFAULT 0,
    Honesty numeric NOT NULL DEFAULT 0,
    Quickness numeric NOT NULL DEFAULT 0,
    NumReviews int NOT NULL DEFAULT 0
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    UserRole,
                    Verified)
VALUES (
        'kkowner@ualberta.ca',
        'scrypt:32768:8:1$h4aU6IAbnMlGt8mi$ac5fc63d2fc4297b57f9209cfdc3b8378787c90ffc71a39e7a0384f3810523bc009de597dd7a79ed575ddeafeb8325f87ac3e8e2725fe70971539d0901615afe',
        'Owner' ,
        '2024-03-10'::TIMESTAMP,
        'O',
        True
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    UserRole,
                    Verified)
VALUES (
        'kkadmin@ualberta.ca',
        'scrypt:32768:8:1$ZSjbh863YzkeCobn$b948d3ad5b5defc114e8b596543c3127a780096460e75776cabab11e25b87e6175f4d502c7500210c7c94cbd48a35f13c8ad090f8bfc73389117b81539fd2e0b',
        'Admin' ,
        '2024-03-10'::TIMESTAMP,
        'A',
        True
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    DateJoined,
                    UserRole,
                    Verified)
VALUES (
        'kkmod@ualberta.ca',
        'scrypt:32768:8:1$ii77GqgwKwDcoVUC$c8710a13643e5ed9cc2eb770f2f8c5e45610746581270f1f412f01c7cc5c389da64bc8fa795981c25526bf29f12a3151aa2eb5863045a51f5822c53133e633d0',
        'Moderator' ,
        '2024-03-10'::TIMESTAMP,
        'M',
        True
);