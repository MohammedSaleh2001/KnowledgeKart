import React, { useState } from 'react'
import './Listing.css'

import { Col, Button, Row, Container, Card, Form } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

function RateSeller() {
    const [honesty, setHonesty] = useState(0);
    const [numReviews, setNumReviews] = useState(0);
    const [politeness, setPoliteness] = useState(0);
    const [quickness, setQuickness] = useState(0);

    const { emailToken } = useParams();

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here you can submit the rating data to your backend or perform any other necessary actions
        console.log("Seller Rating:", { honesty, numReviews, politeness, quickness });
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>
                    Honesty:
                    <input
                        type="number"
                        value={honesty}
                        onChange={(e) => setHonesty(parseInt(e.target.value))}
                        min={0}
                        max={4}
                    />
                </label>
            </div>
            <div>
                <label>
                    Number of Reviews:
                    <input
                        type="number"
                        value={numReviews}
                        onChange={(e) => setNumReviews(parseInt(e.target.value))}
                        min={0}
                        max={4}
                    />
                </label>
            </div>
            <div>
                <label>
                    Politeness:
                    <input
                        type="number"
                        value={politeness}
                        onChange={(e) => setPoliteness(parseInt(e.target.value))}
                        min={0}
                        max={4}
                    />
                </label>
            </div>
            <div>
                <label>
                    Quickness:
                    <input
                        type="number"
                        value={quickness}
                        onChange={(e) => setQuickness(parseInt(e.target.value))}
                        min={0}
                        max={4}
                    />
                </label>
            </div>
            <button type="submit">Submit Rating</button>
        </form>
    );
}

export default RateSeller;



// function RateSeller() {

//     const navigate = useNavigate()

//     const { emailToken } = useParams();

//     // const [title, setTitle] = useState('');
//     // const [description, setDescription] = useState('');
//     // const [price, setPrice] = useState(0);
//     // const [category, setCategory] = useState('');
//     const [image, setImage] = useState(null);

//     const [name, setName] = useState('');
//     const [description, setDescription] = useState('');
//     const [asking_price, setAskingPrice] = useState(0.00);
//     const [category_type, setCategoryType] = useState('');
//     const [condition, setCondition] = useState("New");

//     const handleSubmit = async (e) => {
//         e.preventDefault();

//         const token = localStorage.getItem('token');

//         var json = JSON.stringify({
//             "listing_name" : name,
//             "listing_description" : description,
//             "asking_price" : asking_price,
//             "category_type" : 1,
//             "condition" : condition,
//         });

//         try {
//             console.log(json);
//             const response = await fetch('api/add_listing', {
//                 method: 'POST',
//                 cache: 'no-cache',
//                 credentials: 'same-origin',
//                 headers: {
//                     'Authorization': `Bearer ${token}`,
//                     'Accept': 'application/json',
//                     'Content-type': 'application/json',
//                 },
//                 body: json,
//             });
//             if (response.ok) {
//                 console.log("Listing created successfully");
//                 navigate('/home');
//             } else {
//                 console.log('Server error:', response.statusText)
//             }
//         } catch (error) {
//             console.error('Network error:', error);
//         }
//     };

//     return (
//         <Container>
//             <Card>
//                 <Card.Body>
//                     <Form id="create_listing_form">
//                         <Form.Label id="create-listing-title">Create Listing</Form.Label>
//                         <Form.Group>
//                             <Form.Label>Title</Form.Label>
//                             <Form.Control onChange={(e) => {
//                                 setName(e.target.value)
//                             }} type="text" placeholder="Enter Title" />
//                         </Form.Group>

//                         <Form.Group id="textarea-form-group">
//                             <Form.Label>Description</Form.Label>
//                             <Form.Control onChange={(e) => {
//                                 setDescription(e.target.value)
//                             }} as="textarea" placeholder="Enter Description" />
//                         </Form.Group>

//                         <Form.Group>
//                             <Form.Label>Price</Form.Label>
//                             <Form.Control onChange={(e) => {
//                                 setAskingPrice(parseFloat(e.target.value))
//                             }} type="number" placeholder="Enter Price" />
//                         </Form.Group>

//                         <Form.Group>
//                             <Form.Label>Category</Form.Label>
//                             <Form.Control
//                                 as="select"
//                                 value={category_type}
//                                 onChange={(e) => setCategoryType(e.target.value)}
//                             >
//                                 <option>Other</option>
//                                 <option>Textbook</option>
//                                 <option>Lab Equipment</option>
//                             </Form.Control>
//                         </Form.Group>

//                         <Form.Group>
//                             <Button onClick={handleSubmit} variant="primary" type="submit">
//                                 Submit
//                             </Button>
//                             <Button variant="primary" type="submit" onClick={() => {
//                                 navigate('/home');
//                             }}>
//                                 Cancel
//                             </Button>
//                         </Form.Group>
//                     </Form>        
//                 </Card.Body>
//             </Card>
//         </Container>
//     )
// }

// export default RateSeller;