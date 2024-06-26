import React, { useEffect, useState } from 'react'
import './LoginSignup.css'
import { useNavigate, useParams } from "react-router-dom";

function ForgotPasswordForm(props) {
    const navigate = useNavigate();
    const { resetToken } = useParams();
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const response = await fetch('/api/reset_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    reset_token: resetToken,
                    new_password: newPassword,
                }),
            });
            const data = await response.json();
            console.log("Data:", data);
            if (response.ok) {
                alert("Password reset successfully");
                navigate("/");
            } else {
                console.error("Failed to reset password.");
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
                        type="password"
                        placeholder="New Password"
                        value={newPassword}
                        onChange={e => setNewPassword(e.target.value)}
                    />
                </div>
                <div className="input">
                    <input
                        type="password"
                        placeholder="Re-type New Password"
                        value={confirmPassword}
                        onChange={e => setConfirmPassword(e.target.value)}
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

export default ForgotPasswordForm