import os
import pytest

from starkware.starknet.testing.starknet import Starknet
from starkware.starknet.public.abi import get_selector_from_name

# The path to the contract source code.
CONTRACT_FILE = os.path.join(
    os.path.dirname(__file__), "build/exec/Main.cairo")


@pytest.mark.asyncio
async def test_view():
    starknet = await Starknet.empty()

    contract = await starknet.deploy(
        source=CONTRACT_FILE,
        constructor_calldata=[]
    )

    result = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("writeEx"),
        calldata=[42],
        caller_address = 0,
        max_fee = 0
    )
 
    result = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("viewEx"),
        calldata=[],
        caller_address = 0,
        max_fee = 0
    )

    print(result.call_info.retdata)
 
    assert result.call_info.retdata == [42]