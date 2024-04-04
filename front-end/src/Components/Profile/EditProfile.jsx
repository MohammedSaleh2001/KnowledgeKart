import React from 'react'

import { useNavigate, useParams } from 'react-router-dom'

import './Profile.css'

function EditProfile() {

    const { email } = useParams();

    const navigate = useNavigate();

    return (
        <div id="edit_profile_container">
            <div id="edit_profile_title">Edit Profile</div>
            <div id="edit_first_name_div">
                <div>Edit Name:</div>
                <input type="text" placeholder="Enter Name" />
            </div>
            <div id="edit_picture_div">
                <div>Edit Picture:</div>
                <div>
                    <input type="file" />    
                </div>
            </div>
            <div id="edit_profile_submit_div">
                <button id="edit_profile_cancel_button" onClick={() => {
                    navigate(`/viewprofile/${email}`);
                }}>Cancel</button>
                <button id="edit_profile_submit_button">Submit</button>
            </div>
        </div>
    )
}

export default EditProfile;