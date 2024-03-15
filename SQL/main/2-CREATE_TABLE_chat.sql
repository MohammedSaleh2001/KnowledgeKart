CREATE TABLE IF NOT EXISTS chat (
    MessageID SERIAL PRIMARY KEY,
    MessageTo int REFERENCES kkuser(UserID),
    MessageFrom int REFERENCES kkuser(UserID),
    DateSent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    Message text NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_chat_messageto ON chat (MessageTo);
CREATE INDEX IF NOT EXISTS ix_chat_messagefrom ON chat (MessageFrom);