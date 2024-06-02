import React, { useState } from 'react'
import Loader from './Loader';
import DisplayData from './DisplayData';
import toast from 'react-hot-toast';
import axios from 'axios';
const url = process.env.API_URLn || 'http://127.0.0.1:5000/api/get_trending_topics';


const App = () => {
  const [method,setmethod] = useState('GET');
  const [data,setdata] = useState({'username':'','password':''});
  const [loading,setloading] = useState(false);
  const [response,setresponse] = useState(null);

  const getTrandingData = async () => {
    if(!url) return toast.error('API URL not found');
    if(method === 'POST' && (!data?.username || !data?.password)) return toast.error('Please enter username and password for POST method');
    try {
      setloading(true);
      let res;
      if(method === 'GET'){
        res = await axios.get(url);
      }else{
        res = await axios.post(url,{username:data.username,password:data.password});
      }
      if(res.data?.error) return toast.error(res.data.error); 
      setresponse(res.data);
    } catch (error) {
      toast.error(error?.message || 'Something went wrong');
    }finally{
      setloading(false);
    }
  }
  return (
    <div className='wrapper'>
       <div className='inputwrapper'>
       <div className='optioninput'>
        <div>  
        <input  onChange={(e)=>setmethod(e.target.value)}  type='radio' value={'POST'}  checked={method==='POST'} name='methodtype' id='p'/>
        <label htmlFor='p'>Give your own  user id and password</label>
        </div>
        <div>
        <input onChange={(e)=>setmethod(e.target.value)} type='radio' value={'GET'} checked={method==='GET'} name='methodtype' id='g'/>
        <label htmlFor='g'>Proceed with default parameters</label>
        </div>
       </div>
       {
          method === 'POST' &&
          <div className='valueinput'>
          <input onChange={(e)=>setdata({...data,'username':e.target.value})} type='text' placeholder='Enter user name' className='ipbox' />
          <input onChange={(e)=>setdata({...data,'password':e.target.value})} type='password' placeholder='Enter password' className='ipbox' />
          </div>
       }
       </div>
       {
        loading ? <Loader/>: <DisplayData response = {response} />
       }
       <button disabled={loading} onClick={getTrandingData} className='btn'>Fetch Result</button>
    </div>
  )
}

export default App