import React from 'react'
import Messages from './Messages'
import ChatInput from './ChatInput'

import './Chat.css'

const ChatBar = () => {
    return (
        <div id="chat_bar_container">
            <Messages />
            <ChatInput />
        </div>
    )
}

export default ChatBar;