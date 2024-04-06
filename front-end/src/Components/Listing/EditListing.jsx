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
    const [category_type, setCategoryType] = useState('');
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
                    setName(data.data.listing_name);
                    setDescription(data.data.listing_description);
                    setAskingPrice(data.data.asking_price);
                    setCategoryType(data.data.category_type);
                    setCondition(data.data.condition);
                    setStatus(data.data.listingstatus);
                    setSoldTo(data.data.soldto);
                    setSoldPrice(data.data.soldprice);
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

            if (response.ok && data.data && data.data.userid) {
                console.log("Fetched Buyer id successfully!");
                soldToId = response?.data.userid;
            } else {
                alert("The email address does not exist.");
                return;
            }
        } catch (error) {
            console.error("Network error:", error);
        }

        var json = JSON.stringify({
            "listingid": parseInt(listingId),
            "listing_name" : name,
            "listing_description" : description,
            "asking_price" : asking_price,
            "category_type" : 1,
            "condition" : condition,
            "status": status,
            "sold_to": soldTo,
            "sold_price": soldPrice,
        });
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

                        <Form.Group controlId="formFile">
                            <Form.Label>Upload Image</Form.Label>
                            <Form.Control onChange={(e) => {
                                setImage(e.target.files[0])
                            }} type="file" />
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
                                type="text"
                                placeholder="Sold To"
                                value={status !== 'Sold' ? '' : soldTo}
                                onChange={(e) => setSoldTo(e.target.value)}
                                readOnly={status !== 'Sold' ? "readonly" : false} // Only editable when status is 'Closed'
                            />
                        </Form.Group>

                        <Form.Group>
                            <Form.Label>Sold Price</Form.Label>
                            <Form.Control
                                type="number"
                                placeholder="Sold Price"
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