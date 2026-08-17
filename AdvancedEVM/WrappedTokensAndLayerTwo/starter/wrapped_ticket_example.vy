# pragma version ^0.4.0
"""
wrapped_ticket_example.vy — THE STUDIED EXAMPLE, not your submission.

This is the wrapper contract walked through in class. Read it top to
bottom, run it on the Sepolia testnet, then write YOUR OWN variant for
the assignment. Your variant must fix at least one of the DESIGN
QUESTION comments below.

The question: how can a contract hold tokens that belong to a totally
different contract?
The answer: a contract has an address just like a person does. Send
tokens to that address and the contract owns them — a vault whose only
key is the code below.

The deal this vault offers:
    wrap:   deposit 1000 ticket tokens  ->  receive 1 wrapped ticket
    unwrap: burn    1 wrapped ticket    ->  get back 1000 ticket tokens
"""

# The ERC-20 interface — the standard "shape" every ticket token from the
# Blockchains module shares. Importing it lets this contract call
# transferFrom / transfer / balanceOf on ANY token that follows the
# standard, without knowing anything else about it.
from ethereum.ercs import IERC20

# ---------------------------------------------------------------------------
# The wrapped token's own bookkeeping.
# These two names are NOT ours to choose: the ERC-20 standard requires
# getters called totalSupply() and balanceOf(address), and marking the
# variables public makes Vyper generate those getters for us.
# ---------------------------------------------------------------------------
totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])

# The exchange rate, fixed at deploy time: 1000 ticket tokens buy exactly
# 1 wrapped ticket. Named as a constant so the ratio appears once, not
# scattered as a magic number through the math.
TICKETS_PER_WRAPPED: constant(uint256) = 1000


@external
def wrapToken(ticket_token_address: address, ticket_amount: uint256):
    """
    Deposit `ticket_amount` of the token at `ticket_token_address` into
    the vault and mint wrapped tickets at 1000:1.

    BEFORE anyone calls this, they must call approve(this_contract,
    ticket_amount) ON THE TICKET TOKEN ITSELF — otherwise transferFrom
    below is a stranger reaching into their pocket, and it reverts.
    """
    # Validation first: the ratio makes anything under 1000 round to zero
    # wrapped tickets, which would swallow the deposit and mint nothing.
    assert ticket_amount >= TICKETS_PER_WRAPPED, "Minimum 1000 tickets required"

    # Integer division: 1000 tickets -> 1 wrapped, 2000 -> 2, and so on.
    #
    # DESIGN QUESTION 1: what happens to a deposit of 1500? The division
    # yields 1 wrapped ticket, but the vault keeps all 1500 originals —
    # 500 tickets vanish from the depositor's point of view. Your variant
    # should reject non-multiples of 1000, or wrap only the part that
    # divides evenly and leave the rest untouched.
    wrapped_amount: uint256 = ticket_amount // TICKETS_PER_WRAPPED

    # --- SECURITY: contracts can lie -------------------------------------
    # We are about to trust a contract we did not write. staticcall only
    # stops the token from MODIFYING state during the call — it does NOT
    # stop the token from REPORTING whatever numbers it likes. A malicious
    # token's balanceOf can simply return arbitrary values, and a malicious
    # transferFrom can return True while moving nothing.
    #
    # Defense used here: measure the vault's balance before and after the
    # transfer, and insist the vault ACTUALLY grew by the amount claimed.
    # Even that only proves this token's own bookkeeping is self-
    # consistent. Stronger defenses your variant can add:
    #   - verify the token's source code is the genuine token you expect
    #   - keep a trusted token list and refuse everything not on it
    # ----------------------------------------------------------------------
    tickets_held_before: uint256 = staticcall IERC20(ticket_token_address).balanceOf(self)

    # Pull the original tickets from the depositor into this vault.
    transfer_succeeded: bool = extcall IERC20(ticket_token_address).transferFrom(
        msg.sender, self, ticket_amount
    )
    assert transfer_succeeded, "Transfer failed"

    tickets_held_after: uint256 = staticcall IERC20(ticket_token_address).balanceOf(self)
    assert tickets_held_after - tickets_held_before == ticket_amount, "Vault did not receive the tickets"

    # Only now that the vault provably holds the originals do we mint.
    # Mint-before-lock would break the invariant that every wrapped ticket
    # is backed by 1000 real ones sitting in the vault.
    self.totalSupply += wrapped_amount
    self.balanceOf[msg.sender] += wrapped_amount


@external
def unwrapToken(ticket_token_address: address, wrapped_amount: uint256):
    """
    Burn `wrapped_amount` wrapped tickets and release the original tokens
    from the vault at 1:1000.

    DESIGN QUESTION 2: this function trusts the caller to name the same
    token they wrapped. This vault never remembers WHICH token backs
    WHICH wrapped ticket — so a caller who wrapped a worthless token
    could try to unwrap into a valuable one the vault also holds. Your
    variant should remember what was wrapped (store the token address at
    deploy time, or keep per-token accounting).
    """
    original_amount: uint256 = wrapped_amount * TICKETS_PER_WRAPPED

    # Burn first: subtract from the caller's balance and from totalSupply
    # so the wrapped tickets cease to exist BEFORE any tokens leave the
    # vault. Paying out before burning would let a caller be paid twice.
    assert self.balanceOf[msg.sender] >= wrapped_amount, "Insufficient wrapped tokens"
    self.balanceOf[msg.sender] -= wrapped_amount
    self.totalSupply -= wrapped_amount

    # Release the originals. No approve step is needed on this side —
    # the vault owns these tokens and may send its own property freely.
    transfer_succeeded: bool = extcall IERC20(ticket_token_address).transfer(
        msg.sender, original_amount
    )
    assert transfer_succeeded, "Transfer failed"


# ---------------------------------------------------------------------------
# Helper view functions — free to call, change nothing. Use these to check
# your math before spending gas on the real thing. (Balances and total
# supply already have free getters from the public variables above.)
# ---------------------------------------------------------------------------

@external
@view
def previewWrap(ticket_amount: uint256) -> uint256:
    """How many wrapped tickets would a deposit of `ticket_amount` mint?"""
    return ticket_amount // TICKETS_PER_WRAPPED


@external
@view
def previewUnwrap(wrapped_amount: uint256) -> uint256:
    """How many original tickets does burning `wrapped_amount` release?"""
    return wrapped_amount * TICKETS_PER_WRAPPED


# TESTING CHECKLIST (from class — do these on Sepolia, in this order):
#   1. Test with small amounts first: approve 1000, wrap 1000, expect 1.
#   2. Verify the ratio both directions: unwrap 1, expect exactly 1000 back.
#   3. Edge cases: wrap 999 (must revert), wrap 1500 (see DESIGN QUESTION 1),
#      unwrap more than you hold (must revert).
#   4. Confirm every failure reverts with its message — no silent failures.
# Real wrappers also emit events for every state change and often include
# an admin function for emergencies; consider both for your variant.
