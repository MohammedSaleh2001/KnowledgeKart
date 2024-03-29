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
                setListing(data.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchListing();
    }, [listingId]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    console.log(listing);

    return (
        <div id="listing_page_container">
            <div id="listing_top_div">
                <div class="back-button">
                    <ArrowBackIosNewIcon style={{cursor: 'pointer'}} onClick={() => {
                        navigate("/home")
                    }} />
                </div>
                <div id="listing_title">
                    {listing.listing_name || "Untitled Listing"}
                </div>
                <div id="listing_date">
                    {"Date Listed: " + listing.date_listed || ""}
                </div>
            </div>
            <div id="listing_mid_div">
                <div id="listing_mid_left">
                    <div id="listing_mid_left_top">
                        <div id="listing_mid_left_top_left">
                            <PortraitIcon style={{fontSize: 250}}/>
                        </div>
                        <div id="listing_mid_left_top_right">
                            <div id="listing_mid_left_top_right_top">
                                <div id="listing_seller_name">
                                    {listing.sellerName || "Seller Name"}
                                </div>
                                <div id="listing_rating">
                                    Rating: {listing.rating || "N/A"}
                                </div>
                            </div>
                            <div id="listing_mid_left_top_right_mid">
                                {listing.sellerEmail || "Seller Email Not Available"}
                            </div>
                            <div id="listing_mid_left_top_right_bot">
                                <div className="listing-button">
                                    Email
                                </div>
                                <div className="listing-button">
                                    Chat
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="listing_mid_left_bot">
                        <div id="listing_condition_of_product">
                            Condition: {listing.condition || "N/A"}
                        </div>
                        <div id="listing_price_of_product">
                            Price: {"$" + listing.asking_price || "N/A"}
                        </div>
                    </div>
                </div>
                <div id="listing_mid_right">
                    <PhotoIcon style={{fontSize: 400}} />
                </div>
            </div>
            <div id="listing_bot_div">
                Description:<br></br>
                {listing.listing_description || ""}
            </div>
        </div>
    )
}

export default Listing