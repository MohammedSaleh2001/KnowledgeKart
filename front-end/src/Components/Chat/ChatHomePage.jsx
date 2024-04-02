import React from 'react'
import { ChatProvider } from './ChatContext';

import './Chat.css'

import ChatSideBar from './ChatSideBar'
import ChatBar from './ChatBar'

const ChatHomePage = () => {
    return (
        <ChatProvider>
            <div id="chat_home_page_container">
                <ChatSideBar />
                <ChatBar />
            </div>    
        </ChatProvider>
    )
}

export default ChatHomePage;