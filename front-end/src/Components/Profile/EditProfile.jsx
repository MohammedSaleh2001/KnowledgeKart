import React, { useEffect, useState } from 'react'

import { useNavigate, useParams } from 'react-router-dom'

import './Profile.css'

function EditProfile() {
    const { email } = useParams();
    const navigate = useNavigate();

    const [newName, setNewName] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('/api/edit_user_profile', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "new_name": newName }),
            });

            const data = await response.json();

            console.log("edit_user_profile response:", data);

            if (data.status === 'success') {
                navigate(`/viewprofile/${email}`)
            } else {
                console.error('Failed to update profile');
            }
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    };

    return (
        <div id="edit_profile_container">
            <div id="edit_profile_title">Edit Profile</div>
            <div id="edit_first_name_div">
                <div id="edit_first_name_div_title">Edit Name</div>
                <input
                    type="text"
                    placeholder="Enter Name"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                />
            </div>
            <div id="edit_profile_submit_div">
                <button type="button" id="edit_profile_cancel_button" onClick={() => {
                    navigate(`/viewprofile/${email}`);
                }}>Cancel</button>
                <button type="submit" id="edit_profile_submit_button" onClick={handleSubmit}>Submit</button>
            </div>
        </div>
    )
}

export default EditProfile;