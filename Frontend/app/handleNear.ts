import { Ethereum } from "../service/ethereum";
import { NearLoadingState } from "./MainBody";

const Sepolia = 11155111;
export const Eth = new Ethereum('https://rpc2.sepolia.org', Sepolia);

export const MPC_CONTRACT = 'multichain-testnet-2.testnet';

async function chainSignature(senderAddress: any, amount: any, wallet: any, MPC_CONTRACT: any, derivationPath: any, asset: any, setStateHook:Function) {
    const { transaction, payload } = await Eth.createPayload(senderAddress, amount, asset, wallet, MPC_CONTRACT, derivationPath, setStateHook);

    try {
        const signedTransaction = await Eth.requestSignatureToMPC(wallet, MPC_CONTRACT, derivationPath, payload, transaction, senderAddress);
        setStateHook(NearLoadingState.DepositedSig)
        return signedTransaction;
    } catch (e) {
        setStateHook(NearLoadingState.ReadyToOperate)
        console.error("err in chainSignature", e);
        throw e;
    }
}

async function relayTransaction(signedTransaction: any) {
    try {
        const txHash = await Eth.relayTransaction(signedTransaction);
        return txHash;
    } catch (e) {
        console.error("err in relayTransaction", e);
        throw e;
    }
}

export async function handleTx(amount: number, senderAddress: string, derivationPath: string, wallet: any, asset: string, setStateHook: Function) {
    try {
        // 使用 await 等待 chainSignature 完成，并获取 signedTransaction
        const signedTransaction = await chainSignature(senderAddress, amount, wallet, MPC_CONTRACT, derivationPath, asset, setStateHook);  
        console.log("Signed Transaction:", signedTransaction);
        // 使用 await 等待 relayTransaction 完成，并获取 txHash
        const txHash = await relayTransaction(signedTransaction);
        setStateHook(NearLoadingState.DepositedRelay)
        console.log("Transaction Hash:", txHash);

        txHash && console.log(`✅ Successful: https://sepolia.etherscan.io/tx/${txHash}`);

        // 在所有异步操作成功完成后返回 txHash
        return txHash;
    } catch (e) {
        setStateHook(NearLoadingState.ReadyToOperate);
        // 捕获 chainSignature 或 relayTransaction 中的任何错误
        console.error("Error in transaction process", e);
    }
    // 如果有必要，这里可以处理后续逻辑
    console.log("Transaction process completed");
}

