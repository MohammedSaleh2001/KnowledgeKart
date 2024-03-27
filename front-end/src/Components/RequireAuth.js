import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from '../Hooks/useAuth';

const requireAuth = ({ allowedRoles }) => {
    const { auth } = useAuth();
    const location = useLocation();

    return (
        auth?.roles?.find(role => allowedRoles?.includes(role))
            ? <Outlet />
            : <Navigate to="/" state={{ from: location }} replace />
    );
}

export default requireAuth;