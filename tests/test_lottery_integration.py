from brownie import network
import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONNEMENTS,
    fund_with_link,
    get_account,
)
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONNEMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # ideally add a little to the getEntranceFee value
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # ici on va juste attendre la réponse du node chainlink :
    time.sleep(180)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
