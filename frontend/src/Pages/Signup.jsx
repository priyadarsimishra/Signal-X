import React from 'react'
import loginlogo from "../Assets/logo_login.png"
import "../index.css";

const Signup = () => {
    return (
        <div className="login-page">
        <div className='circle'>
            <img className="ll" src={loginlogo} alt=""/>
        </div>
        <div className="sign-heading">
            <h1 class="signup">Create your account for Signal</h1>
            <h1 class="x1">X</h1>
        </div>

        <h1 className='goog'>Continue with Google</h1>
        <h1 className='email'>Continue with Email</h1>

        <p class="p-body" >By signing up, you agree to the Terms of Service and Data Processing Agreement.</p>
    </div>
    )
}

export default Signup