import React from 'react'
import './Listing.css'

import Searchbar from './Searchbar'
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ChatIcon from '@mui/icons-material/Chat';
import PostAddIcon from '@mui/icons-material/PostAdd';

import ListingItem from './ListingItem'

function HomePage() {

    const sample_listings = [
        {
            id: 1,
            title: "Listing 1",
            description: "Description 1",
            price: 30.00,
            category: "some_category"
        }
    ]
    const listingComponents = []
    for (const listing of sample_listings) {
        listingComponents.push(<ListingItem
            title={listing.title}
            description={listing.description}
            price={listing.price}
            category={listing.category}
        />)
    }
    
    return (
        <div id="homepage-container">
            <div id="menu-container">
                <div id="search-bar-container">
                    <Searchbar />
                </div>
                <div>
                    <ChatIcon style={{fontSize: 50}} id="chat-icon" />
                    <PostAddIcon style={{fontSize: 50}} id="add-post-icon" />
                    <AccountCircleIcon style={{fontSize: 50}} id="profile-icon" />
                </div>
            </div>
            <div>
                {listingComponents}
            </div>
            {/* <ListingItem
                title={"Listing 1"}
                description={"Description 1"}
                price={30.00}
                category={"some_category"}
            /> */}
        </div>
    )
}

export default HomePage;