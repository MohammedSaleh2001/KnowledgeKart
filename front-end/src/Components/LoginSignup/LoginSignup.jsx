/*
Author: John Yu
Functional Requirements Fulfilled:
    None
*/

import React, { useState, useEffect } from 'react';
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";  

function LoginSignup(props) {
    const navigate = useNavigate();

    return (
        <div className='container'>
            <div className="header">
                <div className="text">Welcome</div>
                <div className="underline" />
            </div>
            <div className="submit-container">
                <div className="submit" onClick={() => {
                    navigate("/signup")
                }}
                >Sign Up</div>
                <div className="submit" onClick={() => {
                    navigate("/login")
                }}
                >Login</div>
            </div>
        </div>
    )
}

export default LoginSignup