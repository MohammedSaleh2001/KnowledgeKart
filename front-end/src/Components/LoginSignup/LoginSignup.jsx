import React, { useState, useEffect } from 'react';
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";  

function LoginSignup(props) {
    const navigate = useNavigate()

    // const [currentTime, setCurrentTime] = useState(0);
    
    // useEffect(() => {
    //   fetch('/api/time', {
    //     method: 'GET',
    //     mode: 'no-cors',
    //     cache: 'no-cache',
    //     credentials: 'same-origin',
    //     headers: {
    //         'Content-type': 'application/json',
    //     },
    // }).then(res => res.json()).then(data => {
    //     setCurrentTime(data.time);
    // });
    // }, []);

    // getUser();

    // console.log(props);

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