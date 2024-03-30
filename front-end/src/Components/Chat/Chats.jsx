import React, { useEffect, useState } from 'react'

import './Chat.css'

import ChatListing from './ChatListing'

const Chats = () => {

    const [chatListings, setChatListings] = useState([]);

    useEffect(() => {
        fetchChats();
    }, [])

    const fetchChats = async () => {
        const sample = [
            {id: 1, name: "Alpha"},
            {id: 2, name: "Beta"},
            {id: 3, name: "Charlie"}
        ];
        setChatListings(sample);
    }

    return (
        <div id="chats_container">
            {chatListings.map(listing => (
                <ChatListing key={listing?.id} name={listing?.name} />
            ))}
        </div>
    )
}

export default Chats;