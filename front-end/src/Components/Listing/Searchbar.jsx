import React, { useState } from 'react'

import SearchIcon from '@mui/icons-material/Search';

import './Listing.css'

function Searchbar({ onSearch }) {
    const [searchTerm, setSearchTerm] = useState('');
    
    return (
        <div className='input-wrapper'>
            <input
                id='search-bar'
                placeholder="Type to search..."
                value={searchTerm}
                onChange={(e) => {
                    setSearchTerm(e.target.value)
                }}
                onKeydown={(e) => {
                    if (e.key == 'Enter') {
                        onSearch(searchTerm);
                    }
                }}
            />
            <SearchIcon style={{cursor: 'pointer'}} onClick={() => {
                onSearch(searchTerm)
            }} />
        </div>
    )
}

export default Searchbar