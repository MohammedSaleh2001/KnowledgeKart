import React, { createContext, useContext, useState } from 'react';

const ChatContext = createContext();

export const useChat = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
    const [activeChat, setActiveChat] = useState(null);

    const addMessageToActiveChat = (newMessage) => {
        if (!activeChat) return;  // If there is no active chat, do nothing!

        const updatedMessages = [...activeChat.messages, newMessage];

        setActiveChat({ ...activeChat, messages: updatedMessages });
    }

    return (
        <ChatContext.Provider value={{ activeChat, setActiveChat, addMessageToActiveChat }}>
            {children}
        </ChatContext.Provider>
    );
};