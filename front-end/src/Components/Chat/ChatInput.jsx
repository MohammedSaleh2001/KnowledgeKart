import React from 'react'

import './Chat.css'

const ChatInput = () => {
    return (
        <div id="chat_input_container">
            <input type="text" placeholder='Type something...' />
            <div>Send</div>
        </div>
    )
}

export default ChatInput;