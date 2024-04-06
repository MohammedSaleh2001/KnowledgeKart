import React, { useEffect, useState } from 'react'

import ReportInstance from './ReportInstance'

import './Moderate.css'

function ModerateView() {
    const [reports, setReports] = useState([]);

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
                console.log("Reports data:", data.data);
                if (response.ok && data.status === 'success') {
                    const openReports = Object.values(data.data).filter(report => report.report_open);
                    setReports(openReports);
                } else {
                    console.error('Failed to fetch reports');
                }
            } catch (error) {
                console.error('Error fetching reports:', error);
            }
        };

        fetchReports();
    }, []);

    console.log("Reports:", reports);

    return (
        <div id="moderate_view_container">
            <div id="moderate_view_navbar">
                <div>
                    Report
                </div>
                <div>
                    Logout
                </div>
            </div>
            <div id="report_listings">
                {reports.map((report) => (
                    <ReportInstance key={report.reportid} report={report} />
                ))}
            </div>
        </div>
    )
}

export default ModerateView;