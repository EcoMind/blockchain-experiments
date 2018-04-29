import json
import hashlib

def hash_function(k):
    """Hashes our transaction."""
    if type(k) is not str:
        k = json.dumps(k, sort_keys=True)

    return hashlib.sha256(k.encode("utf-8")).hexdigest()

def update_state(transaction, state):
    state = state.copy()

    for key in transaction:
        if key in state.keys():
            state[key] += transaction[key]
        else:
            state[key] = transaction[key]

    return state



def valid_transaction(transaction, state):
    """A valid transaction must sum to 0."""
    if sum(transaction.values()) is not 0:
        return False

    for key in transaction.keys():
        if key in state.keys():
            account_balance = state[key]
        else:
            account_balance = 0

        if account_balance + transaction[key] < 0:
            return False

    return True

def make_block(transactions, chain):
    """Make a block to go into the chain."""
    parent_hash = chain[-1]['hash']
    block_number = chain[-1]['contents']['block_number'] + 1

    block_contents = {
        'block_number': block_number,
        'parent_hash': parent_hash,
        'transaction_count': block_number + 1,
        'transaction': transactions
    }

    return {'hash': hash_function(block_contents), 'contents': block_contents}

def check_block_hash(block):
    expected_hash = hash_function(block['contents'])

    if block['hash'] != expected_hash:
        raise ValueError("Unexpected hash {}, expecting {}".format(block['hash'], expected_hash))

    return

def check_block_validity(block, parent, state):
    parent_number = parent['contents']['block_number']
    parent_hash = parent['hash']
    block_number = block['contents']['block_number']

    for transaction in block['contents']['transaction']:
        if valid_transaction(transaction, state):
            state = update_state(transaction, state)
        else:
            raise

    check_block_hash(block)  # Check hash integrity

    if block_number is not parent_number + 1:
        raise

    if block['contents']['parent_hash'] is not parent_hash:
        raise

    return state


def check_chain(chain):
    """Check the chain is valid."""
    if type(chain) is str:
        try:
            chain = json.loads(chain)
            assert (type(chain) == list)
        except ValueError:
            # String passed in was not valid JSON
            return False
    elif type(chain) is not list:
        return False

    state = {}

    for transaction in chain[0]['contents']['transaction']:
        state = update_state(transaction, state)

    check_block_hash(chain[0])
    parent = chain[0]

    for block in chain[1:]:
        state = check_block_validity(block, parent, state)
        parent = block

    return state

def add_transaction_to_chain(transaction, state, chain):
    if valid_transaction(transaction, state):
        state = update_state(transaction, state)
    else:
        raise Exception('Invalid transaction.')

    my_block = make_block(state, chain)
    chain.append(my_block)

    for transaction in chain:
        check_chain(transaction)

    return state, chain



def transfer(chain_state, block_chain, from_coins, to_coins, amount):
    print ("BEFORE: State {} Chain {}".format(chain_state, block_chain))
    # print( "BEFORE: Chain valid: {}".format(check_chain(block_chain)))
    chain_state, block_chain = add_transaction_to_chain(transaction={from_coins: -amount, to_coins: amount}, state=chain_state, chain=block_chain)
    # print( "AFTER: Chain valid: {}".format(check_chain(block_chain)))
    print ("AFTER: State {} Chain {}".format(chain_state, block_chain))
    return chain_state, block_chain

def firstTry():
    contents = {
            'block_number': 0,
            'parent_hash': None,
            'transaction_count': 1,
            'transaction': [{'Tom': 10}]
        }
    genesis_block = {
        'hash': hash_function(contents),
        'contents': contents,
    }

    block_chain = [genesis_block]
    chain_state = {'Tom': 10}

    chain_state, block_chain = transfer(chain_state, block_chain, 'Tom', 'Medium', 1)
    chain_state, block_chain = transfer(chain_state, block_chain, 'Tom', 'Sam', 3)


firstTry()
