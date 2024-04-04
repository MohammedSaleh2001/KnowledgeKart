import React, { useState } from 'react'
import './Listing.css'

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

function CreateListing() {

    const navigate = useNavigate()

    // const [title, setTitle] = useState('');
    // const [description, setDescription] = useState('');
    // const [price, setPrice] = useState(0);
    // const [category, setCategory] = useState('');
    const [image, setImage] = useState(null);

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [asking_price, setAskingPrice] = useState(0.00);
    const [category_type, setCategoryType] = useState('');
    const [condition, setCondition] = useState("New");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('token');

        var json = JSON.stringify({
            "listing_name" : name,
            "listing_description" : description,
            "asking_price" : asking_price,
            "category_type" : 1,
            "condition" : condition,
        });

        try {
            console.log(json);
            const response = await fetch('api/add_listing', {
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
                console.log("Listing created successfully");
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
                        <Form.Label id="create-listing-title">Create Listing</Form.Label>
                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setName(e.target.value)
                            }} type="text" placeholder="Enter Title" />
                        </Form.Group>

                        <Form.Group id="textarea-form-group">
                            <Form.Control onChange={(e) => {
                                setDescription(e.target.value)
                            }} as="textarea" placeholder="Enter Description" />
                        </Form.Group>

                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setAskingPrice(parseFloat(e.target.value))
                            }} type="number" placeholder="Enter Price" />
                        </Form.Group>

                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setCategoryType(parseInt(e.target.value))
                            }} type="number" placeholder="Enter Category" />
                        </Form.Group>

                        <Form.Group controlId="formFile">
                            <Form.Label>Upload Image</Form.Label>
                            <Form.Control onChange={(e) => {
                                setImage(e.target.files[0])
                            }} type="file" />
                        </Form.Group>

                        <Button onClick={handleSubmit} variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>        
                </Card.Body>
            </Card>
        </Container>
    )
}

export default CreateListing;