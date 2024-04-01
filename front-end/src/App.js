import logo from './logo.svg';
import useToken from './Components/AuthToken/useToken'
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './Context/AuthProvider';

import {AnalyticsView} from './Components/Analytics/index'
import {ChatHomePage} from './Components/Chat/index'
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
              <Route path="/create" element={<CreateListing token={token} setToken={setToken} />} />
              <Route path="/listing/:listingId" element={<Listing />} />
              <Route path="/viewprofile/:email" element={<ViewProfile token={token} setToken={setToken} />} />
            </Route>
            <Route path="/viewanalytics" element={<AnalyticsView token={token} setToken={setToken} />} />
            <Route path="/moderateinvestigate/:email" element={<ModerateInvestigate token={token} setToken={setToken} />} />
            <Route path="/moderatereport/:email" element={<ModerateReport token={token} setToken={setToken} />} />
            <Route path="/moderatesuspend/:email" element={<ModerateSuspend token={token} setToken={setToken} />} />
            <Route path="/moderateview" element={<ModerateView token={token} setToken={setToken} />} />
            <Route path="/editprofile/:email" element={<EditProfile token={token} setToken={setToken} />} />
            <Route path="/chat/:email" element={<ChatHomePage token={token} setToken={setToken} />} />
          </Routes>
        </Router>
      </div>
    </AuthProvider>
  );
}

export default App;
