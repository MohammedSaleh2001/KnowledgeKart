CREATE TABLE IF NOT EXISTS chat (
    MessageID SERIAL PRIMARY KEY,
    MessageTo int REFERENCES kkuser(UserID),
    MessageFrom int REFERENCES kkuser(UserID),
    DateSent timestamp NOT NULL,
    Message text NOT NULL
)