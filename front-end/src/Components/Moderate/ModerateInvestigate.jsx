import React, { useEffect, useState } from 'react';

import { useNavigate, useParams } from 'react-router-dom'

import './Moderate.css'

function ModerateInvestigate() {
    const navigate = useNavigate();
    const { reportId } = useParams();
    const [report, setReport] = useState(null);

    const handleCloseReport = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('/api/close_report', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reportid: reportId,
                    verdict: "Report is closed. No one was at fault."
                }),
            });
            const data = await response.json();
            if (response.ok && data.status === 'success') {
                alert("Report closed successfully.");
                navigate('/moderateview');
            } else {
                console.error('Failed to close report');
            }
        } catch (error) {
            console.error('Error closing report:', error);
        }
    };

    useEffect(() => {
        const fetchReports = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('/api/get_reports', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({}),
                });
                const data = await response.json();
                if (response.ok && data.status == 'success') {
                    const specificReport = data.data[reportId];
                    if (specificReport) {
                        setReport(specificReport);
                    } else {
                        console.error('Report not found');
                        navigate('/moderateview');
                    }
                } else {
                    console.error('Failed to fetch reports');
                }
            } catch (error) {
                console.error('Error fetching reports:', error);
            }
        };

        fetchReports();
    }, [reportId, navigate])

    if (!report) {
        return <div>Loading...</div>
    }

    return (
        <div id="moderate_investigate_container">
            <div id="title">
                Investigation Form
            </div>
            <div id="email_container">
                <input type="email" placeholder="Enter Email" value={report.report_for_email} readonly="readonly"/>
            </div>
            <div id="textarea_container">
                <textarea placeholder="Type Your Rationale..." value={report.report_text} readonly="readonly"/>
            </div>
            <div id="action_buttons_div">
                <div onClick={() => {
                    navigate('/moderateview');
                }}>
                    Back
                </div>
                <div onClick={() => {
                    navigate(`/viewprofile/${report.report_for_email}`);
                }}>
                    View Profile
                </div>
                <div onClick={() => {
                    navigate(`/chat/${report.report_for_email}`)
                }}>
                    View Chat History
                </div>
                <div id="close_button" onClick={handleCloseReport}>
                    Close
                </div>
                <div id="suspend_button">
                    Suspend
                </div>
            </div>
        </div>
    )
}

export default ModerateInvestigate;