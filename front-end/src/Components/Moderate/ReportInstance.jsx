import React from 'react'

function ReportInstance() {
    return (
        <div id="report_instance_div">
            <div id="report_instance_info">
                <div id="report_instance_email">
                    Report: Insert Email Here
                </div>
                <div id="report_instance_date">
                    Date Reported: Insert Date Here
                </div>    
            </div>
            <div id="action_buttons_div">
                <div id="suspend_button">
                    Suspend
                </div>
                <div id="investigate_button">
                    Investigate
                </div>    
            </div>
        </div>
    )
}

export default ReportInstance;