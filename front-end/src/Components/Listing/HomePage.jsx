import React, { useEffect, useState } from 'react'
import './Listing.css'

import Searchbar from './Searchbar'
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ChatIcon from '@mui/icons-material/Chat';
import PostAddIcon from '@mui/icons-material/PostAdd';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ShieldIcon from '@mui/icons-material/Shield';

import ListingItem from './ListingItem'
import UserItem from './UserItem'

import { useNavigate } from "react-router-dom";  

function HomePage() {

    const navigate = useNavigate();
    const [listings, setListings] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState("%");
    const [choice, setChoice] = useState('Listing');

    useEffect(() => {
        const endpoint = choice === 'Listing' ? '/api/search_listings' : '/api/search_users';
        fetchListings(endpoint, searchTerm);
    }, [searchTerm, choice]);

    const fetchListings = async (endpoint, searchTerm) => {
        const token = localStorage.getItem('token');
        try {
            setIsLoading(true);
            const response = await fetch(endpoint, {
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
            if (!response.ok) {
                throw new Error('Something went wrong!');
            }
            const data = await response.json();
            console.log(data.data);
            setListings(data.data);
        } catch (error) {
            setError(error.message);
            navigate('/');
        } finally {
            setIsLoading(false);
        }
    }

    const handleLogout = async () => {
        const token = localStorage.getItem('token');
        try {
            localStorage.removeItem('token');
            navigate('/');
        } catch (error) {
            console.log('Logout error: ', error);
        }
    }

    const ToggleChoice = () => {
        if (choice === 'Listing') {
            setChoice('User');
        } else {
            setChoice('Listing');
        }
    }

    const handleAnalyticsRedirect = () => {
        const baseURL = "https://localhost/";
        window.location.href = `${baseURL}grafana/login`
    }

    const isOwnerOrAdmin = ['O', 'A'].includes(localStorage.getItem('roles'));
    const isNotVerified = localStorage.getItem('roles') === 'V';

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }
    
    return (
        <div id="homepage-container">
            <div id="menu-container">
                <div id="toggle_button_div" onClick={ToggleChoice}>
                    {choice}
                </div>
                <div id="search-bar-container">
                    <Searchbar onSearch={(newSearchTerm) => {
                        setSearchTerm(newSearchTerm);
                    }} />
                </div>
                <div>
                    {isOwnerOrAdmin && (<AnalyticsIcon style={{fontSize: 50, cursor: 'pointer'}} id="analytics-icon" onClick={() => {
                        handleAnalyticsRedirect();
                    }} />)}
                    {isOwnerOrAdmin && (<ShieldIcon style={{fontSize: 50, cursor: 'pointer'}} id="shield-icon" onClick={() => {
                        navigate('/moderateview');
                    }} />)}
                    {!isNotVerified && (<ChatIcon style={{fontSize: 50, cursor: 'pointer'}} id="chat-icon" onClick={() => {
                        navigate(`/chat/${localStorage.getItem('email')}`)
                    }} />)}
                    {!isNotVerified && (<PostAddIcon style={{fontSize: 50, cursor: 'pointer'}} id="add-post-icon" onClick={() => {
                        navigate("/create")
                    }} />)}
                    {!isNotVerified && <AccountCircleIcon style={{fontSize: 50, cursor: 'pointer'}} id="profile-icon" onClick={() => {
                        navigate(`/viewprofile/${localStorage.getItem('email')}`)
                    }} />}
                    <div onClick={handleLogout}>
                        Logout
                    </div>
                </div>
            </div>
            <div id="listview_container">
                <div id="list_items_div">
                    {choice === 'Listing' ? (
                        listings.filter(listing => listing.listingstatus === "O").map(listing => (
                            <ListingItem key={listing.listingid} id={listing.listingid} title={listing.listing_name} price={listing.asking_price} />
                        ))
                    ) : (
                        listings.map(user => (
                            <UserItem key={user.id} id={user.id} name={user.name} email={user.email} />
                        ))
                    )}
                </div>
            </div>
        </div>
    )
}

export default HomePage;