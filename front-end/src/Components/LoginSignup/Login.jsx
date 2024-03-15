import React from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate()
    
    return (
        <div className="container">
            <div className="header">
                <div className="text">Login</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="email" placeholder="Email Address" />
                </div>
                <div className="input">
                    <input type="password" placeholder="Password" />
                </div>
            </div>
            <div id="forgot-password" onClick={() => {
                navigate("/forgotpassword")
            }}
            >Forgot Password?</div>
            <div className="submit-container">
                <div className="submit" onClick={() => {
                    navigate("/")
                }}
                >Login</div>
            </div>
        </div>
    )
}

export default Login