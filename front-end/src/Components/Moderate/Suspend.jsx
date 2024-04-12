import React, { useEffect, useState } from 'react'

import { useNavigate, useParams } from "react-router-dom"

function Suspend() {
    const navigate = useNavigate();
    const { reportId } = useParams();
    const [report, setReport] = useState(null);
    const [hours, setHours] = useState(null);
    const [rationale, setRationale] = useState('');

    const handleCloseReport = async (rationale) => {
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
                    // verdict: "Report is closed. No one was at fault."
                    verdict: rationale
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
        const blacklistedUntil = new Date(new Date().getTime() + (hours * 60 * 60 * 1000)).toISOString();

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
                handleCloseReport(rationale);
                // window.location.reload();
            } else {
                console.log("Failed to suspend user.");
            }
        } catch (error) {
            console.error('Error suspending user:', error);
        }
    }

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
                if (response.ok && data.status === 'success') {
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

    return (
        <div id="suspend_container">
            <div id="title">
                Suspend
            </div>
            <div id="email_container">
                <input
                    type="email"
                    placeholder="Enter Email"
                    value={report?.report_for_email}
                    readOnly
                />
            </div>
            <div id="duration_container">
                <input
                    type="number"
                    placeholder="Enter Duration (in Hours)"
                    value={hours}
                    onChange={(e) => setHours(e.target.value)}
                />
            </div>
            <div id="rationale_container">
                <textarea
                    placeholder="Type Your Rationale"
                    value={rationale}
                    onChange={(e) => setRationale(e.target.value)}
                />
            </div>
            <div id="action_buttons_div">
                <button onClick={() => {
                    navigate(`/moderateinvestigate/${reportId}`)
                }}>Cancel</button>
                <button onClick={handleSuspendUser}>Submit</button>
            </div>
        </div>
    )
}

export default Suspend;