import React from 'react'

const DisplayData = ({response}) => {
  if(!response) return null;
  return (
    <div>
        <p>These are the most happening topics as on {response?.end_time}</p>
        <div className='datawrapper'>
            {
                [1,2,3,4,5].map((item,index) => (
                    <div key={index} className='data'>
                        <p>{response[`trend${item}`]}</p>
                    </div>
                ))
            }
           </div>
           <p>The IP address used for this query was {response?.ip_address}</p>
    </div>
  )
}

export default DisplayData