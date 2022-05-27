import React from 'react'
import {TextField, Box, Button, Typography} from '@mui/material';
import { useState } from 'react';
import io from 'socket.io-client'

const socket = io('ws://127.0.0.1:1410');

function Body() {
  const [text, setText] = useState('');
	const [items1, setItems1] = useState([]);
	const [items2, setItems2] = useState([]);
  const [listenSocket, setListenSocket] = useState(false);

  const listen = () => {
		socket.on('parse', function(data) {
      console.log('Data from api');
      console.log(data.data);
      setItems1(data.data[0]);
      setItems2(data.data[1]);
    })
	}

  const handleOnClickBtn = () => {
    socket.emit('parse', text);
    if (!listenSocket) {
      listen();
      setListenSocket(true);
    }
  }

  return (
    <Box sx={{
      display: 'flex',
      justifyContent:"center",
    }}>
      <Box sx={{
        width: '40%',
        display:"flex",
        flexDirection:"column",
        justifyContent:"center",
      }}>
        {/* Text Input Area */}
        <Box fullWidth sx={{
            display:"flex",
            flexDirection:'column',
            p: 1,
        }}>
          <TextField  
            label="Nhập một câu tiếng Ba Na" 
            variant="standard" 
            inputProps={{
              style: {fontSize: 25} 
            }}
            InputLabelProps={{
              style: {fontSize: 25} 
            }}                
            sx={{width: '100%', mb: 2, boxShadow: 1}}
            onChange={(obj) => {setText(obj.target.value)}}
          />
          <Button 
            style={{ fontSize: '20px'}}
            sx={{
              height: '100%',
              width: '100%',
              border: '1px #ebebeb solid'
            }}
            onClick={handleOnClickBtn}
          >
            Phân tích
          </Button>
        </Box>


        {/* Result Area */}
        <Box fullWidth>
          {items1.map((item,index)=>{
            return (
            <Box key={index} sx={{display:'flex', flexDirection:'row'}}>	
              <Box sx={{width: '50%'}}>
                <Typography noWrap sx={{fontSize: 18, fontWeight:500, maxWidth: '70%', display:'inline-block'}}>{item.key}</Typography>
              </Box>
              <Box sx={{width: '50%'}}>
                <Typography noWrap sx={{fontSize: 18, fontWeight:500, maxWidth: '70%', display:'inline-block'}}>{item.val}</Typography>
              </Box>
            </Box>
            )
          })}
        </Box>

        <Box fullWidth>
          {items2.map((item,index)=>{
            return (
            <Box key={index} sx={{display:'flex', flexDirection:'row'}}>	
              <Box sx={{width: '50%'}}>
                <Typography noWrap sx={{fontSize: 18, fontWeight:500, maxWidth: '70%', display:'inline-block'}}>{item.key}</Typography>
              </Box>
              <Box sx={{width: '50%'}}>
                <Typography noWrap sx={{fontSize: 18, fontWeight:500, maxWidth: '70%', display:'inline-block'}}>{item.val}</Typography>
              </Box>
            </Box>
            )
          })}
        </Box>

      </Box>
    </Box>
  )
}

export default Body