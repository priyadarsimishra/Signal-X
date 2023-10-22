import React, { Children } from 'react'
import Body from './Body'
import gradient from "../Assets/gradient.png"
import logo from "../Assets/Logo.png"
import vector from "../Assets/vector.png"
import "../index.css";
import {Link} from "react-router-dom"

const Navbar = () => {

    const path = window.location.pathname

    return (
            <div className="nav">
                <div className='nav-pages'>
                    <ul className='ul1'>
                        <img className='logo' src={logo}/>
                        <li>
                            <Link to="/" className='site-title'> Signal</Link>
                        </li>
                        <li>
                            <Link to="/" className='site-x'> X</Link>
                        </li>
                        <li>
                            <CustomLink to="/" className='site-features'>Features</CustomLink>
                        </li>
                        <li>
                            <CustomLink to="/stock" className='site-stocks'>Stocks</CustomLink>
                        </li>
                    </ul>

                    <div className='nav-account'>
                        <ul className='ul2'>
                            <li>
                                <CustomLink to="/login" className='site-login'>Log in</CustomLink>
                            </li>
                            <li>
                                <CustomLink to="/signup" className='site-signup'>Sign up</CustomLink>
                            </li>
                        </ul>
                    </div>

                </div>
            </div>
    )
}

function CustomLink({ to, children, ...props}) {
    const path = window.location.pathname
    
    return (
        <li className={path === to ? "active" : ""}>
            <Link to={to} {...props}>{children}</Link>
        </li>
    )

}

export default Navbar