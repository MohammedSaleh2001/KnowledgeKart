import React from 'react';

import { useParams } from 'react-router-dom'

import { useNavigate } from "react-router-dom"; 

import './Moderate.css'

function ModerateReport() {

    const { email } = useParams();

    const navigate = useNavigate();

    const handleSubmit = () => {
        navigate('/home');
    }

    return (
        <div id="moderate_report_container">
            <div id="title">
                Report Form
            </div>
            <div id="input_email_container">
                <input type="email" placeholder="Enter Email" />
            </div>
            <div id="textarea_container">
                <textarea placeholder="Type Your Rationale..." />
            </div>
            <div id="submit_button_div">
                <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    )
}

export default ModerateReport;