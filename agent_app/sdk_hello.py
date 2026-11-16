"""Lab 5: Claude Agent SDK로 만든 최소 고객 지원 에이전트.

하네스 요소
- 도구: get_order(조회), request_refund(변경). 위험도에 따라 도구를 분리했다.
- 권한: get_order만 자동 허용. request_refund는 can_use_tool 콜백에서 사람 승인을 받는다.
- 폭주 방지: max_turns, max_budget_usd.
- 역할 경계: 시스템 프롬프트.

실행 (저장소 루트에서):
    pip install -r requirements-agent.txt
    python scripts/seed.py
    set ANTHROPIC_API_KEY=...        (macOS/Linux: export ANTHROPIC_API_KEY=...)
    python -m agent_app.sdk_hello "주문 9번 환불해 주세요"

SDK API는 버전에 따라 바뀔 수 있다. 오류가 나면 공식 SDK 레퍼런스와 대조할 것.
"""

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    TextBlock,
    create_sdk_mcp_server,
    tool,
)

from app.services import order_service

REFUND_LOG: list[int] = []


def text(message: str) -> dict:
    return {"content": [{"type": "text", "text": message}]}


@tool("get_order", "주문 번호로 주문 상태와 금액(원)을 조회한다.", {"order_id": int})
async def get_order(args: dict) -> dict:
    order = order_service.get_order(int(args["order_id"]))
    if order is None:
        return text(f"주문 {args['order_id']}을(를) 찾을 수 없다. 주문 번호를 다시 확인하라.")
    return text(f"주문 {order.id}: 상태 {order.status}, 금액 {order.amount_krw:,}원")


@tool(
    "request_refund",
    "결제 완료(PAID) 주문의 환불을 요청한다. 사람 승인이 필요하다.",
    {"order_id": int},
)
async def request_refund(args: dict) -> dict:
    order = order_service.get_order(int(args["order_id"]))
    if order is None or order.status != "PAID":
        return text("환불 불가: PAID 상태인 주문만 환불할 수 있다.")
    REFUND_LOG.append(order.id)
    return text(f"주문 {order.id} 환불 요청 접수 ({order.amount_krw:,}원).")


async def approve(
    tool_name: str, tool_input: dict, context
) -> PermissionResultAllow | PermissionResultDeny:
    """allowed_tools에 없는 도구가 호출되면 여기로 온다. 위험 작업에 사람 승인을 붙이는 지점."""
    if tool_name.endswith("request_refund"):
        answer = input(f"\n[승인 요청] 주문 {tool_input.get('order_id')} 환불을 허용할까요? (y/N) ")
        if answer.strip().lower() == "y":
            return PermissionResultAllow()
        return PermissionResultDeny(
            message="담당자가 환불을 거절했다. 고객에게 상담원 연결을 안내하라."
        )
    return PermissionResultDeny(message=f"{tool_name}은(는) 이 에이전트에 허용되지 않은 도구다.")


shop = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[get_order, request_refund])

options = ClaudeAgentOptions(
    system_prompt=(
        "너는 Order Service의 고객 지원 에이전트다. 반드시 도구로 확인한 사실만 답한다. "
        "주문 정보는 get_order로 조회하고, 환불은 request_refund로만 요청한다. "
        "금액은 원 단위로 표기한다. 모르는 것은 추측하지 말고 상담원 연결을 안내한다."
    ),
    mcp_servers={"shop": shop},
    allowed_tools=["mcp__shop__get_order"],
    can_use_tool=approve,
    max_turns=8,
    max_budget_usd=0.5,
)


async def main(question: str) -> None:
    async with ClaudeSDKClient(options=options) as client:
        await client.query(question)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
    if REFUND_LOG:
        print(f"\n[감사 로그] 환불 요청된 주문: {REFUND_LOG}")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "주문 17번은 지금 어떤 상태인가요?"))
