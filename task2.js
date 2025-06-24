const { ethers } = require("ethers");

const provider = new ethers.JsonRpcProvider("https://mantle-mainnet.public.blastapi.io");
const privateKey = "0xaa4593e62b23e6ba509a58fa42f2c0493f7adfa858361ba77628b9d6b482f831";
const wallet = new ethers.Wallet(privateKey, provider);

async function doTask() {
    try {
        console.log("Адрес кошелька:", wallet.address);

        const network = await provider.getNetwork();
        console.log("Сеть:", network.chainId === 5000n ? "Mantle" : `Не Mantle! chainId=${network.chainId}`);

        const balance = await provider.getBalance(wallet.address);
        console.log("Баланс:", ethers.formatEther(balance), "MNT");
        
        if (balance <= ethers.parseEther("0.0001")) {
            throw new Error("Недостаточно $MNT для газа!");
        }

        const feeData = await provider.getFeeData();

        const txData = {
            to: "0x356a5304b1396f8c4f57561fc57b804b0401ee40",
            data: "0xa9c2dbcf0000000000000000000000000000000000000000000000000000000000004e21000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000e4461696c7920636865636b2d696e000000000000000000000000000000000000",
            maxPriorityFeePerGas: feeData.maxPriorityFeePerGas,
            maxFeePerGas: feeData.maxFeePerGas
        };

        txData.gasLimit = await provider.estimateGas(txData);
        console.log("Оценочный gasLimit:", txData.gasLimit.toString());

        const tx = await wallet.sendTransaction(txData);

        console.log("Транзакция отправлена:", tx.hash);
        await tx.wait();
        console.log("Транзакция выполнена:", tx.hash);
    } catch (error) {
        console.error("Ошибка:", error.message);
    }
}

doTask();
 