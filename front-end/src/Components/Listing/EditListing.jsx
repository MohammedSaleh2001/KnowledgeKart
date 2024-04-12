import React, { useEffect, useState } from 'react';

import { useParams } from 'react-router-dom';

import './Listing.css';

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

function EditListing() {

    const navigate = useNavigate();

    const { listingId } = useParams();

    const [image, setImage] = useState(null);

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [asking_price, setAskingPrice] = useState(0.00);
    const [category_type, setCategoryType] = useState('Other');
    const [condition, setCondition] = useState("New");
    const [status, setStatus] = useState('open');
    const [soldTo, setSoldTo] = useState('');
    const [soldPrice, setSoldPrice] = useState('');

    useEffect(() => {
        const fetchListingDetails = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(`/api/listing_profile`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 'listingid': listingId }),
                });
                const data = await response.json();
                if (response.ok) {
                    console.log("data.data:", data.data);
                    switch (data.data.category_type) {
                        case 1:
                            setCategoryType("Other");
                            break;
                        case 2:
                            setCategoryType("Textbook");
                            break;
                        case 3:
                            setCategoryType("Lab Equipment");
                            break;
                        default:
                            setCategoryType("Other");
                            break;
                    }
                    setName(data.data.listing_name);
                    setDescription(data.data.listing_description);
                    setAskingPrice(data.data.asking_price);
                    setCondition(data.data.condition);
                    setSoldTo(data.data.buyer.email);
                    setSoldPrice(data.data.soldprice);
                    var currentStatus;
                    switch (data.data.listingstatus) {
                        case "O":
                            currentStatus = 'Open'; break;
                        case "C":
                            currentStatus = 'Closed'; break;
                        case "S":
                            currentStatus = 'Sold'; break;
                        default:
                            currentStatus = 'Open'; break;
                    }
                    setStatus(currentStatus);
                } else {
                    console.error('Failed to fetch listing details');
                }
            } catch (error) {
                console.error('Error fetching listing details:', error);
            }
        }

        fetchListingDetails();
    }, [listingId])

    const handleSubmit = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('token');
        var soldToId = NaN;

        try {
            const response = await fetch('/api/user_profile', {
                method: 'POST',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({"email": soldTo}),
            });

            const data = await response.json();
            if (response.ok && (data.status === 'success')) {
                console.log("Fetched Buyer id successfully!");
                soldToId = data.data.userid;
            } else {
                console.log("Sold to user does not exist.");
            }
        } catch (error) {
            console.error("Network error:", error);
        }

        var statusToSend = "O"
        switch (status) {
            case "Open":
                statusToSend = 'O';
                break;
            case "Closed":
                statusToSend = 'C';
                break;
            case "Sold":
                statusToSend = 'S';
                break;
            default:
                statusToSend = 'O';
                break;
        }

        var json = JSON.stringify({
            "listingid": parseInt(listingId),
            "listing_name" : name,
            "listing_description" : description,
            "asking_price" : asking_price,
            "category_type" : category_type,
            "condition" : condition,
            "status": statusToSend,
            "sold_to": soldToId,
            "sold_price": soldPrice,
        });
        console.log("json:", json);
        try {
            const response = await fetch('/api/edit_listing', {
                method: 'POST',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Accept': 'application/json',
                    'Content-type': 'application/json',
                },
                body: json,
            });
            if (response.ok) {
                console.log("Listing edited successfully");
                navigate('/home');
            } else {
                console.log('Server error:', response.statusText)
            }
        } catch (error) {
            console.error('Network error:', error);
        }
    };

    return (
        <Container>
            <Card>
                <Card.Body>
                    <Form id="create_listing_form">
                        <Form.Label id="create-listing-title">Edit Listing</Form.Label>
                        <Form.Group>
                            <Form.Label>Title</Form.Label>
                            <Form.Control onChange={(e) => {
                                setName(e.target.value)
                            }} type="text" placeholder="Enter Title" value={name} />
                        </Form.Group>

                        <Form.Group id="textarea-form-group">
                            <Form.Label>Description</Form.Label>
                            <Form.Control onChange={(e) => {
                                setDescription(e.target.value)
                            }} as="textarea" placeholder="Enter Description" value={description} />
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Condition</Form.Label>
                            <Form.Control
                                as="select"
                                value={condition}
                                onChange={(e) => setCondition(e.target.value)}
                            >
                                <option>New</option>
                                <option>Very Good</option>
                                <option>Good</option>
                                <option>Used</option>
                                <option>Very Used</option>
                            </Form.Control>
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Price</Form.Label>
                            <Form.Control onChange={(e) => {
                                setAskingPrice(parseFloat(e.target.value))
                            }} type="number" placeholder="Enter Price" value={asking_price} />
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Category</Form.Label>
                            <Form.Control
                                as="select"
                                value={category_type}
                                onChange={(e) => setCategoryType(e.target.value)}
                            >
                                <option>Other</option>
                                <option>Textbook</option>
                                <option>Lab Equipment</option>
                            </Form.Control>
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Status</Form.Label>
                            <Form.Control
                                as="select"
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                            >
                                <option>Open</option>
                                <option>Closed</option>
                                <option>Sold</option>
                            </Form.Control>
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Sold To</Form.Label>
                            <Form.Control
                                // className="input_readonly"
                                className={status !== 'Sold' ? "input_readonly" : ""}
                                type="text"
                                placeholder={status !== 'Sold' ? '' : "Enter Email Address"}
                                value={status !== 'Sold' ? '' : soldTo}
                                onChange={(e) => setSoldTo(e.target.value)}
                                readOnly={status !== 'Sold' ? "readonly" : false} // Only editable when status is 'Closed'
                            />
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Sold Price</Form.Label>
                            <Form.Control
                                className={status !== 'Sold' ? "input_readonly" : ""}
                                type="number"
                                placeholder={status !== 'Sold' ? '' : "Enter Price"}
                                value={status !== 'Sold' ? '' : soldPrice}
                                onChange={(e) => setSoldPrice(e.target.value)}
                                readOnly={status !== 'Sold' ? "readonly" : false} // Only editable when status is 'Closed'
                            />
                        </Form.Group>
                        
                        <Form.Group>
                            <Button onClick={handleSubmit} variant="primary" type="submit">
                                Submit
                            </Button>
                            <Button variant="primary" type="submit" onClick={() => {
                                navigate(`/listing/${listingId}`)
                            }}>
                                Cancel
                            </Button>
                        </Form.Group>
                    </Form>        
                </Card.Body>
            </Card>
        </Container>
    )
}

export default EditListing;