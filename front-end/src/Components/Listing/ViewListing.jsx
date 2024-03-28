import React from 'react'
import { Link, useParams } from 'react-router-dom'

import './Listing.css'

import PortraitIcon from '@mui/icons-material/Portrait';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import PhotoIcon from '@mui/icons-material/Photo';

import { useNavigate } from "react-router-dom";  

function Listing() {

    const navigate = useNavigate();

    const { listingId } = useParams();

    return (
        <div id="listing_page_container">
            <div id="listing_top_div">
                <div class="back-button">
                    <ArrowBackIosNewIcon onClick={() => {
                        navigate("/home")
                    }} />
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
                                    Elmo
                                </div>
                                <div id="listing_rating">
                                    Rating: 8/10
                                </div>
                            </div>
                            <div id="listing_mid_left_top_right_mid">
                                sesame@street.com
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
                            Condition: Good
                        </div>
                        <div id="listing_price_of_product">
                            Price: $20
                        </div>
                    </div>
                </div>
                <div id="listing_mid_right">
                    <PhotoIcon style={{fontSize: 400}} />
                </div>
            </div>
            <div id="listing_bot_div">
                Description<br></br>
                Insert description here
            </div>
        </div>
    )
}

export default Listing