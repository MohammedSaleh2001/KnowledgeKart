import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from '../Hooks/useAuth';

const requireAuth = ({ allowedRoles }) => {
    const { auth } = useAuth();
    const location = useLocation();

    if (!auth || !allowedRoles.includes(auth.roles)) {
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return <Outlet />;
}

export default requireAuth;