import React from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function ForgotPassword() {
    const navigate = useNavigate()

    return (
        <div className="container">
            <div className="header">
                <div className="text">Forgot Password</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="email" placeholder="Email Address" />
                </div>
            </div>
            <div className="submit-container">
                <div className="submit" onClick={() => {
                    navigate("/")
                }}
                >Submit</div>
            </div>
        </div>
    )
}

export default ForgotPassword