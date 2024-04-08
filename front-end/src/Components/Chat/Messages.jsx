import React, { useEffect, useState } from 'react'
import Message from './Message'
import { useChat } from '../../Context/ChatContext';

import './Chat.css'

const Messages = ({ email }) => {

    const { activeChat } = useChat();

    const [currentUserId, setCurrentUserId] = useState(null);

    useEffect(() => {
        const fetchCurrentUserId = async () => {
            const token = localStorage.getItem('token');

            try {
                const response = await fetch('/api/user_profile', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({"email": email }),
                });

                const data = await response.json();

                if (response.ok) {
                    setCurrentUserId(data.data.userid);
                } else {
                    throw new Error('Failed to fetch current user profile');
                }
            } catch (error) {
                console.error('Error fetching current user ID:', error);
            }
        }

        fetchCurrentUserId();
    }, []);

    return (
        <div id="messages-container">
            {activeChat?.messages.map((msg, index) => (
                <Message key={index} message={msg.message} datesent={msg.datesent} sentByCurrentUser={msg.from === currentUserId} />
            ))}
        </div>
    )
}

export default Messages