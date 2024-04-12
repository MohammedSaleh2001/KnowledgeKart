import useToken from './Components/AuthToken/useToken'
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './Context/AuthProvider';

import {AnalyticsView} from './Components/Analytics/index'
import {ChatHomePage} from './Components/Chat/index'
import {CreateListing, HomePage, Listing, EditListing, RateSeller} from './Components/Listing/index'
import {ChangePassword, ForgotPasswordRequest, ForgotPasswordForm, Login, LoginSignup, Signup} from './Components/LoginSignup/index'
import {ModerateInvestigate, ModerateReport, Suspend, ModerateView} from './Components/Moderate/index'
import {EditProfile, ViewProfile} from './Components/Profile/index'
import { ChatProvider } from './Context/ChatContext'

import RequireAuth from "./Components/RequireAuth";

const ROLES = {
  'User': 'U',
  'Unverified': 'V',
  'Moderator': 'M',
  'Owner': 'O',
  'Admin': 'A',
}

function App() {
  const { token, removeToken, setToken } = useToken();
  return (
    <AuthProvider>
      <ChatProvider>
        <div class="centered">
          <Router>
            <Routes>
              <Route path="/" element={<LoginSignup token={token} setToken={setToken} />} />
              <Route path="/signup" element={<Signup token={token} setToken={setToken} />} />
              <Route path="/login" element={<Login token={token} setToken={setToken} />} />
              <Route path="/changepassword" element={<ChangePassword token={token} setToken={setToken} />} />
              <Route path="/forgotpassword" element={<ForgotPasswordRequest token={token} setToken={setToken} />} />
              <Route path="/forgotpasswordform/:resetToken" element={<ForgotPasswordForm token={token} setToken={setToken} />} />
              <Route path="/rateseller/:emailToken" element={<RateSeller token={token} setToken={setToken} />} />
              <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Unverified, ROLES.Admin, ROLES.Owner]} />}>
                <Route path="/home" element={<HomePage token={token} setToken={setToken} />} />
                <Route path="/editprofile/:email" element={<EditProfile token={token} setToken={setToken} />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Unverified, ROLES.Moderator, ROLES.Admin, ROLES.Owner]} />}>
                <Route path="/viewprofile/:email" element={<ViewProfile token={token} setToken={setToken} />} />
                <Route path="/listing/:listingId" element={<Listing />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Admin, ROLES.Owner]} />}>
                <Route path="/create" element={<CreateListing token={token} setToken={setToken} />} />
                <Route path="/editlisting/:listingId" element={<EditListing token={token} setToken={setToken} />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Moderator, ROLES.Admin, ROLES.Owner]} />}>
                <Route path="/moderatereport/:email" element={<ModerateReport token={token} setToken={setToken} />} />
                <Route path="/chat/:email" element={<ChatHomePage token={token} setToken={setToken} />} />
                <Route path="/listing/:listingId" element={<Listing />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.Moderator, ROLES.Admin, ROLES.Owner]} />}>
                <Route path="/moderateview" element={<ModerateView token={token} setToken={setToken} />} />
                <Route path="/moderateinvestigate/:reportId" element={<ModerateInvestigate token={token} setToken={setToken} />} />
                <Route path="/suspend/:reportId" element={<Suspend token={token} setToken={setToken} />} />
              </Route>
            </Routes>
          </Router>
        </div>  
      </ChatProvider>
    </AuthProvider>
  );
}

export default App;
