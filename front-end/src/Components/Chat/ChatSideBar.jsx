/*
Author: John Yu

Functional Requirements Fulfilled:
    - Refer to the ChatHomePage.jsx component.
*/

import React from 'react'
import ChatNavBar from './ChatNavBar'
import SearchChat from './SearchChat'
import Chats from './Chats'

import './Chat.css'

const ChatSidebar = ({ email }) => {
    return (
        <div id="chat_side_bar_container">
            <ChatNavBar />
            <SearchChat />
            <Chats email={email} />
        </div>
    )
}

export default ChatSidebar;