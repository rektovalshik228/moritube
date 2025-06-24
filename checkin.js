const { ethers } = require("ethers");

const provider = new ethers.JsonRpcProvider("https://rpc.mantle.xyz");
const privateKey = "0xaa4593e62b23e6ba509a58fa42f2c0493f7adfa858361ba77628b9d6b482f831"; 
const wallet = new ethers.Wallet(privateKey, provider);

const contractAddress = "0xbd82e1a3f908afb789f1f0b8f88b1fd0c2787a3d";
const abi = [
  "function claim(uint256 uid, uint256 deadline, uint256 param, bytes signature) public"
];
const contract = new ethers.Contract(contractAddress, abi, wallet);

async function doCheckIn() {
  try {
    const uid = "0x6f7001ecf36b";
    const deadline = "1741906724";
    const param = "1763476384";
    const signature = "0xdc61941bbecba54a26af6e199b69c3dd01c73c593bc9a588a992ba17af376a9f61b116279940f22301120b723054f48ea07d7be7be1746bfe1bb87852b0ae21b1b";

    const tx = await contract.claim(uid, deadline, param, signature);
    await tx.wait();
    console.log("Транзакция выполнена:", tx.hash);
  } catch (error) {
    console.error("Ошибка:", error.message);
  }
}

doCheckIn();