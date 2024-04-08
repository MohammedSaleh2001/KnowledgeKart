import React from 'react'
import { useParams } from 'react-router-dom';
import { ChatProvider } from '../../Context/ChatContext';

import './Chat.css'

import ChatSideBar from './ChatSideBar'
import ChatBar from './ChatBar'

const ChatHomePage = () => {
    const { email } = useParams();

    return (
        <div id="chat_home_page_container">
            <ChatSideBar email={email} />
            <ChatBar email={email} />
        </div>
    )
}

export default ChatHomePage;