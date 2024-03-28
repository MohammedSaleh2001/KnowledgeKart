import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Listing.css'

function ListingItem({id, title, price}) {

    const navigate = useNavigate();

    return (
        <div id="listing-container" style={{cursor: 'pointer'}} onClick={() => {
            navigate(`/listing/${id}`)
        }}>
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