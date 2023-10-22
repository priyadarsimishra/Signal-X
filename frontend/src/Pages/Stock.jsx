import React, { useState }  from 'react'
import TradingViewWidget from '../Components/TradingViewWidget';
import Buy from "../Assets/buy.png"
import Hold from "../Assets/hold.png"
import Sell from "../Assets/sell.png"
// import { useReactTable} from "@tanstack/react-table"
import "../index.css";

const Stock = () => {
    const [nav, setNav] = useState(false)

    // const [data, setData] = useState(DATA)
    // const table = useReactTable({
    //     data,
    // })

    const handleNav = () => {
        setNav(!nav)
    }

    return (
            <div className="stock-page">
                <div className="label">
                    <h1 className="text-wrapper">Apple Inc.</h1>
                </div>
                <div className="label1">
                    <span className="text-wrapper1">NASDAQ: </span>
                    <span className="span"> AAPL <br/> </span>
                    <span className="span1">Market Summary &gt; Apple Inc.</span>
                </div>

                <div className='box'>
                    <button onClick={handleNav} className='ov'>Overview</button>
                    <button onClick={handleNav} className='fin'>Financials</button>
                </div>
                <TradingViewWidget />

                {nav ? (<div className='modal'>
                    <p className='desc'>
                        Apple Inc. is an American multinational technology company headquartered in Cupertino, California. As of March 2023, Apple is the world's biggest company by market capitalization, and with US$394.3 billion the largest technology company by 2022 revenue.
                    </p>
                    <h1 className='ceo'>CEO: Tim Cook</h1>
                    <h1 className='hq'>Headquarters: Cupertino, CA</h1>
                </div>)
                : 
                (<div>
                    <h1 className='mp'>Model Prediction:</h1>
                    <img src={Buy} className='buy-icon'/> 
                    <span className='spanner'>
                        <h1 className='buy'>Buy</h1>
                        <h1 className='sell'>Sell</h1> 
                    </span>

                    {/* <img src={Hold}/>
                    <img src={Sell}/> */}
                </div>)}
            </div>
    )
}

export default Stock