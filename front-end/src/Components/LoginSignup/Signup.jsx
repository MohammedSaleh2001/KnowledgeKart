import React from 'react'
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

function Signup() {
    const navigate = useNavigate()

    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async () => {
        if (password != confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const data = {
            fullName,
            email,
            password,
            confirmPassword
        };

        try {
            const url = 'http://flaskapp:5439/signup';
            const response = await fetch(url, {
                method: 'POST',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log(responseData);
                navigate('/')
            } else {
                throw new Error('HTTP error: ${response.status}');
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
                <div className="submit" onClick={handleSubmit}>Sign Up</div>
            </div>
        </div>
    )
}

export default Signup;