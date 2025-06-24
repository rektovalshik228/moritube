const { ethers } = require("ethers");

const provider = new ethers.JsonRpcProvider("https://mantle-mainnet.public.blastapi.io");
const privateKey = "0xcc51935a9a4321e996e21fa6cc9d994b4ba8ea01b2404fa48bd0925ce975d780";
const wallet = new ethers.Wallet(privateKey, provider);

async function checkSignature() {
    console.log("Скрипт запущен");
    try {
        console.log("Адрес кошелька:", wallet.address);
        const message = "Funny Agents verify evm address";
        const signature = await wallet.signMessage(message);
        console.log("Подпись:", signature);
    } catch (error) {
        console.error("Ошибка:", error.message);
    }
}

checkSignature();