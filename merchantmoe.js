const { ethers } = require("ethers");

// Конфигурация с проверенными параметрами
const CONFIG = {
  RPC_URL: "https://rpc.ankr.com/mantle", // Альтернативный надежный RPC
  PRIVATE_KEY: "0xcc51935a9a4321e996e21fa6cc9d994b4ba8ea01b2404fa48bd0925ce975d780",
  
  // Проверенные адреса контрактов
  ADDRESSES: {
    ROUTER: "0x45a62b090df48243f12a21897e7ed91863e2c86b",
    WMNT: "0x78c1b0c915c4faa5fffa6cabf0219da63d7f4cb8",
    MOE: "0x4515a45337f461a11ff0fe8abf3c606ae5dc00c9"
  },

  // Оптимальные параметры газа
  GAS_SETTINGS: {
    PRICE_GWEI: 1.5, // Увеличенный gas price
    LIMIT: 3500000    // Увеличенный gas limit
  },

  // Настройки свапа
  SWAP: {
    SLIPPAGE: 3, // 3% slippage
    AMOUNT: "0.001" // 0.001 MNT
  }
};

// Минимальный ABI для работы
const ABI = {
  ROUTER: [
    // Упрощенный ABI для избежания ошибок
    "function swapExactETHForTokens(uint256 amountOutMin, address[] path, address to, uint256 deadline) payable returns (uint[] amounts)"
  ]
};

async function executeSwap() {
  try {
    // 1. Инициализация провайдера и кошелька
    const provider = new ethers.JsonRpcProvider(CONFIG.RPC_URL);
    const wallet = new ethers.Wallet(CONFIG.PRIVATE_KEY, provider);
    
    // 2. Проверка баланса
    const balance = await provider.getBalance(wallet.address);
    console.log(`💰 Баланс: ${ethers.formatEther(balance)} MNT`);
    
    const amountIn = ethers.parseUnits(CONFIG.SWAP.AMOUNT, 18);
    if (balance < amountIn) {
      throw new Error("Недостаточно средств для свапа");
    }

    // 3. Подготовка параметров транзакции
    const router = new ethers.Contract(
      CONFIG.ADDRESSES.ROUTER,
      ABI.ROUTER,
      wallet
    );

    const path = [CONFIG.ADDRESSES.WMNT, CONFIG.ADDRESSES.MOE];
    const deadline = Math.floor(Date.now() / 1000) + 600; // 10 минут
    
    // 4. Отправка транзакции без предварительной проверки getAmountsOut
    const tx = await router.swapExactETHForTokens(
      1, // Минимальное количество (1 wei токена)
      path,
      wallet.address,
      deadline,
      {
        value: amountIn,
        gasPrice: ethers.parseUnits(CONFIG.GAS_SETTINGS.PRICE_GWEI.toString(), "gwei"),
        gasLimit: CONFIG.GAS_SETTINGS.LIMIT
      }
    );

    console.log(`✅ Транзакция отправлена: https://mantlescan.xyz/tx/${tx.hash}`);
    const receipt = await tx.wait();
    console.log(`🟢 Успешно! Блок: ${receipt.blockNumber}`);

  } catch (error) {
    console.error("❌ Критическая ошибка:", error.message);
    if (error.transactionHash) {
      console.log(`🔗 Проверить транзакцию: https://mantlescan.xyz/tx/${error.transactionHash}`);
    }
    process.exit(1);
  }
}

// Запуск
executeSwap();