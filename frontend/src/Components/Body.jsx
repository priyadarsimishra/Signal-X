import React, { useState } from 'react'
import "../index.css";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";


const Body = () => {
    const[ticker, setTicker] = useState();
    const navigate = useNavigate();

    console.log(ticker);

    const routePage = () => 
    {
        console.log("here");
        if(ticker && ticker.length <= 4)
        {
            navigate(`/stock/${ticker.toUpperCase()}`);
        }
    }

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
                {/* <input className='ticker'>Search a ticker symbol</input> */}
                <TextField id="filled-basic" label="Search a ticker symbol" variant="filled" fullWidth margin="dense" onChange={(evt) => setTicker(evt.target.value)}/>
                {/* <input className='search_bar' type="text" id="Name" name="Name" placeholder="Jane Doe" className='ticker' /> */}
                <Button id="search-button" variant="contained" onClick={() => routePage()}>Search</Button>
            </div>
        </div>
    )
}

export default Body