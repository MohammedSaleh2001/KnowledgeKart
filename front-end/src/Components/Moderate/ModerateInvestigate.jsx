import React from 'react';

import { useNavigate, useParams } from 'react-router-dom'

import './Moderate.css'

function ModerateInvestigate() {

    const navigate = useNavigate();

    const { email } = useParams();

    return (
        <div id="moderate_investigate_container">
            <div id="title">
                Investigation Form
            </div>
            <div id="email_container">
                <input type="email" placeholder="Enter Email" value={email} readonly="readonly"/>
            </div>
            <div id="textarea_container">
                <textarea placeholder="Type Your Rationale..." readonly="readonly"/>
            </div>
            <div id="action_buttons_div">
                <div onClick={() => {
                    navigate('/moderateview');
                }}>
                    Back
                </div>
                <div onClick={() => {
                    navigate(`/viewprofile/${email}`);
                }}>
                    View Profile
                </div>
                <div onClick={() => {
                    navigate(`/chat/${email}`)
                }}>
                    View Chat History
                </div>
                <div id="suspend_button">
                    Suspend
                </div>
            </div>
        </div>
    )
}

export default ModerateInvestigate;