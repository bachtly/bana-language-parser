import React from 'react';
import Header from './components/Header';
import Body from './components/Body';
import ReactDOM from 'react-dom/client';
import { Box } from '@mui/material';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Box>
    <Header/>
    <Body/>
  </Box>
);