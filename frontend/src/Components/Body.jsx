import React from 'react'
import "../index.css";

const Body = () => {
    return (
        <div className="body">
            <div className="heading">
                <h1 class="signal">Signal</h1>
                <h1 class="x">X</h1>
                <h1 class="is_a">is a better way to invest</h1>
            </div>
            <div className="btext1">
                <p1 class="p1">Meet the new standard for modern security investing. </p1>
            </div>
            <div className="btext2">
                <p1 class="p1">Streamline time-screen predictions & algorithm trading. </p1>
            </div>

            <p class= "space"/>

            <div className='search'>
                <h1 className='ticker'>Search a ticker symbol</h1>
            </div>
        </div>
    )
}

export default Body