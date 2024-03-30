import React, { useEffect, useState } from 'react'

import { useParams } from 'react-router-dom'

import './Profile.css'

import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PortraitIcon from '@mui/icons-material/Portrait';

import { useNavigate } from "react-router-dom";  

function ViewProfile() {

    const navigate = useNavigate();
    const { email } = useParams();
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('/api/user_profile', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                if (data.status === 'success') {
                    setUserData(data.data)
                } else {
                    console.error('Failed to fetch user profile:', data.message);
                    navigate('/home');
                }
            } catch (error) {
                console.error('There was an error fetching the user profile:', error);
            }
        };

        fetchUserData();
    }, [email]);

    return (
        <div id="view_profile_container">
            <div id="view_profile_top">
                <div id="view_profile_back_button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
                        navigate('/home');
                    }} />
                </div>
                <div id="edit_profile_button" onClick={() => {
                    navigate(`/editprofile/${localStorage.getItem('email')}`)
                }}>
                    Edit Profile
                </div>
            </div>
            <div id="view_profile_mid">
                <div id="view_profile_mid_left">
                    <PortraitIcon style={{fontSize: 250}}/>
                </div>
                <div id="view_profile_mid_mid">
                    <div id="view_profile_seller_name">
                        {userData?.firstname}
                    </div>
                    <div id="view_profile_seller_email">
                        {email}
                    </div>
                    <div id="view_profile_rating">
                        Insert Rating
                    </div>
                    <div id="view_profile_action_buttons">
                        <div id="view_profile_email_button">
                            Email
                        </div>
                        <div id="view_profile_chat_button">
                            Chat
                        </div>
                        <div id="view_profile_report_button">
                            Report
                        </div>
                    </div>
                </div>
                <div id="view_profile_mid_right">
                    Description:<br />
                </div>
            </div>
            <div id="view_profile_bot">

            </div>
        </div>
    )
}

export default ViewProfile;