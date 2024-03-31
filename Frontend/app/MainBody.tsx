"use client"

import { ChangeEvent, useState, useEffect } from 'react';
import { Input, Image, ConfigProvider, Spin, Space, InputNumber, Modal } from 'antd';
import React from 'react';
import { Button, Card, Flex, Typography } from 'antd';
import { CSSTransition } from 'react-transition-group';
import { postData, ResponseData } from './api';
import { Wallet } from "../service/near-wallet";
import { Eth, MPC_CONTRACT, handleTx } from './handleNear';
import Navbar from './Navbar';
import { assetAddrMap } from '../service/ethereum';
import { LoadingOutlined } from '@ant-design/icons';
import { LinkOutlined } from '@ant-design/icons';

import "./custom.css"

const imgUrls = {
  "sFRAX": "./sFRAX.png",
  "NearX": "./NearX.svg",
  "STNEAR": "./STNEAR.svg", // Assuming you want to keep this, even though it was empty in the original object
  "USDC.e": "./USDC.e.svg",
  "USDC": "./USDC.svg",
  "USDT.e": "./USDT.e.svg",
  "USDT": "./USDT.svg",
  "WBTC": "./WBTC.svg",
  "WOO": "./WOO.svg",
  "AURORA": "./AURORA.svg",
  "BRRR": "./BRRR.png",
  "DAI": "./DAI.svg",
  "ETH": "./ETH.png",
  "FRAX": "./FRAX.png",
  "LINEAR": "./LINEAR.svg",
  "NEAR": "./NEAR.png"
};

const nearInfos = [
  "✅ Key pairs hatched!",
  "✅ 'Approve' via ABI zoomed to MPC",
  "✅ 'Approve' via ABI flew to Relay",
  "✅ 'Supply' through ABI darted to MPC",
  "✅ 'Supply' via ABI raced to Relay",
]

const cardStyle: React.CSSProperties = {
  width: 1020,
};

const inputStype: React.CSSProperties = {
  width: '100%',
  // borderColor: 'white',
  'borderRadius': '30px'
};

enum BodyState {
  Init, Loading, Showing
};

export enum NearLoadingState {
  BeforeInit, ReadyToOperate, StartedRunning, DerivedKey, ApprovedSig, ApprovedRelay, DepositedSig, DepositedRelay
};

const leftItemLeftStyle: React.CSSProperties = {
  "fontSize": "12px",
  "color": "grey",
  "marginBottom": "3px"
};

const MainBody = () => {

  // 使用TypeScript，明确状态的类型为string
  const [inputValue, setInputValue] = useState<string>('');

  const [currentState, setCurrentState] = useState<BodyState>(BodyState.Init);

  const [dataInCard, setDataInCard] = useState<ResponseData>();

  const [txAmount, setTxAmount] = useState<number>(0);

  const [nearLoadingState, setNearLoadingState] = useState<NearLoadingState>(NearLoadingState.BeforeInit);

  const wallet = new Wallet({ network: 'testnet', createAccessKeyFor: MPC_CONTRACT });

  const [isSignedIn, setIsSignedIn] = useState<boolean>(false);

  const initFunction = async () => {
    const isSignedIn = await wallet.startUp();
    setIsSignedIn(isSignedIn);
  }

  initFunction();

  const renderMessages = () => {
    console.log([NearLoadingState.StartedRunning, NearLoadingState.DerivedKey,
    NearLoadingState.ApprovedSig, NearLoadingState.ApprovedRelay,
    NearLoadingState.DepositedSig, NearLoadingState.DepositedRelay])
    console.log("Near Loading State:", nearLoadingState);
    // 初始化展示信息数组
    let infosToShow = [...nearInfos];

    // 如果dataInCard.symbol为"ETH"，移除特定信息
    if (dataInCard?.symbol === "ETH") {
      // 移除 "✅ 'Approve' via ABI zoomed to MPC" 和 "✅ 'Approve' via ABI flew to Relay"
      infosToShow = infosToShow.filter((info) =>
        info !== "✅ 'Approve' via ABI zoomed to MPC" &&
        info !== "✅ 'Approve' via ABI flew to Relay"
      );
    }
    if (nearLoadingState < NearLoadingState.StartedRunning) {
      // return an empty array if the loading state is not started
      return [];
    }
    // 生成对应状态及之前状态的信息列表
    return infosToShow.slice(0, nearLoadingState - 2).map((info, index) => (
      <div key={index}>{info}</div>
    ));
  };

  // 明确事件类型为ChangeEvent<HTMLInputElement>
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  // 点击按钮时调用的函数不需要接受任何参数
  const handleButtonClick = () => {
    console.log(inputValue);
    setCurrentState(BodyState.Loading);

    // 异步请求远端服务，在data字段中上传文本框中的文字
    postData(inputValue)
      .then(data => {
        // 这里处理成功的结果
        console.log("Data received:", data);
        setDataInCard(data);
        setCurrentState(BodyState.Showing);
      })
      .catch(error => {
        // 这里处理错误
        console.error("An error occurred:", error);
        setCurrentState(BodyState.Init);
      });
  };

  const handleClickBuy = (e: any) => {
    console.log("Buy button clicked!", e);
    setNearLoadingState(NearLoadingState.StartedRunning);

    console.log("Wallet:", wallet);
    const derivationPath = "test"
    console.log("Derivation Path:", derivationPath);
    Eth.deriveAddress(wallet.accountId, derivationPath)
      .then((address) => {
        setNearLoadingState(NearLoadingState.DerivedKey);
        let addr = address.address;
        console.log("Address:", addr);
        Eth.getBalance(addr)
          .then((balance) => {
            console.log("Balance:", balance);
          })
          .catch((e) => {
            console.error("Error in getBalance", e);
          });
        handleTx(txAmount, addr, derivationPath, wallet, dataInCard?.symbol, setNearLoadingState)
          .then((result) => {
            console.log("Result:", result);
            console.log("Transaction Hash:", result);
            console.log(`✅ Successful: https://sepolia.etherscan.io/tx/${result}`);
          })
      })
      .catch((e) => {
        setNearLoadingState(NearLoadingState.ReadyToOperate);
        console.error("Error in deriveAddress", e);
      });
  }

  return (
    <ConfigProvider
      theme={{
        components: {
          // Button: {
          //   colorPrimary: 'white',
          //   // primaryColor: 'black',
          //   algorithm: false, // 启用算法
          // },
          Input: {
            colorPrimary: 'rgb(255,255,255,0.05)',
            algorithm: true, // 启用算法
          }
        },
      }}
    >
      <Flex style={{ width: '100%' }} vertical align='center' gap={'large'}>
        <Navbar wallet={wallet} isSignedIn={isSignedIn}></Navbar>
        {(currentState === BodyState.Init || currentState === BodyState.Loading) && (
          <div>
            <Image
              width={300}
              preview={false}
              src='./logo.png'
            />
          </div>
        )}
        <Flex style={{ width: '70%' }} gap={'large'} className={'flex-container-upward'}>
          <Input size="large" style={inputStype} placeholder="e.g. I have some eth, give me some advice." onChange={handleInputChange} onPressEnter={handleButtonClick} />
          <button
            className="customButton"
            // style={{ border: "0.8px solid white"}}
            onClick={handleButtonClick}>
            Find it out!
          </button>
        </Flex>
        <Spin
          // spinning={true}
          spinning={currentState === BodyState.Loading}
          indicator={
            <LoadingOutlined
              style={{
                fontSize: 24,
                color: "white"
              }}
              spin
            />
          }
        />
        <CSSTransition
          in={currentState === BodyState.Showing}
          timeout={300}
          classNames="card"
          unmountOnExit
        >
          <Card hoverable style={cardStyle} styles={{ body: { padding: '20px', overflow: 'hidden' } }}>
            <Space direction="vertical" size={'large'}>
              <Flex justify="center">
                {(dataInCard?.state == 0 && <Flex vertical align="start" justify="flex-start" gap={'middle'} style={{ padding: 32, width: '70%' }}>
                  <Flex align='center' gap={"large"}>
                    <Image
                      width={60}
                      preview={false}
                      src={imgUrls[dataInCard?.symbol]}
                    />
                    <Flex vertical>
                      <Typography.Title level={3}>
                        {dataInCard ? (dataInCard.symbol) : "loading"}
                      </Typography.Title>
                      <Flex align='flex-end' gap={"small"}>
                        <div style={{ "fontSize": "12px", "color": "grey" }}>
                          Price:
                        </div>
                        <div style={{ "fontSize": "12px" }}>
                          ${dataInCard ? (dataInCard.price) : "loading"}
                        </div>
                      </Flex>
                    </Flex>
                  </Flex>
                  <Flex align='flex-end' gap={"small"}>
                    <div style={leftItemLeftStyle}>
                      {dataInCard?.type === 'supply' ? "Supply" : 'Borrow'} APY:
                    </div>
                    <div style={{ "fontSize": "20px" }}>
                      {dataInCard?.apy}%
                    </div>
                  </Flex>
                  <Flex align='flex-end' gap={"small"}>
                    <div style={leftItemLeftStyle}>
                      Protocol:
                    </div>
                    <div style={{ "fontSize": "20px" }}>
                      {dataInCard?.protocol}
                    </div>
                  </Flex>
                  <Flex align='flex-end' gap={"small"}>
                    <div style={leftItemLeftStyle}>
                      Chain:
                    </div>
                    <div style={{ "fontSize": "20px" }}>
                      {dataInCard?.protocol === 'burrow' ? "Near" : "Ethereum"}
                    </div>
                  </Flex>
                </Flex>)}
                <Flex vertical align="flex-end" justify="space-between" style={{ padding: 32, paddingLeft: '0px' }}>
                  <Typography.Title level={5}>
                    {dataInCard?.reply}
                  </Typography.Title>
                  <Flex align='center' gap={"large"} style={{ marginTop: '60px' }}>
                    {(dataInCard?.symbol && dataInCard.protocol === "AAVE")
                      && ((dataInCard.symbol === "ETH" || dataInCard.symbol in assetAddrMap) && dataInCard.type === "supply")
                      && (<InputNumber
                        onChange={(value) => { console.log("onchange", value); setTxAmount(value as number) }}
                        min={0} step={1}
                        size='large' addonBefore="Amount "
                        style={{ "width": "300px" }}
                      />)}
                    {(dataInCard?.symbol && dataInCard.protocol === "AAVE")
                      && ((dataInCard.symbol === "ETH" || dataInCard.symbol in assetAddrMap) && dataInCard.type === "supply")
                      && (
                        <button
                          className="customCardButton"
                          onClick={handleClickBuy}
                          >
                          Invest with Near!
                        </button>)}
                    {dataInCard?.symbol && dataInCard.protocol === "AAVE"
                      && !((dataInCard.symbol === "ETH" || dataInCard.symbol in assetAddrMap) && dataInCard.type === "supply")
                      && <div>{dataInCard.type === "supply" ? "Supplying" : "Borrowing"} {dataInCard.symbol} here is not supported now.😥</div>}
                    {dataInCard?.state == 0 && (<Button
                      size='large' shape={'round'} type='primary'
                      style={{ backgroundColor: "black", "color": "white", "paddingTop": "0px" }}
                      onClick={() => { window.open(dataInCard?.link, '_blank', 'noopener,noreferrer'); }}>
                        <LinkOutlined />
                    </Button>)}
                  </Flex>
                </Flex>
              </Flex>
            </Space>
          </Card>
        </CSSTransition>
      </Flex>
      <Modal
        title="Have a cup of coffee while waiting...☕ It may take a while."
        open={[NearLoadingState.StartedRunning, NearLoadingState.DerivedKey,
        NearLoadingState.ApprovedSig, NearLoadingState.ApprovedRelay,
        NearLoadingState.DepositedSig, NearLoadingState.DepositedRelay].includes(nearLoadingState)}
        maskClosable={false}
        closable={false}
        footer={[
          <Button
            key="ok"
            disabled={nearLoadingState !== NearLoadingState.DepositedRelay}
            onClick={() => {
              if (nearLoadingState === NearLoadingState.DepositedRelay) {
                // 当且仅当在DepositedRelay状态时关闭Modal
                setNearLoadingState(NearLoadingState.ReadyToOperate); // 或其他逻辑来更新状态
              }
            }}
          >
            All done!
          </Button>,
        ]}
      >
        {renderMessages()}
        {([NearLoadingState.StartedRunning, NearLoadingState.DerivedKey,
        NearLoadingState.ApprovedSig, NearLoadingState.ApprovedRelay,
        NearLoadingState.DepositedSig].includes(nearLoadingState)) &&
          (<Spin
            style={{ marginTop: "5px", marginLeft: "3px" }}
            spinning={nearLoadingState !== NearLoadingState.DepositedRelay}
            indicator={
              <LoadingOutlined
                style={{
                  fontSize: 12,
                  color: "green"
                }}
                spin
              />
            }
          />)}
      </Modal>
    </ConfigProvider>
  )
}

export default MainBody;