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
        cairo_path = ["../../../../skyro-runtime"],
        constructor_calldata=[1,2,1,0]
    )

    result = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("viewEx"),
        calldata=[1],
        caller_address = 0,
        max_fee = 0
    )

    assert result.call_info.retdata == [2]

    result = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("writeEx"),
        calldata=[1,2],
        caller_address = 0,
        max_fee = 0
    )

    result = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("viewEx"),
        calldata=[1],
        caller_address = 0,
        max_fee = 0
    )

    result2 = await starknet.state.invoke_raw(
        contract_address=contract.contract_address,
        selector=get_selector_from_name("recEx"),
        calldata=[2,1,3],
        caller_address = 0,
        max_fee = 0
    )

    assert result.call_info.retdata == [10]
    assert result2.call_info.retdata == [1, 3, 1]
