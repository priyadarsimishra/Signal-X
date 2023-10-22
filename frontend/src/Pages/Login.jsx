import React from 'react'
import loginlogo from "../Assets/logo_login.png"
import "../index.css";

const Login = () => {
    return (
            <div className="login-page">
                <div className='circle'>
                    <img className="ll" src={loginlogo} alt=""/>
                </div>
                <div className="login-heading">
                    <h1 class="signal1">Log in to Signal </h1>
                    <h1 class="x1">X</h1>
                </div>

                <h1 className='goog'>Continue with Google</h1>
                <h1 className='email'>Continue with Email</h1>
            </div>
    )
}

export default Login