import React from 'react'
import { useNavigate } from 'react-router-dom'
import './Listing.css'

function UserItem({id, name, email}) {
    const navigate = useNavigate();
    return (
        <div id="listing-container" style={{cursor: 'pointer'}} onClick={() => {
            navigate(`/viewprofile/${email}/`)
        }}>
            <div className="list-item-title">
                {name}
            </div>
            <div className="list-item-price">
                {email}
            </div>
        </div>
    )
}

export default UserItem;