import React, { useEffect, useState } from 'react'
import PortraitIcon from '@mui/icons-material/Portrait';

import './Chat.css'

const ChatListing = ({name}) => {

    return (
        <div id="chat_listing_container">
            <div id="chat_listing_portrait">
                <PortraitIcon style={{fontSize: 50}} />
            </div>
            <div id="chat_listing_info_div">
                <div id="chat_listing_info_div_name">{name}</div>
                <div id="chat_listing_info_div_last_msg">Last Message Goes Here</div>
            </div>
        </div>
    )
}

export default ChatListing;