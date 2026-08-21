# Assignment — Mempool and Wallet Programming

*Lesson: [Mempool and Wallet Programming](README.md)*

**Due:** Next class
**Points:** 25

---

Create a working Bitcoin **testnet** wallet in Java using the BitcoinJ library.

> **Warning:**
> Testnet only. Never point this program at the main Bitcoin network, never fund it with real money, and never share a private key or seed phrase with anyone.

## Steps

1. Create a new Java project (VS Code or your usual setup) with a Gradle or Maven build file.
2. Add the BitcoinJ dependency — for Gradle:

```
dependencies {
    implementation 'org.bitcoinj:bitcoinj-core:0.16.2'
    implementation 'org.slf4j:slf4j-simple:1.7.36'
}
```

3. Create `ClassWallet.java`:

```java
import java.io.File;
import org.bitcoinj.core.Coin;
import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.kits.WalletAppKit;
import org.bitcoinj.params.TestNet3Params;

public class ClassWallet {
    public static void main(String[] commandLineArguments) {
        // Testnet coins are worthless play-money - exactly what we want.
        NetworkParameters testNetwork = TestNet3Params.get();

        // WalletAppKit creates the wallet files on first run and reloads
        // them on every later run, then syncs with the testnet.
        WalletAppKit walletKit = new WalletAppKit(testNetwork, new File("."), "class-wallet");
        walletKit.startAsync();
        walletKit.awaitRunning();

        System.out.println("My testnet receive address: " + walletKit.wallet().freshReceiveAddress());
        System.out.println("Current balance: " + walletKit.wallet().getBalance().toFriendlyString());

        // Announce it when coins arrive from the faucet.
        walletKit.wallet().addCoinsReceivedEventListener((wallet, transaction, previousBalance, newBalance) -> {
            Coin receivedAmount = newBalance.subtract(previousBalance);
            System.out.println("Received " + receivedAmount.toFriendlyString()
                    + " in transaction " + transaction.getTxId());
        });

        // Keep the program alive so it can hear about incoming coins.
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        }
    }
}
```

4. Run the program. The first sync can take a few minutes — watch the log lines while it catches up with the chain.
5. Copy the receive address it prints and request coins from a Bitcoin **testnet faucet** (for example [coinfaucet.eu](https://coinfaucet.eu/en/btc-testnet/) — search "bitcoin testnet faucet" if it is dry).
6. Leave the program running until it announces the received coins, then take your screenshot.

## Extra Credit

Send some of your testnet bitcoin to another person in class. Get a classmate's receive address and add a send after the sync completes:

```java
walletKit.wallet().sendCoins(walletKit.peerGroup(),
        org.bitcoinj.core.Address.fromString(testNetwork, "CLASSMATE_ADDRESS_HERE"),
        Coin.parseCoin("0.0001"));
```

Record the transaction ID it prints, and have your classmate confirm the coins arrived.

---

## Success Criteria

Confirm each of the following before submitting:

- [ ] **Project builds** — the BitcoinJ dependency resolves and the program compiles
- [ ] **Testnet only** — the program uses `TestNet3Params.get()` and nothing else
- [ ] **Address printed** — your program prints a testnet receive address on startup
- [ ] **Coins received** — the faucet coins arrived and your program printed the received amount and transaction ID
- [ ] **Extra credit (optional)** — you sent testnet coins to a classmate and both of you can name the transaction ID

---

## Submission

Submit **both text and a screenshot** on Canvas.

### Text response

Copy the stencil, fill in each line, and paste it into the Canvas text box:

```
Testnet receive address:         
Faucet used:                     
Received transaction ID:         
Extra credit - sent to (name):   
Extra credit - send tx ID:       
```

### Screenshot

Your running program's output showing the printed receive address, the balance, and the "Received ..." line after the faucet coins arrived. Do **not** include any seed phrase or private key in the screenshot — a screenshot showing a seed phrase will be rejected.
