# EXAMPLE TO LEARN FROM - NOT TO RESUBMIT.
# This is the worked example from the lesson. Your homework contract must be
# UNIQUE from this code while meeting all four requirements:
#   1. uses an environment variable   (shown here: tx.gasprice)
#   2. has at least one assert        (shown here, with a message)
#   3. calls one Vyper built-in function
#      (NOT shown here - you must add one; see the built-in functions docs)
#   4. has an @external method with inputs AND outputs (shown here)
#
# The gamble method belongs inside a token contract, so the two pieces of
# token state it touches are declared here. In the full ERC20 example these
# same names track every holder's balance and the total number of tokens.

balanceOf: public(HashMap[address, uint256])
totalSupply: public(uint256)


@external
def gamble(_gambleAmount: uint256, _walletAddress: address) -> (bool):
    # Don't allow them to run this unless they have 50x the tokens to lose
    assert self.balanceOf[_walletAddress] > (_gambleAmount * 50), "You don't have enough to gamble"

    # If the transaction's gas price is odd, then you win the gamble amount!
    # 1/2 the time it's a win!
    if (tx.gasprice % 2 == 1):
        self.balanceOf[_walletAddress] += _gambleAmount
        self.totalSupply += _gambleAmount

    # If the transaction's gas price's mod 11 is 7, then you lose 50 times
    # the amount you gambled!
    # 1/11 the time you lose 50x! Yikes!
    if (tx.gasprice % 11 == 7):
        self.balanceOf[_walletAddress] -= _gambleAmount * 50
    return (True)
