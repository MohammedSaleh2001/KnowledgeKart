import React, { useEffect, useState } from 'react'
import Message from './Message'

import './Chat.css'

const Messages = () => {

    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const fetchMessages = async () => {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/get_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({})
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.data);
                setMessages(data.data);
            }
        };

        fetchMessages();
    }, []);

    return (
        <div id="messages-container">
            {messages.map((message, index) => (
                <Message key={index} message={message.message} />
            ))}
        </div>
    )
}

export default Messages