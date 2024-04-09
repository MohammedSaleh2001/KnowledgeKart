import React from 'react'

import { useNavigate } from "react-router-dom"

function ReportInstance({ report }) {
    const navigate = useNavigate();

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
                    reportid: report.reportid,
                    verdict: "Report is closed. No one was at fault."
                }),
            });
            const data = await response.json();
            if (response.ok && data.status === 'success') {
                navigate('/moderateview');
                window.location.reload();
            } else {
                console.error('Failed to close report');
            }
        } catch (error) {
            console.error('Error closing report:', error);
        }
    };

    const handleSuspendUser = async () => {
        const token = localStorage.getItem('token');
        const blacklistedUntil = new Date(new Date().getTime() + (72 * 60 * 60 * 1000)).toISOString();
        try {
            const response = await fetch('/api/suspend_user', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: report.report_for_email,
                    blacklist: true,
                    blacklisted_until: blacklistedUntil,
                }),
            });
            const data = await response.json();
            if (response.ok && data.status === 'success') {
                handleCloseReport();
                alert("User succesfully suspended.");
                navigate('/moderateview');
                window.location.reload();
            } else {
                console.log("Failed to suspend user.");
            }
        } catch (error) {
            console.error('Error suspending user:', error);
        }
    }

    return (
        <div id="report_instance_div">
            <div id="report_instance_info">
                <div id="report_instance_email">
                    Report: {report.report_for_email}
                </div>
                <div id="report_instance_date">
                    Date Reported: {report.date_reported}
                </div>    
            </div>
            <div id="action_buttons_div">
                <div id="suspend_button" onClick={() => {
                    navigate(`/suspend/${report.reportid}`)
                }}>
                    Suspend
                </div>
                <div id="close_button" onClick={handleCloseReport}>
                    Close
                </div>
                <div id="investigate_button" onClick={() => {
                    navigate(`/moderateinvestigate/${report.reportid}`);
                }}>
                    Investigate
                </div>    
            </div>
        </div>
    )
}

export default ReportInstance;