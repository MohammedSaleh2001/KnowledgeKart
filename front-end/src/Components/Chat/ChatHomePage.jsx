import React from 'react'

import './Chat.css'

import ChatSideBar from './ChatSideBar'
import ChatBar from './ChatBar'

const ChatHomePage = () => {
    return (
        <div id="chat_home_page_container">
            <ChatSideBar />
            <ChatBar />
        </div>
    )
}

export default ChatHomePage;