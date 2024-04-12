import React, { useEffect, useState } from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function ForgotPasswordRequest(props) {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('/api/reset_password_request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                }),
            });
            const data = await response.json();
            console.log("Data:", data);
            if (response.ok && (data.status === 'success')) {
                alert("Sent reset password email!");
                navigate("/");
            } else {
                console.error("Failed!");
            }
        } catch (error) {
            console.error('Error resetting password:', error);
            alert('An error occurred while resetting the password.');
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
                        onChange={e => setEmail(e.target.value)}
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

export default ForgotPasswordRequest