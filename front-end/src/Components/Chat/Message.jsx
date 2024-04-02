import React from 'react'
import PortraitIcon from '@mui/icons-material/Portrait';

import './Chat.css'

const Message = ({message}) => {
    return (
        <div className="message-container owner">
            <div id="messageInfo">
                <div id="messageImage">
                    <PortraitIcon style={{fontSize: 40}} />
                </div>
                <div id="messageDate">
                    Just Now
                </div>
            </div>
            <div id="messageContent">
                {message}
            </div>
        </div>
    )
}

export default Message;