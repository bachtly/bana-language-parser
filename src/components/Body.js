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

  const handleOnChangeTextField = (obj) => {
    setText(obj.target.value);
  }

  return (
    <Box sx={{
      display: 'flex',
      justifyContent:"center",
    }}>
      <Box sx={{
        width: {xs: '80%', sm: '50%', md: '40%'},
        display:"flex",
        flexDirection:"column",
        justifyContent:"center",
      }}>
        {/* Text Input Area */}
        <Box fullWidth sx={{
            display:"flex",
            flexDirection:'column',
            p: 1,
            mb:7
        }}>
          <TextField  
            label="Nhập một câu tiếng Ba Na" 
            variant="standard" 
            inputProps={{
              style: {fontSize: 15} 
            }}
            InputLabelProps={{
              style: {fontSize: 15} 
            }}                
            sx={{width: '100%', mb: 2, boxShadow: 1}}
            onChange={handleOnChangeTextField}
          />
          <Button 
            // style={{ fontSize: {xs:'10px', md: '20px'}}}
            sx={{
              height: '100%',
              width: '100%',
              border: '1px #ebebeb solid',
              fontSize: {xs:'14px', md: '20px'}
            }}
            onClick={handleOnClickBtn}
          >
            Phân tích
          </Button>
        </Box>


        {/* Result Area */}
        <Typography variant='h6' sx={{mb: 2}}>Nhãn văn phạm</Typography>
        <Box fullWidth sx={{mb:5}}>
          {items1.map((item,index)=>{
            return (
            <Box key={index} sx={{display:'flex', flexDirection:'row'}}>	
              <Box sx={{width: '40%', mr: 1}}>
                <Typography noWrap sx={{fontSize: {xs: '10', sm: '14'}, maxWidth:'100%', display:'inline-block'}}>{item.key}</Typography>
              </Box>
              :
              <Box sx={{width: '60%'}}>
                <Typography noWrap sx={{fontSize: {xs: '10', sm: '14'}, pl:2, maxWidth:'100%', display:'inline-block'}}>{item.val}</Typography>
              </Box>
            </Box>
            )
          })}
        </Box>
        
        <Typography variant='h6' sx={{mb: 2}}>Nhãn PoS</Typography>
        <Box fullWidth>
          {items2.map((item,index)=>{
            return (
            <Box key={index} sx={{display:'flex', flexDirection:'row'}}>	
              <Box sx={{width: '40%', mr:1}}>
                <Typography noWrap sx={{fontSize: {xs: '10', sm: '14'}, maxWidth:'100%', display:'inline-block'}}>{item.key}</Typography>
              </Box>
              :
              <Box sx={{width: '60%'}}>
                <Typography noWrap sx={{fontSize: {xs: '10', sm: '14'}, pl:2, maxWidth:'100%', display:'inline-block'}}>{item.val}</Typography>
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