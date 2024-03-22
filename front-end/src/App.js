import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import {ForgotPassword, Login, LoginSignup, Signup} from './Components/LoginSignup/index'
import {CreateListing, HomePage, Listing} from './Components/Listing/index'

function App() {
  return (
    <div class="centered">
      <Router>
        <Routes>
          <Route path="/" element={<LoginSignup />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/forgotpassword" element={<ForgotPassword />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/createlisting" element={<CreateListing />} />
          <Route path="/listing/:listingId" element={<Listing />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
