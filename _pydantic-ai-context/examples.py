# Hello World Example
from pydantic_ai import Agent

def hello_world_example():
    agent = Agent(  
        'gemini-1.5-flash',
        system_prompt='Be concise, reply with one sentence.',  
    )

    result = agent.run_sync('Where does "hello world" come from?')  
    print(result.data)
    """
    The first known use of "hello, world" was in a 1974 textbook about the C programming language.
    """

# Bank Support Example
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Stub class for example purposes
class DatabaseConn:
    """Stub class representing a database connection. Implementation not included."""
    async def customer_name(self, id: int) -> str:
        """Stub method that would return customer name in real implementation."""
        raise NotImplementedError("This is a stub class for example purposes")
    
    async def customer_balance(self, id: int, include_pending: bool) -> float:
        """Stub method that would return customer balance in real implementation."""
        raise NotImplementedError("This is a stub class for example purposes")

@dataclass
class SupportDependencies:  
    customer_id: int
    db: DatabaseConn

class SupportResult(BaseModel):  
    support_advice: str = Field(description='Advice returned to the customer')
    block_card: bool = Field(description="Whether to block the customer's card")
    risk: int = Field(description='Risk level of query', ge=0, le=10)

support_agent = Agent(  
    'openai:gpt-4o',  
    deps_type=SupportDependencies,
    result_type=SupportResult,  
    system_prompt=(  
        'You are a support agent in our bank, give the '
        'customer support and judge the risk level of their query.'
    ),
)

@support_agent.system_prompt  
async def add_customer_name(ctx: RunContext[SupportDependencies]) -> str:
    customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
    return f"The customer's name is {customer_name!r}"

@support_agent.tool  
async def customer_balance(
    ctx: RunContext[SupportDependencies], include_pending: bool
) -> float:
    """Returns the customer's current account balance."""  
    return await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
        include_pending=include_pending,
    )

async def main():
    # Note: This example won't run as-is since DatabaseConn is just a stub
    deps = SupportDependencies(customer_id=123, db=DatabaseConn())
    result = await support_agent.run('What is my balance?', deps=deps)  
    print(result.data)  
    """
    support_advice='Hello John, your current account balance, including pending transactions, is $123.45.' block_card=False risk=1
    """

    result = await support_agent.run('I just lost my card!', deps=deps)
    print(result.data)
    """
    support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to prevent unauthorized transactions." block_card=True risk=8
    """

# Logfire Integration Example
def setup_logfire():
    import logfire
    logfire.configure()  
    logfire.instrument_asyncpg()