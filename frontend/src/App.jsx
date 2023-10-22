import { useState } from 'react'
import Navbar from './Components/Navbar';
import Body from './Components/Body';
import Stock from './Pages/Stock';
import Signup from './Pages/Signup';
import Login from './Pages/Login';
import "./index.css";
import { Route, Routes } from 'react-router-dom';

function App() {

  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Body />} />
        <Route path="/login" element={<Login />} />
        <Route path="/stock/:ticker" element={<Stock />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </div>
  )
}

export default App