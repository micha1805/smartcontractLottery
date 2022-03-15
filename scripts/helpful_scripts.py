from brownie import (
    network,
    accounts,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONNEMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):

    # Si on passe un index : on utilisera un des comptes de ganache
    # Si on pass un id on utilisera un des comptes enregistrés dans brownie
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONNEMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mocks = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config if defined,
    otherwise it will deploy a mock version of that contract and return
    that mock contract.

        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract : the most recently deployed version of this contract
    """

    # the contract_name variable needs to match a key of the dictionary contract_to_mocks
    contract_type = contract_to_mocks[contract_name]

    # development context :
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONNEMENTS:
        # verifier si ce contrat est déjà déployé
        if len(contract_type) <= 0:  # exemple : MockV3Aggregator.length <= 0
            deploy_mocks()
        contract = contract_type[-1]
    # live context :
    else:
        # exemple : config["networks"][mainnet-fork-dev][eth_usd_price_feed]
        contract_address = config["networks"][network.show_active()][contract_name]
        # we need the address and the abi of the contract
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # exemple : contract_type = MockV3Aggregator
        # on aurait donc ceci :
        # contract = Contract.from_abi(
        #     MockV3Aggregator._name, contract_address, MockV3Aggregator.abi
        # )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks deployed!")


# For the following function the amount is 0.1 by defaut
# so 100_000_000_000_000_000 in 18 decimals Solidity representation
def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
