CREATE TABLE IF NOT EXISTS report (
    ReportID SERIAL PRIMARY KEY,
    ReportBy int REFERENCES kkuser(UserID),
    ReportFor int REFERENCES kkuser(UserID),
    ReportText text,
    DateReported timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    ModeratorAssigned int REFERENCES kkuser(UserID),
    ReportOpen boolean NOT NULL,
    DateClosed timestamp,
    Verdict text
);

CREATE INDEX IF NOT EXISTS ix_report_reportby ON report (ReportBy);
CREATE INDEX IF NOT EXISTS ix_report_reportfor ON report (ReportFor);
CREATE INDEX IF NOT EXISTS ix_report_modassigned ON report (ModeratorAssigned);