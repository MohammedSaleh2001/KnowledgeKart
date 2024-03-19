import React, { useState } from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function Signup() {
    const navigate = useNavigate()

    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async () => {
        if (password != confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const data = {
            name,
            email,
            password
        };

        console.log(JSON.stringify(data));

        try {
            const url = '/api/signup';
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
                console.log(responseData);
                navigate('/')
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
                <div className="text">Sign Up</div>
                <div className="underline" />
            </div>
            <div className="inputs">
                <div className="input">
                    <input type="text" placeholder="Full Name" value={name} onInput={e => setName(e.target.value)} />
                </div>
                <div className="input">
                    <input type="email" placeholder="Email Address" value={email} onInput={e => setEmail(e.target.value)} />
                </div>
                <div className="input">
                    <input type="password" placeholder="Password" value={password} onInput={e => setPassword(e.target.value)} />
                </div>
                <div className="input">
                    <input type="password" placeholder="Re-enter Password" value={confirmPassword} onInput={e => setConfirmPassword(e.target.value)} />
                </div>
            </div>
            <div className="submit-container">
                <div className="submit" onClick={handleSubmit}>Sign Up</div>
            </div>
        </div>
    )
}

export default Signup;