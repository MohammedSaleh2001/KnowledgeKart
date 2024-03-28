import logo from './logo.svg';
import useToken from './Components/AuthToken/useToken'
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './Context/AuthProvider';

import {AnalyticsView} from './Components/Analytics/index'
import {ChatMessage, ChatView} from './Components/Chat/index'
import {CreateListing, HomePage, Listing} from './Components/Listing/index'
import {ForgotPassword, Login, LoginSignup, Signup} from './Components/LoginSignup/index'
import {ModerateInvestigate, ModerateReport, ModerateSuspend, ModerateView} from './Components/Moderate/index'
import {EditProfile, ViewProfile} from './Components/Profile/index'

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
              <Route path="/listing/:listingId" element={<Listing />} />
            </Route>
            <Route path="/viewanalytics" element={<AnalyticsView token={token} setToken={setToken} />} />
            <Route path="/chatmessage/:chatID" element={<ChatMessage token={token} setToken={setToken} />} />
            <Route path="/chatview" element={<ChatView token={token} setToken={setToken} />} />
            <Route path="/moderateinvestigate/:userID" element={<ModerateInvestigate token={token} setToken={setToken} />} />
            <Route path="/moderatereport/:userID" element={<ModerateReport token={token} setToken={setToken} />} />
            <Route path="/moderatesuspend/:userID" element={<ModerateSuspend token={token} setToken={setToken} />} />
            <Route path="/moderateview" element={<ModerateView token={token} setToken={setToken} />} />
            <Route path="/editprofile/:userID" element={<EditProfile token={token} setToken={setToken} />} />
            <Route path="/viewprofile/:userID" element={<ViewProfile token={token} setToken={setToken} />} />
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
