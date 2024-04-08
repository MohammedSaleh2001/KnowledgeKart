import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import './Listing.css'

import PortraitIcon from '@mui/icons-material/Portrait';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PhotoIcon from '@mui/icons-material/Photo';

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
                switch (data.data.listingStatus) {
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
                const numreviews = listing.seller.numreviews;

                const calculatedRating = (honesty + politeness + quickness + numreviews) / 4;
                setRating(calculatedRating.toFixed(2));
            } catch (error) {
                console.error("Error calculating the user's rating!")
            }
        }
    }, [listing])

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    const initiateChatWithSeller = async () => {
        const receiverEmail = listing?.seller?.email;
        const message = "Hello, I'm interested in your listing.";
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
    }

    return (
        // <div id="listing_page_container">
        //     <div id="listing_top_div">
        //         <div class="back-button">
        //             <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
        //                 navigate("/home")
        //             }} />
        //         </div>
        //         <div id="listing_title">
        //             {listing?.listing_name || "Untitled Listing"}
        //         </div>
        //         <div id="listing_date">
        //             {"Date Listed: " + listing?.date_listed || ""}
        //         </div>
        //         {isOwner && <div id="edit_button" onClick={() => {
        //                 navigate(`/editlisting/${listingId}`);
        //             }}>
        //                 Edit
        //             </div>    
        //         }
                
        //     </div>
        //     <div id="listing_mid_div">
        //         <div id="listing_mid_left">
        //             <div id="listing_mid_left_top">
        //                 <div id="listing_mid_left_top_left">
        //                     <PortraitIcon style={{fontSize: 250}}/>
        //                 </div>
        //                 <div id="listing_mid_left_top_right">
        //                     <div id="listing_mid_left_top_right_top">
        //                         <div id="listing_seller_name">
        //                             Name: {listing?.seller?.firstname || "Seller Name"}
        //                         </div>
        //                         <div id="listing_rating">
        //                             Rating: {rating || "N/A"}
        //                         </div>
        //                     </div>
        //                     <div id="listing_mid_left_top_right_mid">
        //                         Email: {listing?.seller?.email || "Seller Email Not Available"}
        //                     </div>
        //                     <div id="listing_mid_left_top_right_bot">
        //                         <div className="listing-button">
        //                             Email
        //                         </div>
        //                         <div className="listing-button" onClick={initiateChatWithSeller}>
        //                             Chat
        //                         </div>
        //                     </div>
        //                 </div>
        //             </div>
        //             <div id="listing_mid_left_bot">
        //                 <div id="listing_condition_of_product">
        //                     Condition: {listing?.condition || "N/A"}
        //                 </div>
        //                 <div id="listing_price_of_product">
        //                     Price: {"$" + listing?.asking_price || "N/A"}
        //                 </div>
        //             </div>
        //         </div>
        //         <div id="listing_mid_right">
        //             <PhotoIcon style={{fontSize: 400}} />
        //         </div>
        //     </div>
        //     <div id="listing_bot_div">
        //         Description:<br></br>
        //         {listing?.listing_description || ""}
        //     </div>
        // </div>
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
                    <div id="listing_date_div">
                        Date Listed: {listing?.date_listed || ""}    
                    </div>
                    <div id="listing_action_button_div">
                        <div>Email</div>
                        <div>Chat</div>
                    </div>    
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
                        Honesty: {listing?.seller?.honesty}
                    </div>
                    <div>
                        Number of Reviews: {listing?.seller?.numreviews}
                    </div>
                    <div>
                        Politeness: {listing?.seller?.politeness}
                    </div>
                    <div>
                        Quickness: {listing?.seller?.quickness}
                    </div>
                    <div id="listing_email_div">
                        Email: {listing?.seller?.email || "Not Available"}
                    </div>    
                </div>
            </div>
        </div>
    )
}

export default Listing