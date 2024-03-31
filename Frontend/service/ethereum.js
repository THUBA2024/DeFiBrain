import { Web3 } from "web3"
import { bytesToHex } from '@ethereumjs/util';
import { FeeMarketEIP1559Transaction } from '@ethereumjs/tx';
import { deriveChildPublicKey, najPublicKeyStrToUncompressedHexPoint, uncompressedHexPointToEvmAddress } from '../service/kdf';
import { Common } from '@ethereumjs/common'
import {NearLoadingState} from '../app/MainBody';

export const assetAddrMap = {
  "USDC": "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8",
  "USDT": "0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0"
};

export class Ethereum {
  constructor(chain_rpc, chain_id) {
    this.web3 = new Web3(chain_rpc);
    this.chain_id = chain_id;
    this.queryGasPrice();
  }

  async deriveAddress(accountId, derivation_path) {
    const publicKey = await deriveChildPublicKey(najPublicKeyStrToUncompressedHexPoint(), accountId, derivation_path);
    const address = await uncompressedHexPointToEvmAddress(publicKey);
    return { publicKey: Buffer.from(publicKey, 'hex'), address };
  }

  async queryGasPrice() {
    const maxFeePerGas = await this.web3.eth.getGasPrice();
    const maxPriorityFeePerGas = await this.web3.eth.getMaxPriorityFeePerGas();
    return { maxFeePerGas, maxPriorityFeePerGas };
  }

  async getBalance(accountId) {
    const balance = await this.web3.eth.getBalance(accountId)
    const ONE_ETH = 1000000000000000000n;
    return Number(balance * 100n / ONE_ETH) / 100;
  }

  async ApproveERC20Transaction(sender, amount, wallet, MPC_CONTRACT, derivationPath, 
    assetAddr, setStateHook, asset) {
    const common = new Common({ chain: this.chain_id });

    // Get the nonce & gas price
    const nonce = await this.web3.eth.getTransactionCount(sender);
    const { maxFeePerGas, maxPriorityFeePerGas } = await this.queryGasPrice();
    const contractMethodData = this.web3.eth.abi.encodeFunctionCall({
      name: 'approve',
      type: 'function',
      inputs: [
        {type: 'address', name: 'spender'},
        {type: 'uint256', name: 'amount'},
      ]
    }, ["0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951", BigInt(Math.round(parseFloat(amount + 1) * 10 ** 6))]); // methodParams 是一个数组，包含你调用方法的参数
    // 构造交易数据
    const transactionData = {
      nonce,
      gasLimit: 2100000, // 你应该为合约调用估算一个合理的gas limit
      maxFeePerGas,
      maxPriorityFeePerGas,
      to: assetAddrMap[asset], // 合约地址
      data: contractMethodData, // 调用合约方法的编码数据
      value: "0x0", // 如果方法调用需要发送以太币，这里设置值
      chainId: this.chain_id,
    };
    // Return the message hash
    const transaction = FeeMarketEIP1559Transaction.fromTxData(transactionData, { common });
    const payload = Array.from(transaction.getHashedMessageToSign().reverse());

    
    const request = await wallet.callMethod({ MPC_CONTRACT, method: 'sign', args: { payload, path: derivationPath,  key_version: 0 }, gas: '250000000000000' });
    setStateHook(NearLoadingState.ApprovedSig);
    const [big_r, big_s] = await wallet.getTransactionResult(request.transaction.hash);

    // reconstruct the signature
    const r = Buffer.from(big_r.substring(2), 'hex');
    const s = Buffer.from(big_s, 'hex');

    const candidates = [0n, 1n].map((v) => transaction.addSignature(v, r, s));
    const signature = candidates.find((c) => c.getSenderAddress().toString().toLowerCase() === sender.toLowerCase());

    if (!signature) {
      throw new Error("Signature is not valid");
    }

    if (signature.getValidationErrors().length > 0) throw new Error("Transaction validation errors");
    if (!signature.verifySignature()) throw new Error("Signature is not valid");

    const serializedTx = bytesToHex(signature.serialize());
    const relayed = await this.web3.eth.sendSignedTransaction(serializedTx);
    setStateHook(NearLoadingState.ApprovedRelay);
  }
  
  async createPayload(sender, amount, asset, wallet, MPC_CONTRACT, derivationPath, setStateHook) {   //asset输入代币名称
    const common = new Common({ chain: this.chain_id });

    // Get the nonce & gas price
    const nonce = await this.web3.eth.getTransactionCount(sender);
    const { maxFeePerGas, maxPriorityFeePerGas } = await this.queryGasPrice();
    
    // // Construct transaction
    // const transactionData = {
    //   nonce,
    //   gasLimit: 21000,
    //   maxFeePerGas,
    //   maxPriorityFeePerGas,
    //   to: receiver,
    //   value: BigInt(this.web3.utils.toWei(amount, "ether")),
    //   chain: this.chain_id,
    // };
    let transactionData = {};


    if (asset === "ETH"){
      const contractMethodData = this.web3.eth.abi.encodeFunctionCall({
        name: 'depositETH',
        type: 'function',
        inputs: [
          {type: 'address', name: ''},
          {type: 'address', name: 'onBehalfOf'},
          {type: 'uint16', name: 'referralCode'},
        ]
      }, ['0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951',sender,0]); // methodParams 是一个数组，包含你调用方法的参数
      // 构造交易数据
      transactionData = {
        nonce,
        gasLimit: 2100000, // 你应该为合约调用估算一个合理的gas limit
        maxFeePerGas,
        maxPriorityFeePerGas,
        to: "0x387d311e47e80b498169e6fb51d3193167d89F7D", // 合约地址
        data: contractMethodData, // 调用合约方法的编码数据
        value: BigInt(this.web3.utils.toWei(amount, "ether")), // 如果方法调用需要发送以太币，这里设置值
        chainId: this.chain_id,
      };
    }else if (asset in assetAddrMap){
      
      await this.ApproveERC20Transaction(sender, amount, wallet, MPC_CONTRACT, 
        derivationPath, assetAddrMap[asset], setStateHook, asset);
      const nonce = await this.web3.eth.getTransactionCount(sender);
      const contractMethodData = this.web3.eth.abi.encodeFunctionCall({
        name: 'supply',
        type: 'function',
        inputs: [
          {type: 'address', name: 'asset'},
          {type: 'uint256', name: 'amount'},
          {type: 'address', name: 'onBehalfOf'},
          {type: 'uint16', name: 'referralCode'},
        ]
      }, [assetAddrMap[asset],BigInt(Math.round(parseFloat(amount) * 10 ** 6)),sender,0]); // methodParams 是一个数组，包含你调用方法的参数

      // 构造交易数据
      transactionData = {
        nonce,
        gasLimit: 2100000, // 你应该为合约调用估算一个合理的gas limit
        maxFeePerGas,
        maxPriorityFeePerGas,
        to: "0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951", // 合约地址
        //to: "0x0562453c3dafbb5e625483af58f4e6d668c44e19",
        data: contractMethodData, // 调用合约方法的编码数据
        //value: '0x0',
        chainId: this.chain_id,
      };
    }else{
      throw new Error("asset not supported");
    }
    console.log(transactionData);

    // Return the message hash
    const transaction = FeeMarketEIP1559Transaction.fromTxData(transactionData, { common });
    const payload = transaction.getHashedMessageToSign();
    return { transaction, payload };
  }

  async requestSignatureToMPC(wallet, contractId, path, ethPayload, transaction, sender) {
    // Ask the MPC to sign the payload
    const payload = Array.from(ethPayload.reverse());
    const request = await wallet.callMethod({ contractId, method: 'sign', args: { payload, path, key_version: 0 }, gas: '250000000000000' });
    const [big_r, big_s] = await wallet.getTransactionResult(request.transaction.hash);

    // reconstruct the signature
    const r = Buffer.from(big_r.substring(2), 'hex');
    const s = Buffer.from(big_s, 'hex');

    const candidates = [0n, 1n].map((v) => transaction.addSignature(v, r, s));
    const signature = candidates.find((c) => c.getSenderAddress().toString().toLowerCase() === sender.toLowerCase());

    if (!signature) {
      throw new Error("Signature is not valid");
    }

    if (signature.getValidationErrors().length > 0) throw new Error("Transaction validation errors");
    if (!signature.verifySignature()) throw new Error("Signature is not valid");

    return signature;
  }

  // This code can be used to actually relay the transaction to the Ethereum network
  async relayTransaction(signedTransaction) {
    console.log("signedTransaction in relayTransaction", signedTransaction);
    const serializedTx = bytesToHex(signedTransaction.serialize());
    console.log("serializedTx in relayTransaction", serializedTx);
    const relayed = await this.web3.eth.sendSignedTransaction(serializedTx);
    console.log("relayed in relayTransaction", relayed);
    return relayed.transactionHash
  }
}