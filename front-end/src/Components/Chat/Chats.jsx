import React, { useEffect, useState } from 'react'
import { useChat } from '../../Context/ChatContext';

import './Chat.css'

import ChatListing from './ChatListing'

const Chats = () => {

    const { setActiveChat } = useChat();

    const [chatListings, setChatListings] = useState([]);

    useEffect(() => {
        fetchChats();
    }, [])

    const fetchChats = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/get_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            const chatsArray = Object.keys(data.data).map(key => {
                return { id: key, name: key, messages: data.data[key] };
            });

            setChatListings(chatsArray);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    const handleChatClick = (listing) => {
        console.log("Chat clicked:", listing);
        setActiveChat(listing);
    };

    return (
        <div id="chats_container">
            {chatListings.map(listing => (
                <ChatListing key={listing.id} name={listing.name} onClick={() => handleChatClick(listing)} />
            ))}
        </div>
    )
}

export default Chats;