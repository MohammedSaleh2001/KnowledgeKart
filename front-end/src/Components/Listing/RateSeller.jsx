import React, { useEffect, useState } from 'react'
import './Listing.css'

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

function RateSeller() {
    const [honesty, setHonesty] = useState();
    const [numReviews, setNumReviews] = useState();
    const [politeness, setPoliteness] = useState();
    const [quickness, setQuickness] = useState();

    const { emailToken } = useParams();

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here you can submit the rating data to your backend or perform any other necessary actions
        console.log("Seller Rating:", { honesty, numReviews, politeness, quickness });
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
            {/* <div id="num_reviews_input" className="input_div">
                <input
                    type="number"
                    placeholder="Enter their number of reviews."
                />
            </div> */}
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
                <button>Submit</button>
                <button>Skip</button>
            </div>
        </div>
    );
}

export default RateSeller;