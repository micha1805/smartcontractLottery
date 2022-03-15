# Smartcontract Lottery

1. User can enter lottery with ETH based on USD fee (let say the entry fee is $50, this will be payed in ETH base on its current price)
2. An admin will choose when the lottery os over
3. The lottery will select a random winner

How do we want to test this?

1. `mainnet-fork`
2. `development` with mocks
3. `testnet`


## .env file content

You need to add a `.env`file with the following content (modified with your personal datas).
`ETHERSCAN_TOKEN` is your api key from Etherscan to verify your contracts.

```shell
export PRIVATE_KEY=0x123412341234
export WEB3_INFURA_PROJECT_ID=123412341234
export ETHERSCAN_TOKEN=123412341234
```