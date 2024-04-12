import React, { useEffect, useState } from 'react'
import './LoginSignup.css'

import { useNavigate, useParams } from "react-router-dom";

function ChangePassword(props) {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [oldPassword, setOldPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

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
                navigate("/");
            } else {
                alert("Password or email is incorrect");
                console.error("Failed to change password.");
            }
        } catch (error) {
            console.error('Error changing password:', error);
            alert('An error occurred while changing the password.');
        }
    };

    return (
        <div className="container">
            <div className="header">
                <div className="text">Forgot Password</div>
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