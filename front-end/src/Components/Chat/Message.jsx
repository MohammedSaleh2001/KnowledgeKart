/*
Author: John Yu

Functional Requirements Fulfilled:
    - Refer to the ChatHomePage.jsx component.
*/

import React from 'react'
import PortraitIcon from '@mui/icons-material/Portrait';
import './Chat.css'

const Message = ({message, datesent, sentByCurrentUser}) => {
    const messageContainerClass = `message-container ${sentByCurrentUser ? 'owner' : ''}`

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-CA', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false,
            timeZone: 'America/Edmonton',
            timeZoneName: 'short',
        }).format(date);
    };

    return (
        <div className={messageContainerClass}>
            <div id="messageTop">
                <div id="messageImage">
                    <PortraitIcon style={{fontSize: 40}} />
                </div>
                <div id="messageContent">
                    {message}    
                </div>
            </div>
            <div id="messageBottom">
                <div id="messageDate">
                    {/* {datesent} */}
                    {formatDate(datesent)}
                </div>
            </div>
        </div>
    )
}

export default Message;