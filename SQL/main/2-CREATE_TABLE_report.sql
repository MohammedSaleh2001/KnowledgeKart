CREATE TABLE IF NOT EXISTS report (
    ReportID SERIAL PRIMARY KEY,
    ReportBy int REFERENCES kkuser(UserID),
    ReportFor int REFERENCES kkuser(UserID),
    ReportText text,
    ModeratorAssigned int REFERENCES kkuser(UserID),
    ReportOpen boolean NOT NULL,
    Verdict text
)