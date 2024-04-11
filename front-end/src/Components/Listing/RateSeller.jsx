import React, { useEffect, useState } from 'react'
import './Listing.css'

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

function RateSeller() {
    const [honesty, setHonesty] = useState();
    const [politeness, setPoliteness] = useState();
    const [quickness, setQuickness] = useState();

    const { emailToken } = useParams();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('/api/submit_review', {
                method: 'POST',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({"review_token": emailToken,
                                    "honesty": parseInt(honesty),
                                    "politeness": parseInt(politeness),
                                    "quickness": parseInt(quickness)}),
            });

            const data = await response.json();
            if (response.ok && (data.status === 'success')) {
                console.log("Submitted review successfully!");
            } else {
                console.log("Error: Invalid token");
            }
        } catch (error) {
            console.error("Network error:", error);
        }
    };

    return (
        <div id="rate_seller_container">
            <div id="rate_seller_title">
                Rating Form
            </div>
            <div id="honesty_input" className="input_div">
                <input
                    type="number"
                    placeholder="Enter their Honesty."
                    value={honesty}
                    onChange={e => setHonesty(e.target.value)}
                />
            </div>
            <div id="politeness_input" className="input_div">
                <input
                    type="number"
                    placeholder="Enter their politeness."
                    value={politeness}
                    onChange={e => setPoliteness(e.target.value)}
                />
            </div>
            <div id="quickness_input" className="input_div">
                <input
                    type="number"
                    placeholder="Enter their responsiveness."
                    value={quickness}
                    onChange={e => setQuickness(e.target.value)}
                />
            </div>
            <div id="action_buttons_div">
                <button onClick={handleSubmit} variant="primary" type="submit">Submit</button>
                <button>Skip</button>
            </div>
        </div>
    );
}

export default RateSeller;