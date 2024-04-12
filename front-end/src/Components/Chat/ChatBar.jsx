/*
Author: John Yu

Functional Requirements Fulfilled:
    - Refer to the ChatHomePage.jsx component.
*/

import React from 'react'
import Messages from './Messages'
import ChatInput from './ChatInput'

import './Chat.css'

const ChatBar = ({ email }) => {
    const isUser = localStorage.getItem('roles') === 'U';

    return (
        <div id="chat_bar_container">
            <Messages email={email} />
            {isUser && <ChatInput />}
        </div>
    )
}

export default ChatBar;