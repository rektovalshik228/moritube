import random
from web3 import Web3
from web3 import Account

# Подключение к сети Arbitrum
rpc_url = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Проверка подключения
if not web3.is_connected():
    print("Не удалось подключиться к Arbitrum")
    exit()

# Приватный ключ отправителя (замените на свой)
private_key = "0x7f1d17234011522a24b3958560e13da2147a0c2930cee476ccbc3acb2161f5b4"
account = Account.from_key(private_key)
sender_address = account.address

# Список адресов получателей
recipients = [
    "0x3d8fd597118d8203020715ddec9246b79c06e4eb",
    "0x3b4f20cfacb7413012a332dd5da454d14ceac75c",
    "0x30269c1c06267f8f2b8aa824f1267219e465955b",
    "0x683d5b0cc5b0a66bc09ce86b334b19fe1fe4ae6c",
    "0xbda3641751c41b6a732ec71b162b7e4f17b89ccb"
]

# Диапазон сумм для отправки (в ETH)
min_amount_eth = 0.0000015
max_amount_eth = 0.0000016

# Chain ID для Arbitrum One
chain_id = 42161

# Получение начального значения nonce
nonce = web3.eth.get_transaction_count(sender_address)

# Отправка транзакций каждому получателю
for recipient in recipients:
    recipient = web3.to_checksum_address(recipient)
    
    # Генерация случайной суммы
    amount_eth = random.uniform(min_amount_eth, max_amount_eth)
    amount_wei = web3.to_wei(amount_eth, 'ether')
    
    # Получение текущей базовой комиссии
    fee_history = web3.eth.fee_history(1, 'latest')
    base_fee = fee_history['baseFeePerGas'][0]
    
    # Установка параметров газа
    max_priority_fee_per_gas = 0
    max_fee_per_gas = base_fee
    
    # Формирование транзакции
    transaction = {
        'to': recipient,
        'value': amount_wei,
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
        'nonce': nonce,
        'chainId': chain_id
    }
    
    # Оценка газа
    try:
        transaction_for_estimation = transaction.copy()
        transaction_for_estimation['from'] = sender_address
        gas_estimate = web3.eth.estimate_gas(transaction_for_estimation)
        transaction['gas'] = int(gas_estimate * 1.2)  # Добавляем 20% буфер
    except Exception as e:
        print(f"Ошибка при оценке газа для {recipient}: {e}")
        continue
    
    # Подписание и отправка транзакции
    signed_txn = account.sign_transaction(transaction)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Отправлена транзакция на {recipient} с суммой {amount_eth:.10f} ETH, tx hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"Ошибка при отправке на {recipient}: {e}")
    
    # Увеличение nonce
    nonce += 11