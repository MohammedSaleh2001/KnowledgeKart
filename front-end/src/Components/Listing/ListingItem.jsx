import React from 'react'
import './Listing.css'

function ListingItem({title, price}) {
    return (
        <div id="listing-container">
            <div className="list-item-title">
                {title}
            </div>
            <div className="list-item-price">
                ${price}
            </div>
        </div>
    )
}

export default ListingItem;