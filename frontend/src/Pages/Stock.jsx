import React, { useState, useEffect }  from 'react'
import TradingViewWidget from '../Components/TradingViewWidget';
import Buy from "../Assets/buy.png"
import Hold from "../Assets/hold.png"
import Sell from "../Assets/sell.png"
import { useParams } from "react-router-dom";
import CircularProgress from '@mui/material/CircularProgress';

import "../index.css";

const Stock = () => {
    const [nav, setNav] = useState(false);
    const [pred, setPred] = useState("");
    const [color, setColor] = useState("");
    const [shortName, setShortName] = useState("");
    const [longName, setLongName] = useState("");
    const [businessSummary, setBusinessSummary] = useState("");
    const [city, setCity] = useState("");
    const [state, setState] = useState("");
    const [CEO, setCEO] = useState("");
    const [marketCap, setMarketCap] = useState("");
    const [loading, setLoading] = useState(false);
    const { ticker } = useParams();
    // const [data, setData] = useState(DATA)
    // const table = useReactTable({
    //     data,
    // })

    useEffect(() => {
        let url_pred = `http://127.0.0.1:5000/api/get_prediction/${ticker}`
        let url_data = `http://127.0.0.1:5000/api/get_details/${ticker}`
        setLoading(true)
        fetch(url_pred)
        .then((response) => response.text())
        .then((body) => {
            let parsed = JSON.parse(body);
            // console.log(parsed)
            setPred(parsed.result.toUpperCase());
            if(parsed.result == "hold")
                setColor("yellow");
            else if(parsed.result == "sell")
                setColor("red");
            else 
                setColor("green")

            fetch(url_data)
            .then((response) => response.text())
            .then((body) => {
                // console.log(body);
                let parsed = JSON.parse(body);
                console.log("parsed: " + parsed.long_name);
                setShortName(parsed.short_name);
                setLongName(parsed.long_name);
                setBusinessSummary(parsed.business_summary);
                setCity(parsed.city);
                setState(parsed.state);
                setCEO(parsed.CEO.name);
                setMarketCap(parsed.market_cap);
                // console.log("pred:", pred)

                setLoading(false)
            })
        }); 
    }, [])

    const handleNav = (val) => {
        setNav(val);
    }

    return (
        <div>
            {loading ? 
                <div>
                    <CircularProgress color="secondary" 
                    style={{
                        width: "150px",
                        height:"150px", 
                        marginLeft: "45vw",
                        marginRight: "45vw",
                        marginTop: "35vh"
                    }}/>
                    <h1 className="loading_text">Loading...</h1>
                </div>
                : 
                (<div className="stock-page">
                     <div className="label">
                         <h1>{longName}</h1>
                     </div>
                     <div className="label1">
                         {/* <span className="text-wrapper1">NASDAQ: </span> */}
                        <span className="span"> {ticker} <br/> </span>
                         <span className="span1">Market Summary &gt; {shortName}</span>
                     </div>

                     <div className='box'>
                         <button onClick={() => handleNav(true)} className='ov'>Overview</button>
                         <button onClick={() => handleNav(false)} className='fin'>Financials</button>
                     </div>
                     <TradingViewWidget ticker={ticker}/>
                     {nav ? (
                        <div className='modal'>
                            <p className='desc'>
                                {businessSummary}
                            </p>
                            <h1 className='ceo'>CEO: {CEO}</h1>
                            <h1 className='hq'>Headquarters: {city}, {state}</h1>
                        </div>
                    )
                    : 
                    (
                        <div>
                            <h1 className='mp'>Model Prediction: <h2 className='mp_text' style={{color: color}}>{pred}</h2></h1>
                            {pred == "BUY" ? <img src={Buy} className='buy-icon'/> :
                                (pred == "SELL" ? 
                                <img src={Sell} className='buy-icon'/> 
                                    : 
                                <img src={Hold} className='buy-icon'/> 
                                )
                            }
                            <span className='spanner'>
                                <h1 className='buy'>Sell</h1>
                                <h1 className='sell'>Buy</h1> 
                            </span>
                        </div>
                    )}
                </div>
                )
            }
        </div>    
    )
}
//         {loading ? 
//              (<h1>Loading...</h1>)
//             :
//                 (<div className="stock-page">
//                     <div className="label">
//                         <h1 className="text-wrapper">Apple Inc.</h1>
//                     </div>
//                     <div className="label1">
//                         <span className="text-wrapper1">NASDAQ: </span>
//                         <span className="span"> AAPL <br/> </span>
//                         <span className="span1">Market Summary &gt; Apple Inc.</span>
//                     </div>

//                     <div className='box'>
//                         <button onClick={() => handleNav(true)} className='ov'>Overview</button>
//                         <button onClick={() => handleNav(false)} className='fin'>Financials</button>
//                     </div>
//                     <TradingViewWidget ticker={ticker}/>
//                     {nav ? (
//                         <div className='modal'>
//                             <p className='desc'>
//                                 Apple Inc. is an American multinational technology company headquartered in Cupertino, California. As of March 2023, Apple is the world's biggest company by market capitalization, and with US$394.3 billion the largest technology company by 2022 revenue.
//                             </p>
//                             <h1 className='ceo'>CEO: Tim Cook</h1>
//                             <h1 className='hq'>Headquarters: Cupertino, CA</h1>
//                         </div>
//                     )
//                     : 
//                     (
//                         <div>
//                             <h1 className='mp'>Model Prediction: <h2>{pred}</h2></h1>
//                             <img src={Buy} className='buy-icon'/> 
//                             <span className='spanner'>
//                                 <h1 className='buy'>Buy</h1>
//                                 <h1 className='sell'>Sell</h1> 
//                             </span>
        
                            
//                         </div>
//                     )}
//                 </div>
//         }
//     )
// }

            // {
            //     loading ? <h1>Loading...</h1>: (

            //         nav ? (
            //             <div className='modal'>
            //                 <p className='desc'>
            //                     Apple Inc. is an American multinational technology company headquartered in Cupertino, California. As of March 2023, Apple is the world's biggest company by market capitalization, and with US$394.3 billion the largest technology company by 2022 revenue.
            //                 </p>
            //                 <h1 className='ceo'>CEO: Tim Cook</h1>
            //                 <h1 className='hq'>Headquarters: Cupertino, CA</h1>
            //             </div>
            //         )
            //         : 
            //         (
            //             <div>
            //                 <h1 className='mp'>Model Prediction: <h2>{pred}</h2></h1>
            //                 <img src={Buy} className='buy-icon'/> 
            //                 <span className='spanner'>
            //                     <h1 className='buy'>Buy</h1>
            //                     <h1 className='sell'>Sell</h1> 
            //                 </span>
        
                            
            //             </div>
            //         )
            //     )
            // }

            
        // </div>

export default Stock;


{/* <img src={Hold}/>
                    <img src={Sell}/> */}