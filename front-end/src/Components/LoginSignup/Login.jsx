import React, { useState } from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function Login(props) {
    const navigate = useNavigate()
    
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async () => {
        if (email.trim() === '' || password.trim() === '') {
            alert('Enter email and password');
            return;
        }

        const data = {
            email,
            password
        };

        console.log(JSON.stringify(data));

        try {
            const url = '/api/login';
            const response = await fetch(url, {
                method: 'POST',
                // mode: 'no-cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const responseData = await response.json();

                props.setToken(responseData.access_token);

                console.log(responseData);
                console.log(props);
                console.log(props.token);

                navigate('/home')
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        } catch (error) {
            console.log('There was a problem with the fetch operation: ', error);
        }
    };

    return (
        <div className="container">
            <div className="header">
                <div className="text">Login</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="email" placeholder="Email Address" value={email} onInput={e => setEmail(e.target.value)} />
                </div>
                <div className="input">
                    <input type="password" placeholder="Password" value={password} onInput={e => setPassword(e.target.value)} />
                </div>
            </div>
            <div id="forgot-password" onClick={() => {
                navigate("/forgotpassword")
            }}
            >Forgot Password?</div>
            <div className="submit-container">
                <div className="submit" onClick={handleSubmit} >Login</div>
            </div>
        </div>
    )
}

export default Login