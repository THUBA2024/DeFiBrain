"use client"

import React from 'react';
import MainBody from './MainBody';
import { Flex } from 'antd';

const gradientBackgroundStyle: React.CSSProperties = {
  background: 'linear-gradient(to right top, #0B0610, transparent ), linear-gradient(to left bottom, #2592E5, #8F50D6 40%), linear-gradient(to right top, #2592E5, #8F50D6 40%)',
  
  // backgroundPosition: 'center, left bottom, center',
  // backgroundRepeat: 'no-repeat',
  height: '100vh',
  width: '100%',
  color: '#333',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'start',
  backgroundColor:"black",
  'minHeight': '100vh',
  'padding': '90px'
  // padding: '100px 0 0 24px' /* 根据Tailwind的配置，24应等于6rem，如果你的配置不同，请调整 */
};

export default function Home() {
  return (
      <Flex vertical gap={'large'}
        style={gradientBackgroundStyle}
        // className={"flex w-full min-h-screen flex-col items-center justify-between p-24"}
      >
        <div style={{width: '100%', display: "flex", flexDirection: "row", justifyContent: "flex-end"}}>
          {/* <NearWalletConnectButton/> */}
        </div>

        <div style={{width:"100%"}}>
          <MainBody />
        </div>
        <div></div>
      </Flex>
  );
}


