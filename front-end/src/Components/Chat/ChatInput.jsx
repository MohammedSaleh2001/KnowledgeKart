import React, { useEffect, useState } from 'react'
import { useChat } from './ChatContext';

import './Chat.css'

const ChatInput = () => {

    const { activeChat } = useChat();
    const { addMessageToActiveChat } = useChat();
    const [message, setMessage] = useState('');

    const sendMessage = async () => {
        if (!message.trim()) return;  // Prevent sending empty messages

        const newMessage = {
            from: 'SenderID',
            to: activeChat.id,
            message: message,
            datasent: new Date().toISOString(),
        }

        const token = localStorage.getItem('token');

        try {
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