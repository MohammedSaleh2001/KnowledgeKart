import React, { useEffect, useState } from 'react'
import PortraitIcon from '@mui/icons-material/Portrait';

import { useNavigate } from "react-router-dom";  

import './Chat.css'

const ChatNavbar = () => {

    const navigate = useNavigate();

    const [userName, setUserName] = useState('');

    useEffect(() => {
        const fetchUserProfile = async () => {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/user_profile', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUserName(data.data.firstname);
            }
        }

        fetchUserProfile();
    }, [])

    return (
        <div id="chat_nav_bar_container">
            <span style={{cursor: 'pointer'}} onClick={() => {
                navigate('/home')
            }}>Home</span>
            <div>
                <div id="chat_nav_bar_portrait_icon_div">
                    <PortraitIcon style={{fontSize: 40}} />
                </div>
                <div id="chat_nav_bar_user_name">{userName}</div>
            </div>
        </div>
    )
}

export default ChatNavbar;