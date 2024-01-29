# V2 - Solana Sniper Bot

The Solana Sniper is a powerful Python-based tool designed to automate the process of buying and selling coins on the Solana blockchain. It allows you to set stop loss and limit orders, enabling you to execute trades automatically based on your predefined criteria. The sniper will snipe tokens from telegram channels based on CA or a birdeye url or dexscreener url or solscan/tx/of_a_new_pool. Raydium has been added too because Jupiter does not support low liquidity coins.

## Whats new ? 
1) Supports fetching pool info at much faster rate.
2) Supports sniping new pools (since, it is open source, you all can modify it to your needs e.g. snipe from tg or discord or monitor pools in a naive way).
3) Instead of getting price from dexscreener. It will now calculate how much your token balance is worth in Solana
4) **Note**: Please keep in mind that if your rpc is good. You defintely will be the first one to buy a coin. I am talking about rented node or private node....
    - ***If it is your first time on this repo, click on the branch and check out the first-release (FREE VERSION) to get an idea.***

## Requirements

To use the Solana Sniper, you will need the following:

- Python 3.x installed on your machine.
- A Solana wallet with sufficient funds for trading and must have the private key in the form of alphanumeric string.
- Access to Telegram channels for receiving trade signals.
- Discord Webhook urls.
- Telegram bot api keys.
- Solana RPC Provider's HTTPS URL
- Kokiez API key (PAID)

## Getting Started

1. Clone the repository and move to the directory:
    ```shell
    git clone https://github.com/kokiez/solana-sniper.git
    cd solana-sniper
    ```
2. Watch the [Video](https://www.youtube.com/watch?v=ZXS4OGUE17k) or Read it here in detail, [Click me](https://github.com/kokiez/solana-sniper/blob/main/guide.md)
- Note: Currently, the sniper is set to check for "new pool" and a solscan.com/tx/blabla url in a new message to snipe new pools... but you can change it to your liking. Example:
   ```
   NEW POOL
   https://solscan.io/tx/5v5BVhWW1rT1sXKvj6i8gRCgSzNLFhEb8tfmKZMUifmFbCLFzfJCnkHgcAwcvCXnizmWMh8cT2WSDV4soJ7Pf5AP
   ```
  You can use this [channel](https://web.telegram.org/k/#@solanapoolsnew) for getting new pools but remember to change the key word "new pool" in main.py to something that is unique in the new pools channel messages from other channels you follow....

## Contact

For Business inquires, please reach out at:
- Telegram: `kokiez4000`

For Discussions and API services (my discord server):
- Discord Server: [[https://discord.gg/UXpCGW5FqW]](https://discord.gg/UXpCGW5FqW)

Happy trading with the Solana Sniper!

## Proof of its working

[Video - Click me](https://youtu.be/ZXS4OGUE17k?t=505)

## Contributors:
- Update CA pattern: [Moka51](https://github.com/Moka51)

## References

1) [https://station.jup.ag/docs/apis/swap-api](https://station.jup.ag/docs/apis/swap-api)
2) [https://github.com/v0idum/solana-swap-arbitrage-bot](https://github.com/v0idum/solana-swap-arbitrage-bot) - Was very useful repo in building the swap info - **Note:** His code is pretty old which is not compatible with current solana and solders library due to which it will give errors but raydium sdk helped in solving all the errors.
3) [https://solanacookbook.com/](https://solanacookbook.com/)
4) [https://github.com/raydium-io/raydium-sdk](https://github.com/raydium-io/raydium-sdk)
5) [https://github.com/raydium-io/raydium-frontend](https://github.com/raydium-io/raydium-frontend)
6) [https://github.com/SolanaNatives/Solana-Programming-Resources](https://github.com/SolanaNatives/Solana-Programming-Resources) - Further resources can be found here...
7) [https://michaelhly.com/solana-py/](https://michaelhly.com/solana-py/)
8) [https://www.soldev.app/course/intro-to-reading-data](https://www.soldev.app/course/intro-to-reading-data)
9) [https://kevinheavey.github.io/solders/index.html](https://kevinheavey.github.io/solders/index.html)
