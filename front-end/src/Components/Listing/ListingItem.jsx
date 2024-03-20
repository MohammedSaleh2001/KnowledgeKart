import React from 'react'
import './Listing.css'

function ListingItem({title, description, price, category}) {
    return (
        <div id="listing-container">
            {title}
            {description}
            {price}
            {category}
        </div>
    )
}

export default ListingItem;