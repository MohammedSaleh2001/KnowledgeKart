import React, { createContext, useState } from "react";

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState(() => {
        const savedToken = localStorage.getItem('token');
        const savedRoles = JSON.parse(localStorage.getItem('roles'));
        const savedEmail = localStorage.getItem('email');
        const savedPassword = localStorage.getItem('password');
        return savedToken ? { accessToken: savedToken, roles: savedRoles, email: savedEmail, password: savedPassword } : null;
    });

    return (
        <AuthContext.Provider value={{ auth, setAuth }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;