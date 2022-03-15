from brownie import Lottery, accounts, network, config
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    # account = get_account(id="freecodecamp-account")
    account = get_account()

    # check the constructor to get all the needed parameters
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # verify is set to default = False
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery !")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # just add a little something to be sure it's above entrance fee
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    # ici il y a une différence car il FAUT attendre que le node chainlink réponde et fasse
    #  la transaction, il est donc impératif d'attendre au moins quelques blocs pour que la
    # transaction soit effectuée par le node chainlink et enregistrée dans la blockchain
    ending_transaction.wait(1)
    # on attend 180 secondes, ce qui doit être suffisant pour que le transaction soit effectuée
    # dans la vidéo c'est 60 secondes, mais ça n'est pas assez :
    # time.sleep(60)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
