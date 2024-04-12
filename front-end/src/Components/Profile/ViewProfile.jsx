/*
Author: John Yu

Functional Requirements Fulfilled:
    - FR5
*/

import React, { useEffect, useState } from 'react'

import { useNavigate, useParams } from 'react-router-dom'

import './Profile.css'

import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PortraitIcon from '@mui/icons-material/Portrait';

import { useChat } from '../../Context/ChatContext';

import ListingItem from '../Listing/ListingItem';

function ViewProfile() {

    const navigate = useNavigate();
    const { email } = useParams();
    const [userData, setUserData] = useState(null);
    const [rating, setRating] = useState();
    const [listings, setListings] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const loggedInUserEmail = localStorage.getItem('email');
    const loggedInUserRole = localStorage.getItem('roles');

    const { activeChat } = useChat();
    const { addMessageToActiveChat } = useChat();
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('/api/user_profile', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"email": email})
                });
                const data = await response.json();
                if (data.status === 'success') {
                    console.log("UserData", data.data);
                    setUserData(data.data)
                } else {
                    console.error('Failed to fetch user profile:', data.message);
                    navigate('/home');
                }
            } catch (error) {
                console.error('There was an error fetching the user profile:', error);
            }
        };

        const fetchListings = async () => {
            const token = localStorage.getItem('token');
            try {
                setIsLoading(true);
                const response = await fetch('/api/get_user_listings', {
                    method: 'POST',
                    cache: 'no-cache',
                    credentials: 'same-origin',
                    mode: 'cors',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "email": email })
                });
                if (!response.ok) {
                    throw new Error('Something went wrong!');
                }
                const data = await response.json();
                console.log("Profile listing is", data.data);
                setListings(data.data);
            } catch (error) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        }

        fetchUserData();
        fetchListings();
    }, [email]);

    useEffect(() => {
        if (userData) {
            try {
                const honesty = parseFloat(userData.honesty);
                const politeness = parseFloat(userData.politeness);
                const quickness = parseFloat(userData.quickness);

                const calculatedRating = (honesty + politeness + quickness) / 3;
                setRating(calculatedRating.toFixed(2));
            } catch (error) {
                console.error("Error calculating the user's rating!")
            }
        }
    }, [userData])

    const handleChatInitiation = async () => {
        const receiverEmail = email;
        const message = "Hello";
        const senderEmail = localStorage.getItem('email');

        const token = localStorage.getItem('token');

        try {
            const senderProfileResponse = await fetch('/api/user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: senderEmail }),
            });

            const senderProfileData = await senderProfileResponse.json();
            if (!senderProfileResponse.ok) {
                throw new Error('Failed to fetch sender profile');
            }

            const senderID = senderProfileData.data.userid;

            console.log("ReceiverEmail", receiverEmail);
            const receiverProfileResponse = await fetch('/api/user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: receiverEmail }),
            });

            const receiverProfileData = await receiverProfileResponse.json();
            if (!receiverProfileResponse.ok) {
                throw new Error('Failed to fetch receiver profile');
            }

            console.log("ReceiverProfileData:", receiverProfileData)

            const receiverID = receiverProfileData.data.userid;

            const newMessage = {
                from: senderID,
                to: receiverID,
                message: message,
                datasent: new Date().toISOString(),
            }

            const response = await fetch('/api/send_chat', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    receiver_email: receiverEmail,
                    message: message,
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
    }

    const isViewingOwnProfile = email === loggedInUserEmail;
    const isVerifiedUser = localStorage.getItem('roles') === 'U';

    return (
        <div id="view_profile_container">
            <div id="profile_header">
                <div id="view_profile_back_button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
                        // if (loggedInUserRole === 'U' ) {
                        if (['U', 'V', 'O', 'A'].includes(loggedInUserRole)) {
                            navigate('/home');    
                        } else if (loggedInUserRole === 'M') {
                            navigate(-1);
                        }
                    }} />
                </div>
                <div id="profile_title">
                    {userData?.firstname}'s Profile
                </div>
                {isViewingOwnProfile && (
                    <div id="edit_profile_button" style={{cursor: 'pointer'}} onClick={() => {
                        navigate(`/editprofile/${localStorage.getItem('email')}`)
                    }}>
                        Edit
                    </div>
                )}
            </div>
            <div id="about_container">
                <div id="about_container_title">About</div>
                <div id="about_container_body">
                    <div>
                        Name: {userData?.firstname}
                    </div>
                    <div>
                        Email: {email}
                    </div>
                    <div>
                        Status: {userData?.verified ? "Verified": "Unverified"}
                    </div>
                    <div>
                        Rating: {rating || "Not Available"}
                    </div>
                    <div>
                        Number of Reviews: {userData?.numreviews}
                    </div>
                    <div>
                        Honesty: {parseFloat(userData?.honesty).toFixed(2)}
                    </div>
                    <div>
                        Politeness: {parseFloat(userData?.politeness).toFixed(2)}
                    </div>
                    <div>
                        Quickness: {parseFloat(userData?.quickness).toFixed(2)}
                    </div>
                    {!isViewingOwnProfile && isVerifiedUser && (
                        <div id="view_profile_action_buttons">
                            <div id="view_profile_email_button">
                                Email
                            </div>
                            <div id="view_profile_chat_button" onClick={handleChatInitiation}>
                                Chat
                            </div>
                            <div id="view_profile_report_button" onClick={() => {
                                navigate(`/moderatereport/${email}`)
                            }}>
                                Report
                            </div>
                        </div>    
                    )}
                </div>
            </div>
            <div id="user_listing_container">
                <div id="user_listing_container_label">Listings</div>
                {listings.map(listing => (
                    <ListingItem key={listing.listingid} id={listing.listingid} title={listing.listing_name} price={listing.asking_price} />
                ))}
            </div>
        </div>
    )
}

export default ViewProfile;