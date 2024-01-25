# V2 - Solana Sniper Bot

The Solana Sniper is a powerful Python-based tool designed to automate the process of buying and selling coins on the Solana blockchain. It allows you to set stop loss and limit orders, enabling you to execute trades automatically based on your predefined criteria. The sniper will snipe tokens from telegram channels based on CA or a birdeye url. Raydium has been added too because Jupiter does not support low liquidity coins.

## Whats new ? 
1) Supports fetching pool info at much faster rate.
2) Supports sniping new pools (since, it is open source, you all can modify it to your needs e.g. snipe from tg or discord or monitor pools in a naive way).
3) Instead of getting price from dexscreener. It will now calculate how much your token balance is worth in Solana
4) **Note**: Please keep in mind that if your rpc is good. You defintely will be the first one to buy a coin. I am talking about rented node or private node....
    - If it is your first time on this repo, click on the branch and check out the first-release to get an idea.

## Requirements

To use the Solana Sniper, you will need the following:

- Python 3.x installed on your machine.
- A Solana wallet with sufficient funds for trading and must have the private key in the form of alphanumeric string.
- Access to Telegram channels for receiving trade signals.
- Discord Webhook urls.
- Telegram bot api keys.
- Solana RPC Provider's HTTPS URL
- Kokiez API key

## Getting Started

1. Clone the repository and move to the directory:
    ```shell
    git clone https://github.com/kokiez/solana-sniper.git
    cd solana-sniper
    ```
2. Read it here in detail, [Click me](https://github.com/kokiez/solana-sniper/blob/main/guide.md)
- Note: Currently, the sniper is set to check for "new pool" and a solscan.com/tx/blabla url in a new message to snipe new pools... but you can change it to your liking.

## Contact

For any business inquiries, please reach out at:
- Telegram: `kokiez4000`

For Discussions and Services:
- Discord Server: [https://discord.gg/ThAb4QCV](https://discord.gg/z5cMem9MCW)

Happy trading with the Solana Sniper!

## Proof of its working

**Note**: The result is a bit different from the version in github (prices are changed to worth) as I work on the bot everyday almost to improve it. 

![1](https://github.com/kokiez/solana-sniper/assets/105941365/2131ce16-1b5c-4cd2-8838-ff0427edbd71)
![2](https://github.com/kokiez/solana-sniper/assets/105941365/f54fb612-23de-4db1-85f2-39ded1ccc516)


## Contributors:
- Update CA pattern: [Moka51](https://github.com/Moka51)
