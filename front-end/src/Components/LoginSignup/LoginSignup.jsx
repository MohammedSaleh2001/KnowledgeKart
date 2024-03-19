import React, { useState, useEffect } from 'react';
import './LoginSignup.css'

import { useNavigate } from "react-router-dom";

// async function getUser() {
//     try {
//       // ⛔️ TypeError: Failed to fetch
//       // 👇️ incorrect or incomplete URL
//       const response = await fetch('flaskapp:5439/login');
  
//       if (!response.ok) {
//         throw new Error(`Error! status: ${response.status}`);
//       }
  
//       const result = await response.json();
//       return result;
//     //   console.
//     } catch (err) {
//       console.log(err);
//     }
// }
  

function LoginSignup() {
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

    return (
        <div className='container'>
            <div className="header">
                <div className="text">Welcome</div>
                <div className="underline" />
            </div>
            {/* <div className="text"> {currentTime} </div> */}
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