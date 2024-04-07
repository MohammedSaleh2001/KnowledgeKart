import React from 'react'
import Messages from './Messages'
import ChatInput from './ChatInput'

import './Chat.css'

const ChatBar = () => {
    const isUser = localStorage.getItem('roles') === 'U';

    return (
        <div id="chat_bar_container">
            <Messages />
            {isUser && <ChatInput />}
        </div>
    )
}

export default ChatBar;