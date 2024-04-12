/*
Author: John Yu

Functional Requirements Fulfilled:
    - FR17
*/

import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom'

import { useNavigate } from "react-router-dom"; 

import './Moderate.css'

function ModerateReport() {
    const { email } = useParams();
    const navigate = useNavigate();

    const [rationale, setRationale] = useState('');

    const handleSubmit = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('/api/add_report', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    report_for: email,
                    message: rationale,
                }),
            });
            const data = await response.json();

            if (response.ok && data.status === 'success') {
                navigate('/home');
            } else {
                console.log('Failed to submit report');
            }
        } catch (error) {
            console.error('Error submitting report:', error);
        }
    }

    return (
        <div id="moderate_report_container">
            <div id="title">
                Report Form
            </div>
            <div id="input_email_container">
                <input
                    type="email"
                    placeholder="Enter Email"
                    value={email}
                    readOnly
                 />
            </div>
            <div id="textarea_container">
                <textarea placeholder="Type Your Rationale..."
                value={rationale}
                onChange={(e) => setRationale(e.target.value)}
             />
            </div>
            <div id="submit_button_div">
                <button onClick={() => {
                    navigate(`/viewprofile/${email}`)
                }}>Cancel</button>
                <button onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    )
}

export default ModerateReport;