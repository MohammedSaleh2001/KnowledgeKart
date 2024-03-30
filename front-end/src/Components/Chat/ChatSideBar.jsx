import React from 'react'

import ChatNavBar from './ChatNavBar'
import SearchChat from './SearchChat'
import Chats from './Chats'

import './Chat.css'

const ChatSidebar = () => {
    return (
        <div id="chat_side_bar_container">
            <ChatNavBar />
            <SearchChat />
            <Chats />
        </div>
    )
}

export default ChatSidebar;