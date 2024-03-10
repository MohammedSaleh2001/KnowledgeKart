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
                    UserRole,
                    Verified)
VALUES (
        'kkowner@ualberta.ca',
        'scrypt:32768:8:1$h4aU6IAbnMlGt8mi$ac5fc63d2fc4297b57f9209cfdc3b8378787c90ffc71a39e7a0384f3810523bc009de597dd7a79ed575ddeafeb8325f87ac3e8e2725fe70971539d0901615afe',
        'Owner' ,
        'O',
        True
);

INSERT INTO kkuser (Email,
                    HashPass,
                    FirstName,
                    UserRole,
                    Verified)
VALUES (
        'kkadmin@ualberta.ca',
        'scrypt:32768:8:1$ZSjbh863YzkeCobn$b948d3ad5b5defc114e8b596543c3127a780096460e75776cabab11e25b87e6175f4d502c7500210c7c94cbd48a35f13c8ad090f8bfc73389117b81539fd2e0b',
        'Admin' ,
        'A',
        True
);