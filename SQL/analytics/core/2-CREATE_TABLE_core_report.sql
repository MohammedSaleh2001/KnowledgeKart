CREATE TABLE IF NOT EXISTS core.report (
    ReportID SERIAL PRIMARY KEY,
    ReportBy int REFERENCES core.kkuser(UserID),
    ReportFor int REFERENCES core.kkuser(UserID),
    /*
    ReportText text,
    */
    ModeratorAssigned int REFERENCES core.kkuser(UserID),
    ReportOpen boolean NOT NULL
    /*
    Verdict text,
    */
)