import React, { useEffect, useState } from 'react'
import { useChat } from '../../Context/ChatContext';

import './Chat.css'

const ChatInput = () => {

    const { activeChat } = useChat();
    const { addMessageToActiveChat } = useChat();
    const [message, setMessage] = useState('');

    const sendMessage = async () => {
        if (!message.trim()) return;  // Prevent sending empty messages

        const senderEmail = localStorage.getItem('email');
        const token = localStorage.getItem('token');

        try {
            const userProfileResponse = await fetch('/api/user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: senderEmail }),
            });

            const userProfileData = await userProfileResponse.json();
            if (!userProfileResponse.ok) {
                throw new Error('Failed to fetch user profile');
            }

            const senderID = userProfileData.data.userid;

            const newMessage = {
                from: senderID,
                to: activeChat.id,
                message: message,
                datesent: new Date().toISOString(),
            }

            const response = await fetch('/api/send_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    receiver_email: activeChat.id,
                    message: message,
                }),
            });

            const data = await response.json();
            console.log(data);

            if (response.ok) {
                setMessage('');  // Clears the input field
                addMessageToActiveChat(newMessage);
            } else {
                console.error('Sending message failed:', data.message);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    return (
        <div id="chat_input_container">
            <input
                type="text"
                placeholder='Type something...'
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'ENTER' && sendMessage()}
            />
            <div onClick={sendMessage}>Send</div>
        </div>
    )
}

export default ChatInput;