import React, { useEffect, useState } from 'react'

import { useParams } from 'react-router-dom'

import './Profile.css'

import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PortraitIcon from '@mui/icons-material/Portrait';

import { useNavigate } from "react-router-dom";

import { useChat } from '../../Context/ChatContext';

function ViewProfile() {

    const navigate = useNavigate();
    const { email } = useParams();
    const [userData, setUserData] = useState(null);
    const loggedInUserEmail = localStorage.getItem('email');

    const { activeChat } = useChat();
    const { addMessageToActiveChat } = useChat();
    const [message, setMessage] = useState('');

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

    const handleChatInitiation = async () => {
        const receiverEmail = email;
        const message = "Hello";
        const senderEmail = localStorage.getItem('email');

        const token = localStorage.getItem('token');

        try {
            const senderProfileResponse = await fetch('/api/user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: senderEmail }),
            });

            const senderProfileData = await senderProfileResponse.json();
            if (!senderProfileResponse.ok) {
                throw new Error('Failed to fetch sender profile');
            }

            const senderID = senderProfileData.data.userid;

            console.log("ReceiverEmail", receiverEmail);
            const receiverProfileResponse = await fetch('/api/user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: receiverEmail }),
            });

            const receiverProfileData = await receiverProfileResponse.json();
            if (!receiverProfileResponse.ok) {
                throw new Error('Failed to fetch receiver profile');
            }

            console.log("ReceiverProfileData:", receiverProfileData)

            const receiverID = receiverProfileData.data.userid;

            const newMessage = {
                from: senderID,
                to: receiverID,
                message: message,
                datasent: new Date().toISOString(),
            }

            const response = await fetch('/api/send_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    receiver_email: receiverEmail,
                    message: message,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                navigate(`/chat/${senderEmail}`);
            } else {
                console.error('Failed to initiate chat:', data.message);
            }
        } catch (error) {
            console.error('Error initiating chat:', error);
        }
    }

    const isViewingOwnProfile = email === loggedInUserEmail;

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
                    {!isViewingOwnProfile && (
                        <div id="view_profile_action_buttons">
                            <div id="view_profile_email_button">
                                Email
                            </div>
                            <div id="view_profile_chat_button" onClick={handleChatInitiation}>
                                Chat
                            </div>
                            <div id="view_profile_report_button">
                                Report
                            </div>
                        </div>    
                    )}
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