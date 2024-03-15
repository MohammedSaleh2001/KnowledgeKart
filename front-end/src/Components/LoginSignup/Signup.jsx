import React from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function Signup() {
    const navigate = useNavigate()

    return (
        <div className="container">
            <div className="header">
                <div className="text">Sign Up</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="text" placeholder="Full Name" />
                </div>
                <div className="input">
                    <input type="email" placeholder="Email Address" />
                </div>
                <div className="input">
                    <input type="password" placeholder="Password" />
                </div>
                <div className="input">
                    <input type="password" placeholder="Re-enter Password" />
                </div>
            </div>
            <div className="submit-container">
                <div className="submit" onClick={() => {
                    navigate("/")
                }}
                >Sign Up</div>
            </div>
        </div>
    )
}

export default Signup;