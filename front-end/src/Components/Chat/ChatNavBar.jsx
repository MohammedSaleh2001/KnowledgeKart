import React from 'react'
import PortraitIcon from '@mui/icons-material/Portrait';

import './Chat.css'

const ChatNavbar = () => {
    return (
        <div id="chat_nav_bar_container">
            <span>KK Chat</span>
            <div>
                <div id="chat_nav_bar_portrait_icon_div">
                    <PortraitIcon style={{fontSize: 40}} />
                </div>
                <div id="chat_nav_bar_user_name">Insert Name</div>
            </div>
        </div>
    )
}

export default ChatNavbar;