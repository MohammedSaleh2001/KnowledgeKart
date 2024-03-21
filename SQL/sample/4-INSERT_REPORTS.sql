INSERT INTO report (    
    ReportBy ,
    ReportFor ,
    ReportText,
    DateReported,
    ModeratorAssigned,
    ReportOpen,
    DateClosed,
    Verdict
) VALUES (
    4,
    6,
    'Alice was a complete scammer! She had posted her textbook for 10 dollars, and when it came time to sell it, she tried to convince me it was listed for 30! I got it for 10, but still.',
    '2024-03-13 12:30:00'::TIMESTAMP,
    3,
    False,
    '2024-03-13 16:00:00'::TIMESTAMP,
    'Even though she was difficult, eventually she gave you the correct price. Please leave a poor rating and proceed.'
)