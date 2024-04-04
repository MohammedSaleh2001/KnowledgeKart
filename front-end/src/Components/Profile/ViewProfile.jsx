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
                    method: 'GET',
                    cache: 'no-cache',
                    credentials: 'same-origin',
                    mode: 'cors',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
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
                const numreviews = userData.numreviews;

                const calculatedRating = (honesty + politeness + quickness + numreviews) / 4;
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

    return (
        <div id="view_profile_container">
            <div id="view_profile_top">
                <div id="view_profile_back_button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
                        navigate('/home');
                    }} />
                </div>
                {isViewingOwnProfile && (
                    <div id="edit_profile_button" onClick={() => {
                        navigate(`/editprofile/${localStorage.getItem('email')}`)
                    }}>
                        Edit Profile
                    </div>
                )}
            </div>
            <div id="view_profile_mid">
                <div id="view_profile_mid_left">
                    <PortraitIcon style={{fontSize: 250}}/>
                </div>
                <div id="view_profile_mid_mid">
                    <div id="view_profile_seller_name">
                        {userData?.firstname}
                    </div>
                    <div id="view_profile_seller_email">
                        {email}
                    </div>
                    <div id="view_profile_rating">
                        Rating: {rating || "Not Available"}
                    </div>
                    {!isViewingOwnProfile && (
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
                <div id="view_profile_mid_right">
                    <div style={{'border-top': 'none'}}>
                        Honesty: {userData?.honesty}
                    </div>
                    <div>
                        Number of Reviews: {userData?.numreviews}
                    </div>
                    <div>
                        Politeness: {userData?.politeness}
                    </div>
                    <div style={{'border-bottom': 'none'}}>
                        Quickness: {userData?.quickness}
                    </div>
                </div>
            </div>
            <div id="view_profile_bot">
                {listings.map(listing => (
                    <ListingItem key={listing.listingid} id={listing.listingid} title={listing.listing_name} price={listing.asking_price} />
                ))}
            </div>
        </div>
    )
}

export default ViewProfile;