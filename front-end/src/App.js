import useToken from './Components/AuthToken/useToken'
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './Context/AuthProvider';

import {AnalyticsView} from './Components/Analytics/index'
import {ChatHomePage} from './Components/Chat/index'
import {CreateListing, HomePage, Listing, EditListing} from './Components/Listing/index'
import {ForgotPassword, Login, LoginSignup, Signup} from './Components/LoginSignup/index'
import {ModerateInvestigate, ModerateReport, ModerateSuspend, ModerateView} from './Components/Moderate/index'
import {EditProfile, ViewProfile} from './Components/Profile/index'
import { ChatProvider } from './Context/ChatContext'

import RequireAuth from "./Components/RequireAuth";

const ROLES = {
  'User': 'U',
  'Moderator': 'M'
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
              <Route path="/forgotpassword" element={<ForgotPassword token={token} setToken={setToken} />} />
              <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
                <Route path="/home" element={<HomePage  token={token} setToken={setToken} />} />
                <Route path="/create" element={<CreateListing token={token} setToken={setToken} />} />
                <Route path="/editlisting/:listingId" element={<EditListing token={token} setToken={setToken} />} />
                <Route path="/editprofile/:email" element={<EditProfile token={token} setToken={setToken} />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.User, ROLES.Moderator]} />}>
                <Route path="/moderatereport/:email" element={<ModerateReport token={token} setToken={setToken} />} />
                <Route path="/viewprofile/:email" element={<ViewProfile token={token} setToken={setToken} />} />
                <Route path="/chat/:email" element={<ChatHomePage token={token} setToken={setToken} />} />
                <Route path="/listing/:listingId" element={<Listing />} />
              </Route>
              <Route element={<RequireAuth allowedRoles={[ROLES.Moderator]} />}>
                <Route path="/moderatesuspend/:email" element={<ModerateSuspend token={token} setToken={setToken} />} />
                <Route path="/moderateview" element={<ModerateView token={token} setToken={setToken} />} />
                <Route path="/moderateinvestigate/:reportId" element={<ModerateInvestigate token={token} setToken={setToken} />} />
              </Route>
              <Route path="/viewanalytics" element={<AnalyticsView token={token} setToken={setToken} />} />
            </Routes>
          </Router>
        </div>  
      </ChatProvider>
    </AuthProvider>
  );
}

export default App;
