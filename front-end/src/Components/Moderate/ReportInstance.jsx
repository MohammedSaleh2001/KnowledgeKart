import React from 'react'

import { useNavigate } from "react-router-dom"

function ReportInstance({ report }) {
    const navigate = useNavigate();

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
                <div id="suspend_button">
                    Suspend
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