/*
Author: Ragur Krishnan

Functional Requirements Implemented:
    - FR4 (Backend implemented in /api/change_password' endpoint)
*/

import React, { useEffect, useState, useContext } from 'react'
import AuthContext from '../../Context/AuthProvider';
import './LoginSignup.css'

import { useNavigate, useParams } from "react-router-dom";

function ChangePassword(props) {
    const navigate = useNavigate();
    const { auth, setAuth } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [oldPassword, setOldPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // ----- Change password ----- //
        try {
            const response = await fetch('/api/change_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    old_password: oldPassword,
                    new_password: newPassword,
                }),
            });
            const data = await response.json();
            console.log("Data:", data);
            if (response.ok && (data.status === 'success')) {
                alert("Password changed successfully");
            } else {
                alert("Password or email is incorrect");
                console.error("Failed to change password.");
            }
        } catch (error) {
            console.error('Error changing password:', error);
            alert('An error occurred while changing the password.');
        }

        // ----- Log the user in ----- //
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                // mode: 'no-cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({
                    "email": email,
                    "password": newPassword
                })
            });

            if (response.ok) {
                const responseData = await response.json();
                const accessToken = responseData?.accessToken;
                const roles = responseData?.role;
                localStorage.setItem('token', accessToken);
                localStorage.setItem('email', email);
                setAuth({ email, newPassword, roles, accessToken });
                props.setToken(responseData.access_token);
                // ----- Check user verification ----- //
                const profileResponse = await fetch('/api/user_profile', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({"email": email})
                });
                const profileData = await profileResponse.json();
                if (profileData.status === 'success') {
                    if (profileData.data.verified) {
                        console.log("User is verified!");
                        localStorage.setItem('roles', roles);
                    } else {
                        console.log("User is not verified!")
                        localStorage.setItem('roles', 'V')
                    }
                } else {
                    console.log("Cannot retrieve profile data.");
                }
                // ----- End Check User Verification ----- //
                if (responseData.status == 'success') {
                    if (roles === 'U' || roles === 'O' || roles === 'A') {
                        navigate('/home', { replace: true })    
                    } else if (roles == 'M') {
                        navigate('/moderateview', { replace: true })
                    }
                } else {
                    alert('Could not log you in!');
                    return;
                }
            }
        } catch (error) {
            console.error("Error loggin in after changing password:", error);
        }
    };

    return (
        <div className="container">
            <div className="header">
                <div className="text">Change Password</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input 
                        type="email" 
                        placeholder="Email Address" 
                        value={email} 
                        onInput={e => setEmail(e.target.value)} 
                    />
                </div>
                <div className="input">
                    <input
                        type="password"
                        placeholder="Old Password"
                        value={oldPassword}
                        onChange={e => setOldPassword(e.target.value)}
                    />
                </div>
                <div className="input">
                    <input
                        type="password"
                        placeholder="New Password"
                        value={newPassword}
                        onChange={e => setNewPassword(e.target.value)}
                    />
                </div>
            </div>
            <div className="submit-container">
                <div className="submit" onClick={handleSubmit}
                >Submit</div>
            </div>
        </div>
    )
}

export default ChangePassword