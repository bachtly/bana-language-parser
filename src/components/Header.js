import React from 'react'
import {Box, Typography} from '@mui/material';
import { styled } from '@mui/material/styles'

const Img = styled('img')({
    margin: 'auto',
    display: 'block',
    maxWidth: '100%',
    maxHeight: '100%',
    height: 50,
    width: 50,
    objectFit: 'cover'
  })
  

function Header() {
  return (
      <Box sx={{
        flexDirection: 'column',
        display: 'flex',
        mb: '20vh',
      }}>
        {/* Header with logo */}
        <Box sx={{
            borderBottom: '1px black solid',
            borderColor: 'gray',
            p: 1,
        }}>
            <Img alt='HCMUT logo' src='hcmut.png' sx={{float: {xs:'center', sm: 'left'}}}/>
        </Box>
        {/* Title */}
        <Box sx={{
            textAlign:'center',
            pt: 3,
        }}>
            <Typography variant='h5' sx={{display: {xs: 'block', md:'none'}}}>Công cụ phân tích ngữ đoạn</Typography>
            <Typography variant='h4' sx={{display: {xs: 'none', md:'block'}}}>Công cụ phân tích ngữ đoạn</Typography>
            <Typography variant='h5' sx={{display: {xs: 'block', md:'none'}}}>cho tiếng Ba Na</Typography>
            <Typography variant='h4' sx={{display: {xs: 'none', md:'block'}}}>cho tiếng Ba Na</Typography>
            
        </Box>
    </Box>

  )
}

export default Header