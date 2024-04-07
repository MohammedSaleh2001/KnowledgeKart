import React, { useState, useContext } from 'react';
import AuthContext from '../../Context/AuthProvider';
import './LoginSignup.css';

import { Link, useNavigate, useLocation } from "react-router-dom";

function Login(props) {
    const { auth, setAuth } = useContext(AuthContext);

    const navigate = useNavigate();
    // const location = useLocation();
    // const from = location.state?.from?.pathname || "/";
    
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

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

                const accessToken = responseData?.accessToken;
                const roles = responseData?.role;

                localStorage.setItem('token', accessToken);
                localStorage.setItem('email', email);
                localStorage.setItem('roles', roles);
                localStorage.setItem('password', password);

                setAuth({ email, password, roles, accessToken });

                props.setToken(responseData.access_token);

                console.log(responseData);
                console.log(props);  // error
                console.log(props.token);

                if (responseData.status == 'success') {
                    if (roles == 'U') {
                        navigate('/home', { replace: true })    
                    } else if (roles == 'M') {
                        navigate('/moderateview', { replace: true })
                    }
                } else {
                    alert('Could not log you in!');
                    return;
                }
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