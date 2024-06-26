CREATE TABLE IF NOT EXISTS core.report (
    ReportID int PRIMARY KEY,
    ReportBy int REFERENCES core.kkuser(UserID),
    ReportFor int REFERENCES core.kkuser(UserID),
    /*
    ReportText text,
    */
    DateReported timestamp NOT NULL,
    /* DATETIME FKs */
    DateReportedFK bigint,
    TimeReportedFK varchar,

    ModeratorAssigned int REFERENCES core.kkuser(UserID),
    ReportOpen boolean NOT NULL,
    DateClosed timestamp,
    /* DATETIME FKs */
    DateClosedFK bigint,
    TimeClosedFK varchar,
    
    /*
    Verdict text
    */

    /* DERIVED FIELDS */
    TimeToClose int
);

CREATE INDEX IF NOT EXISTS ix_report_reportby ON core.report (ReportBy);
CREATE INDEX IF NOT EXISTS ix_report_reportfor ON core.report (ReportFor);
CREATE INDEX IF NOT EXISTS ix_report_modassigned ON core.report (ModeratorAssigned);