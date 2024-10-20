from brownie import LayerZeroMessaging, LayerZeroEndpointMock, accounts

# Define your fixture
@pytest.fixture
def layer_zero_messaging():
    # Deploy the mock LayerZero endpoint
    endpoint = LayerZeroEndpointMock.deploy({'from': accounts[0]})
    # Deploy the LayerZeroMessaging contract
    contract = LayerZeroMessaging.deploy(endpoint.address, {'from': accounts[0]})
    return contract

# Define your test function
def test_initiate_transfer(layer_zero_messaging):
    user = accounts[1]
    recipient = accounts[2]
    dest_chain_id = 101
    max_gas_fee = "0.1 ether"

    # Whitelist the destination chain
    layer_zero_messaging.whitelistChain(dest_chain_id, {'from': accounts[0]})

    # Send some gas fee to the user
    accounts[0].transfer(user, "1 ether")

    # Initiate transfer
    tx = layer_zero_messaging.initiateTransfer(dest_chain_id, recipient, "ipfs://example-uri", max_gas_fee, {'from': user, 'value': max_gas_fee})

    # Check that TransferInitiated event was emitted
    assert len(tx.events) > 0
    assert tx.events['TransferInitiated']['to'] == recipient
