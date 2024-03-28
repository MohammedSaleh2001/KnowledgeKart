import React from 'react'

import { useParams } from 'react-router-dom'

import './Chat.css'

function ChatMessage() {

    const { chatID } = useParams();

    return (
        <>
        </>
    )
}

export default ChatMessage;