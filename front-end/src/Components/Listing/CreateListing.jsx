import React, { useState } from 'react'
import './Listing.css'

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";

function CreateListing() {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState(0);
    const [category, setCategory] = useState('');
    const [image, setImage] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('price', price);
        formData.append('category', category);
        formData.append('category', category);
        if (image) {
            formData.append('image', image);
        }

        try {
            const response = await fetch('insert_api_here', {
                method: 'POST',
                body: formData,
            });
            if (response.ok) {
                console.log("Listing created successfully");
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
                    <Form>
                        <Form.Label id="create-listing-title">Create Listing</Form.Label>
                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setTitle(e.target.value)
                            }} type="text" placeholder="Enter Title" />
                        </Form.Group>

                        <Form.Group id="textarea-form-group">
                            <Form.Control onChange={(e) => {
                                setDescription(e.target.value)
                            }} as="textarea" placeholder="Enter Description" />
                        </Form.Group>

                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setPrice(e.target.value)
                            }} type="number" placeholder="Enter Price" />
                        </Form.Group>

                        <Form.Group>
                            <Form.Control onChange={(e) => {
                                setCategory(e.target.value)
                            }} type="text" placeholder="Enter Category" />
                        </Form.Group>

                        <Form.Group controlId="formFile">
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