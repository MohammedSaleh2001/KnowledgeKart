import React, { useEffect, useState } from 'react'
import Message from './Message'
import { useChat } from '../../Context/ChatContext';

import './Chat.css'

const Messages = () => {

    const { activeChat } = useChat();

    console.log("ActiveChat:", activeChat);

    useEffect(() => {
        console.log("Active chat updated", activeChat);
    }, [activeChat])

    return (
        <div id="messages-container">
            {activeChat?.messages.map((msg, index) => (
                <Message key={index} message={msg.message} datesent={msg.datesent} />
            ))}
        </div>
    )
}

export default Messages