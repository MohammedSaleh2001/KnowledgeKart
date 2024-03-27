import logo from './logo.svg';
import useToken from './Components/AuthToken/useToken'
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './Context/AuthProvider';

import {ForgotPassword, Login, LoginSignup, Signup} from './Components/LoginSignup/index'
import {CreateListing, HomePage, Listing} from './Components/Listing/index'

import RequireAuth from "./Components/RequireAuth";

// function requireAuth(nextState, replace, next) {
//   if (!authenticated) {
//     replace({
//       pathname: "/login",
//       state: {nextPathname: nextState.location.pathname}
//     });
//   }
//   next();
// }

const ROLES = {
  'User': 'U',
}

function App() {
  const { token, removeToken, setToken } = useToken();
  return (
    <AuthProvider>
      <div class="centered">
        <Router>
          <Routes>
            <Route path="/" element={<LoginSignup token={token} setToken={setToken} />} />
            <Route path="/signup" element={<Signup token={token} setToken={setToken} />} />
            <Route path="/login" element={<Login token={token} setToken={setToken} />} />
            <Route path="/forgotpassword" element={<ForgotPassword token={token} setToken={setToken} />} />
            <Route element={<RequireAuth allowedRoles={ROLES.User} />}>
              <Route path="/home" element={<HomePage  token={token} setToken={setToken} />} />
              {/* <Route path="/listing">
                <Route path="create" element={<CreateListing token={token} setToken={setToken} />} />
                <Route path=":listingId" element={<Listing />} />
              </Route>   */}
              <Route path="/create" element={<CreateListing token={token} setToken={setToken} />} />
              <Route path="/listing:listingId" element={<Listing />} />
            </Route>
            {/* <Route path="/test" element={<Listing_Item 
              title="Insert Title Here"
              description="Insert Description Here"
              price={30.00}
              category="test_category"
              />} /> */}
          </Routes>
        </Router>
      </div>
    </AuthProvider>
  );
}

export default App;
