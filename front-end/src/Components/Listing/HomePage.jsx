import React from 'react'
import './Listing.css'

import Searchbar from './Searchbar'
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ChatIcon from '@mui/icons-material/Chat';
import PostAddIcon from '@mui/icons-material/PostAdd';

import ListingItem from './ListingItem'

import { useNavigate } from "react-router-dom";  

function HomePage() {

    const navigate = useNavigate();

    // const sample_listings = [
    //     {
    //         id: 1,
    //         title: "Listing 1",
    //         price: 30.00,
    //     },
    //     {
    //         id: 2,
    //         title: "ENGG 130 Textbook",
    //         price: 100.00
    //     }
    // ]
    // const sample_recommended_listings = [
    //     {
    //         id: 3,
    //         title: "ENGG 130 Textbook",
    //         price: 100.00
    //     },
    //     {  
    //         id: 4,
    //         title: "PHYS 130 Textbook",
    //         price: 90.00
    //     },
    //     {
    //         id: 5,
    //         title: "MATH 100 Textbook",
    //         price: 50.00
    //     },
    //     {
    //         id: 6,
    //         title: "ENGL 199 Textbook",
    //         price: 40.00
    //     },
    //     {
    //         id: 7,
    //         title: "MATH 102 Textbook",
    //         price: 50.00
    //     }
    // ]
    const listingComponents = []
    // for (const listing of sample_listings) {
    //     listingComponents.push(<ListingItem
    //         title={listing.title}
    //         price={listing.price}
    //     />)
    // }
    const recommendedListingComponents = []
    // for (const listing of sample_recommended_listings) {
    //     recommendedListingComponents.push(<ListingItem
    //         title={listing.title}
    //         price={listing.price}
    //     />)
    // }
    
    return (
        <div id="homepage-container">
            <div id="menu-container">
                <div id="search-bar-container">
                    <Searchbar />
                </div>
                <div>
                    <ChatIcon style={{fontSize: 50}} id="chat-icon" />
                    <PostAddIcon style={{fontSize: 50}} id="add-post-icon" onClick={() => {
                        navigate("/create")
                    }} />
                    <AccountCircleIcon style={{fontSize: 50}} id="profile-icon" />
                </div>
            </div>
            <div id="listview_container">
                <div id="list_items_div">
                    {listingComponents}    
                </div>
                <div id="recommended_list">
                    <div id="recommended_list_title">
                        Recommended
                    </div>
                    {recommendedListingComponents}
                </div>
            </div>
        </div>
    )
}

export default HomePage;