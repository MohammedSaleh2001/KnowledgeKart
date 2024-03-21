import React from 'react'

import SearchIcon from '@mui/icons-material/Search';

import './Listing.css'

function Searchbar() {
    return (
        <div className='input-wrapper'>
            <input id='search-bar' placeholder="Type to search..." />
            <SearchIcon />
        </div>
    )
}

export default Searchbar