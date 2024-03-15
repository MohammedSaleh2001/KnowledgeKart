import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import LoginSignup from './Components/LoginSignup/LoginSignup'
import Login from './Components/LoginSignup/Login'
import Signup from './Components/LoginSignup/Signup'
import ForgotPassword from './Components/LoginSignup/ForgotPassword'

function App() {
  return (
    <div class="centered">
      <Router>
        <Routes>
          <Route path="/" element={<LoginSignup />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/forgotpassword" element={<ForgotPassword />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
