import React, { useEffect, useState } from 'react'
import './Listing.css'

import Searchbar from './Searchbar'
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ChatIcon from '@mui/icons-material/Chat';
import PostAddIcon from '@mui/icons-material/PostAdd';

import ListingItem from './ListingItem'

import { useNavigate } from "react-router-dom";  

function HomePage() {

    const navigate = useNavigate();
    const [listings, setListings] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState("%");

    useEffect(() => {
        fetchListings(searchTerm);
    }, [searchTerm]);

    const fetchListings = async (searchTerm) => {
        const token = localStorage.getItem('token');
        try {
            setIsLoading(true);
            const response = await fetch('api/search_listings', {
                method: 'POST',
                cache: 'no-cache',
                credentials: 'same-origin',
                mode: 'cors',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    search_term: `${searchTerm}`,
                    max_number_results: 10,
                })
            });
            console.log(response);
            if (!response.ok) {
                throw new Error('Something went wrong!');
            }
            const data = await response.json();
            setListings(data.data);
        } catch (error) {
            setError(error.message);
        } finally {
            setIsLoading(false);
        }
    }

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }
    
    return (
        <div id="homepage-container">
            <div id="menu-container">
                <div id="search-bar-container">
                    <Searchbar onSearch={(newSearchTerm) => {
                        setSearchTerm(newSearchTerm);
                    }} />
                </div>
                <div>
                    <ChatIcon style={{fontSize: 50}} id="chat-icon" />
                    <PostAddIcon style={{fontSize: 50}} id="add-post-icon" onClick={() => {
                        navigate("/create")
                    }} />
                    <AccountCircleIcon style={{fontSize: 50, cursor: 'pointer'}} id="profile-icon" onClick={() => {
                        navigate(`/viewprofile/${localStorage.getItem('email')}`)
                    }} />
                </div>
            </div>
            <div id="listview_container">
                <div id="list_items_div">
                    {/* {listingComponents} */}
                    {listings.map(listing => (
                        <ListingItem key={listing.listingid} id={listing.listingid} title={listing.listing_name} price={listing.asking_price} />
                    ))}
                </div>
                <div id="recommended_list">
                    <div id="recommended_list_title">
                        Recommended
                    </div>
                    {/* {recommendedListingComponents} */}
                </div>
            </div>
        </div>
    )
}

export default HomePage;