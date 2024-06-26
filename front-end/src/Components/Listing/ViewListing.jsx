/*
Author: John Yu

Functional Requirements Fulfilled:
    - FR8 (Also fulfilled by the HomePage.jsx component)
    - FR9 (Also fulfilled by all components in the Chat folder)
    - FR10
    - FR12
*/

import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import './Listing.css'

import PortraitIcon from '@mui/icons-material/Portrait';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PhotoIcon from '@mui/icons-material/Photo';
import SendIcon from '@mui/icons-material/Send';

import { useNavigate } from "react-router-dom";  

function Listing() {

    const navigate = useNavigate();

    const { listingId } = useParams();

    // Initialize states
    const [listing, setListing] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [rating, setRating] = useState();
    const [isOwner, setIsOwner] = useState(false);
    const [status, setStatus] = useState("Open");
    const [chatMsg, setChatMsg] = useState("");
    const [category, setCategory] = useState("Other");

    useEffect(() => {
        const fetchListing = async () => {
            const token = localStorage.getItem('token');
            setIsLoading(true);
            try{
                const response = await fetch(`/api/listing_profile`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        listingid: listingId
                    })
                });
                if (!response.ok) {
                    throw new Error('Could not fetch listing data');
                }
                const data = await response.json();
                console.log("Listing:", data.data);
                setListing(data.data);
                setIsOwner(data.data.seller.email === localStorage.getItem('email'));
                switch (data.data.listingstatus) {
                    case 'O':
                        setStatus("Open");
                        break;
                    case 'C':
                        setStatus("Closed");
                        break;
                    case 'S':
                        setStatus("Sold");
                        break;
                    default:
                        setStatus('Open');
                        break;
                }
                switch (data.data.category_type) {
                    case 1:
                        setCategory("Other");
                        break;
                    case 2:
                        setCategory("Textbook");
                        break;
                    case 3:
                        setCategory("Lab Equipment");
                        break;
                    default:
                        setCategory("Other");
                        break;
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchListing();
    }, [listingId]);

    useEffect(() => {
        if (listing) {
            try {
                const honesty = parseFloat(listing.seller.honesty);
                const politeness = parseFloat(listing.seller.politeness);
                const quickness = parseFloat(listing.seller.quickness);
                const calculatedRating = (honesty + politeness + quickness) / 3;
                setRating(calculatedRating.toFixed(2));
            } catch (error) {
                console.error("Error calculating the user's rating!")
            }
        }
    }, [listing]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    const initiateChatWithSeller = async () => {
        const receiverEmail = listing?.seller?.email;
        const message = chatMsg;
        console.log("Message:", message);
        const senderEmail = localStorage.getItem('email');

        if (!receiverEmail) {
            console.error("Receiver email not found.");
            return;
        }
        
        const token = localStorage.getItem('token');

        try {
            const response = await fetch('/api/send_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    receiver_email: receiverEmail,
                    message,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                navigate(`/chat/${senderEmail}`);
            } else {
                console.error('Failed to initiate chat:', data.message);
            }
        } catch (error) {
            console.error('Error initiating chat:', error);
        }

        // ----- Send email notification to seller ----- //
        try {
            const response = await fetch('/api/send_contact_email', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "buyer": senderEmail,
                    "seller": receiverEmail,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                ;
            } else {
                console.error('Failed to send email notification to seller:', data.message);
            }
        } catch (error) {
            console.error('Error sending email notification:', error);
        }
    }

    const handleEmailSeller = () => {
        if (listing && listing.seller && listing.seller.email) {
            const mailToLink = `mailto:${listing.seller.email}?body=${chatMsg}`;
            window.location.href = mailToLink;
        }
    }

    const handleViewProfileButton = () => {
        if (listing && listing.seller && listing.seller.email) {
            navigate(`/viewprofile/${listing.seller.email}`)
        }
    }

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

    const isNotVerified = localStorage.getItem('roles') === 'V';

    return (
        <div id="view_listing_container">
            <div id="listing_header">
                <div id="listing_back_button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
                        navigate("/home")
                    }} />
                </div>
                <div id="listing_edit_button">
                    {isOwner && <div id="edit_button" onClick={() => {
                            navigate(`/editlisting/${listingId}`);
                        }}>
                            Edit
                        </div>    
                    }
                </div>
            </div>
            <div id="about_container">
                <div id="listing_title">
                    {listing?.listing_name || "Untitled Listing"}    
                </div>
                <div id="about_container_body">
                    <div id="listing_price_div">
                        Price: {"$" + listing?.asking_price || "N/A"}  
                    </div>   
                    <div id="listing_condition_div">
                        Condition: {listing?.condition || "N/A"}
                    </div> 
                    <div>
                        Status: {status}
                    </div>
                    <div>
                        Category: {category}
                    </div>
                    <div id="listing_date_div">
                        Date Listed: {formatDate(listing?.date_listed) || "Not Available"}    
                    </div>
                    {!isOwner && !isNotVerified && (<div id="listing_chat_div">
                        <input
                            type="text"
                            placeholder="Chat with the seller"
                            value={chatMsg}
                            onChange={e => setChatMsg(e.target.value)}
                        />
                        <SendIcon id="send_icon" onClick={initiateChatWithSeller} />
                    </div>)}
                </div>
            </div>
            <div id="listing_description_container">
                <div id="listing_description_label">
                    Description
                </div>
                <div id="listing_description_body">
                    {listing?.listing_description || ""}
                </div>
            </div>
            <div id="seller_container">
                <div id="seller_container_label">
                    Seller Information
                </div>
                <div id="seller_container_body">
                    <div id="seller_name_div">
                        Name: {listing?.seller?.firstname || "Seller Name"}
                    </div>  
                    <div>
                        Verified: {listing?.seller?.verified ? "Yes" : "No"}
                    </div>
                    <div id="listing_rating_div">
                        Rating: {rating || "N/A"}
                    </div>
                    <div>
                        Number of Reviews: {listing?.seller?.numreviews}
                    </div>
                    <div>
                        Honesty: {parseFloat(listing?.seller?.honesty).toFixed(2)}
                    </div>
                    <div>
                        Politeness: {parseFloat(listing?.seller?.politeness).toFixed(2)}
                    </div>
                    <div>
                        Quickness: {parseFloat(listing?.seller?.quickness).toFixed(2)}
                    </div>
                    <div id="seller_info_buttons_container">
                        {!isOwner && !isNotVerified && (<div id="listing_email_div" onClick={handleEmailSeller}>
                            Email
                        </div>)}   
                        {!isOwner && (<div id="listing_view_profile_div" onClick={handleViewProfileButton}>View Profile</div>)}    
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Listing