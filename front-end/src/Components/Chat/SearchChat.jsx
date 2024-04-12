/*
Author: John Yu

Functional Requirements Fulfilled:
    - Refer to the ChatHomePage.jsx component.
*/

import React from 'react'
import './Chat.css'

const SearchChat = () => {
    return (
        <div id="search_chat_container">
            <input type="text" placeholder="Find a user" />
        </div>
    )
}

export default SearchChat