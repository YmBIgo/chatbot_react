import React, {useState} from 'react';
import {Router, Routes, Route} from "react-router-dom"

import Chat from "./Chat"
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/user/:id" element={<Chat/>}/>
      </Routes>
    </div>
  );
}

export default App;
