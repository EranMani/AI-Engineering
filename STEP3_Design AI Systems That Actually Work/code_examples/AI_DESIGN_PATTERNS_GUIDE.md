# AI Design Patterns: A Comprehensive Guide for Junior Engineers

> **Author's Note**: This guide is written by a senior AI engineer with extensive experience building production AI systems. Each pattern is explained with strict technical precision, real-world scenarios, and practical implementation details. Master these patterns, and you'll be equipped to build robust, scalable AI applications.

---

## Table of Contents

1. [Introduction: Why Design Patterns Matter in AI](#introduction)
2. [Core Routing & Classification Patterns](#core-routing--classification-patterns)
   - [Router Pattern](#1-router-pattern-traffic-controller)
   - [Strategy Pattern](#2-strategy-pattern-vip-pass)
3. [Execution Patterns](#execution-patterns)
   - [Parallelization Pattern](#3-parallelization-pattern-the-pit-crew)
   - [Chain of Responsibility Pattern](#4-chain-of-responsibility-pattern-the-assembly-line)
   - [Orchestrator-Worker Pattern](#5-orchestrator-worker-pattern-the-project-plan)
4. [Quality & Refinement Patterns](#quality--refinement-patterns)
   - [Prompt Chaining Pattern](#6-prompt-chaining-pattern-the-thread)
   - [Evaluator-Optimizer Pattern](#7-evaluator-optimizer-pattern-the-loop)
5. [Architecture Patterns](#architecture-patterns)
   - [Facade Pattern](#8-facade-pattern-the-manager)
6. [Memory & State Management Patterns](#memory--state-management-patterns)
   - [Chat History Pattern](#9-chat-history-pattern-conversational-memory)
   - [Persistent Memory Pattern](#10-persistent-memory-pattern-state-persistence)
7. [Industry-Standard Advanced Patterns](#industry-standard-advanced-patterns)
   - [RAG Pattern](#11-rag-pattern-retrieval-augmented-generation)
   - [ReAct Pattern](#12-react-pattern-reasoning-acting)
   - [Self-Consistency Pattern](#13-self-consistency-pattern-ensemble-voting)
8. [Pattern Selection Guide](#pattern-selection-guide)
9. [Common Anti-Patterns to Avoid](#common-anti-patterns-to-avoid)

---

## Introduction: Why Design Patterns Matter in AI {#introduction}

### The Problem with Naive AI Systems

Most junior engineers start by building AI systems like this:

```python
# ❌ BAD: The "God Prompt" Anti-Pattern
response = agent.run("You are a customer support agent. Handle refunds, 
                      answer technical questions, process orders, 
                      manage accounts, and provide product recommendations.")
```

**Why this fails:**
- **Token Explosion**: One massive prompt consumes excessive tokens
- **Confusion**: The model tries to be everything at once, leading to poor performance
- **No Specialization**: Can't optimize for specific tasks
- **Unmaintainable**: Changes to one feature affect all features
- **No Quality Gates**: No way to ensure output quality

### The Solution: Design Patterns

Design patterns provide **proven architectural solutions** to common AI system problems. They enable:

1. **Modularity**: Each component has a single responsibility
2. **Performance**: Optimized for speed and token efficiency
3. **Maintainability**: Easy to update and extend
4. **Reliability**: Built-in quality checks and error handling
5. **Scalability**: Patterns that work at small and large scales

### When to Use Patterns

- **Router**: When you need to classify intent and route to specialists
- **Parallelization**: When tasks are independent and can run simultaneously
- **Chain of Responsibility**: When tasks must execute in strict sequence
- **Strategy**: When behavior must change based on user context (tier, role, permissions)
- **Facade**: When you want to hide complexity behind a simple interface
- **Prompt Chaining**: When you need iterative refinement of output
- **Evaluator-Optimizer**: When output quality must meet strict thresholds
- **Orchestrator-Worker**: When tasks are dynamic and require runtime planning

---

## Core Routing & Classification Patterns

### 1. Router Pattern (Traffic Controller) 🚦

#### **Definition**

The Router Pattern classifies user intent and directs requests to specialized agents, each optimized for a specific domain.

#### **Why It Exists**

**Problem**: A single "omniscient" agent trying to handle all tasks performs poorly because:
- The prompt becomes bloated with conflicting instructions
- The model can't specialize in any domain
- Token costs explode with unnecessary context
- Response quality degrades as the prompt grows

**Solution**: Create a lightweight classifier that routes to domain-specific agents.

#### **Real-World Scenarios**

##### Scenario 1: Customer Support System
**Company**: E-commerce platform (Amazon, Shopify)

**Problem**: Support tickets arrive covering billing, technical issues, product questions, and returns.

**Solution**:
```
User: "My internet is down and I can't connect to the VPN"
  ↓
Router Agent (classifies intent)
  ↓
Category: TECHNICAL
  ↓
Technical Support Agent (specialized in network issues)
```

**Impact**: 
- 40% reduction in resolution time
- 60% reduction in token costs
- 85% customer satisfaction increase

##### Scenario 2: Healthcare Triage System
**Company**: Telemedicine platform

**Problem**: Patients submit queries ranging from appointment scheduling to emergency symptoms.

**Solution**:
```
Patient: "I have chest pain and shortness of breath"
  ↓
Router Agent
  ↓
Category: URGENT_MEDICAL
  ↓
Emergency Triage Agent → Immediate escalation
```

**Impact**: 
- Life-threatening cases routed immediately
- Non-urgent cases handled efficiently
- Compliance with medical protocols

##### Scenario 3: Legal Document Processing
**Company**: Legal tech platform

**Problem**: Documents arrive in various formats: contracts, NDAs, patents, litigation documents.

**Solution**:
```
Document: [Uploaded PDF]
  ↓
Router Agent (analyzes document structure and content)
  ↓
Category: CONTRACT
  ↓
Contract Analysis Agent (specialized in contract terms)
```

#### **Implementation Details**

**Key Components**:
1. **Classification Model**: Lightweight, fast, structured output (Enum-based)
2. **Routing Logic**: Pattern matching or conditional logic
3. **Specialized Agents**: Domain-specific agents with focused prompts

**Code Structure**:
```python
# 1. Define categories using Enum (type-safe)
class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SALES = "sales"
    OTHER = "other"

# 2. Router Agent (lightweight classifier)
router_agent = Agent(
    model="gpt-4o-mini",  # Fast, cheap model for classification
    system_prompt="You are a help desk router. Classify the user's issue.",
    output_type=UserTicket  # Structured output ensures reliability
)

# 3. Route to specialized agents
match ticket_category:
    case TicketCategory.TECHNICAL:
        technical_agent.run(user_query)
    case TicketCategory.BILLING:
        billing_agent.run(user_query)
```

**Best Practices**:
- Use **fast, cheap models** (gpt-4o-mini, claude-haiku) for routing
- Use **structured output** (Pydantic models) to ensure reliable classification
- Implement **fallback logic** for ambiguous cases
- **Cache** routing decisions when possible (same user, similar queries)

**Common Mistakes**:
- ❌ Using expensive models (GPT-4) for routing
- ❌ Routing based on keywords instead of semantic understanding
- ❌ Not handling edge cases (ambiguous queries)

---

### 2. Strategy Pattern (VIP Pass) 🎩

#### **Definition**

The Strategy Pattern dynamically selects agent behavior (tools, capabilities, prompts) based on user context such as subscription tier, role, or permissions.

#### **Why It Exists**

**Problem**: Different users need different capabilities:
- Free users shouldn't see premium features
- Admins need different tools than regular users
- Enterprise customers require different behavior than individual users

**Solution**: Create multiple agent configurations and select based on context.

#### **Real-World Scenarios**

##### Scenario 1: SaaS Platform Feature Gating
**Company**: Project management tool (Asana, Monday.com)

**Problem**: Free users request premium features (export, advanced analytics, API access).

**Solution**:
```python
# Free User
user = User(tier=UserTier.FREE)
agent = get_support_agent(user)  # Returns agent with limited tools
# Tools: [search_faq, view_documentation]
# Cannot: process_refund, export_data, access_api

# Premium User
user = User(tier=UserTier.PREMIUM)
agent = get_support_agent(user)  # Returns agent with full tools
# Tools: [search_faq, process_refund, export_data, access_api]
```

**Impact**:
- Prevents unauthorized feature access
- Reduces support tickets from free users requesting premium features
- Clear upgrade path demonstrated through tool availability

##### Scenario 2: Enterprise Security Context
**Company**: Internal tooling platform

**Problem**: Different roles need different permissions:
- Developers: Can deploy, view logs, restart services
- QA: Can view logs, run tests, but not deploy
- Observers: Can only view dashboards

**Solution**:
```python
class UserRole(str, Enum):
    DEVELOPER = "developer"
    QA = "qa"
    OBSERVER = "observer"

def get_agent_for_role(role: UserRole) -> Agent:
    match role:
        case UserRole.DEVELOPER:
            return Agent(tools=[deploy, view_logs, restart_service])
        case UserRole.QA:
            return Agent(tools=[view_logs, run_tests])
        case UserRole.OBSERVER:
            return Agent(tools=[view_dashboards])
```

##### Scenario 3: Multi-Tenant AI System
**Company**: White-label AI platform

**Problem**: Each customer (tenant) has different:
- Brand voice
- Allowed actions
- Data access rules
- Model preferences

**Solution**:
```python
def get_tenant_agent(tenant_id: str) -> Agent:
    tenant_config = load_tenant_config(tenant_id)
    return Agent(
        model=tenant_config.preferred_model,
        system_prompt=tenant_config.brand_voice,
        tools=tenant_config.allowed_tools,
        deps_type=tenant_config.security_context
    )
```

#### **Implementation Details**

**Key Components**:
1. **Context Object**: User, tenant, or role information
2. **Strategy Selection**: Function that returns appropriate agent
3. **Agent Variants**: Multiple agent configurations

**Code Structure**:
```python
# 1. Define context
class User(BaseModel):
    name: str
    tier: UserTier

# 2. Create agent variants
free_agent = Agent(
    tools=[search_faq],  # Limited tools
    system_prompt="You are Basic Support..."
)

premium_agent = Agent(
    tools=[search_faq, process_refund],  # Full tools
    system_prompt="You are Premium Concierge..."
)

# 3. Strategy selector
def get_support_agent(user: User) -> Agent:
    if user.tier == UserTier.FREE:
        return free_agent
    elif user.tier == UserTier.PREMIUM:
        return premium_agent
```

**Best Practices**:
- **Inject context** via `deps_type` for runtime behavior modification
- **Validate permissions** before tool execution
- **Log** which strategy was selected for auditing
- **Cache** agent instances when possible (same user, same session)

**Common Mistakes**:
- ❌ Hardcoding permissions in prompts instead of tool availability
- ❌ Not validating permissions at runtime
- ❌ Exposing tool names to unauthorized users in error messages

---

## Execution Patterns

### 3. Parallelization Pattern (The Pit Crew) 🏎️

#### **Definition**

The Parallelization Pattern executes multiple independent tasks simultaneously using asynchronous operations, dramatically reducing total execution time.

#### **Why It Exists**

**Problem**: Sequential execution wastes time when tasks are independent:
```python
# ❌ BAD: Sequential (slow)
security_review = await review_security(code)      # 3 seconds
performance_review = await review_performance(code) # 3 seconds
style_review = await review_style(code)            # 3 seconds
# Total: 9 seconds
```

**Solution**: Execute all tasks concurrently:
```python
# ✅ GOOD: Parallel (fast)
reviews = await asyncio.gather(
    review_security(code),
    review_performance(code),
    review_style(code)
)
# Total: ~3 seconds (time of slowest task)
```

#### **Real-World Scenarios**

##### Scenario 1: Code Review System
**Company**: GitHub Copilot, CodeRabbit

**Problem**: Code reviews need to check multiple aspects: security, performance, style, documentation, test coverage.

**Solution**:
```python
async def review_code(code: str):
    reviewers = [
        security_reviewer,
        performance_reviewer,
        style_reviewer,
        documentation_reviewer,
        test_coverage_reviewer
    ]
    
    # All reviews run simultaneously
    results = await asyncio.gather(*[r.run(code) for r in reviewers])
    return aggregate_reviews(results)
```

**Impact**:
- **5x speedup**: 15 seconds → 3 seconds
- **Better coverage**: All aspects reviewed without time pressure
- **User experience**: Near-instant feedback

##### Scenario 2: Multi-Source Data Aggregation
**Company**: Financial data platform

**Problem**: Need to fetch data from multiple APIs: stock prices, news, social sentiment, analyst reports.

**Solution**:
```python
async def get_market_intelligence(ticker: str):
    data_sources = await asyncio.gather(
        fetch_stock_price(ticker),
        fetch_news(ticker),
        fetch_social_sentiment(ticker),
        fetch_analyst_reports(ticker)
    )
    return combine_data(data_sources)
```

**Impact**:
- **4x faster** data aggregation
- **Real-time** market intelligence
- **Better decisions** from comprehensive data

##### Scenario 3: Content Moderation Pipeline
**Company**: Social media platform

**Problem**: User posts must be checked for: toxicity, spam, copyright violations, NSFW content.

**Solution**:
```python
async def moderate_content(post: str, image: bytes):
    checks = await asyncio.gather(
        check_toxicity(post),
        check_spam(post),
        check_copyright(image),
        check_nsfw(image)
    )
    return all(checks)  # All must pass
```

#### **Implementation Details**

**Key Components**:
1. **Independent Tasks**: Tasks that don't depend on each other
2. **Async Functions**: All tasks must be async
3. **Gather**: `asyncio.gather()` to execute concurrently

**Code Structure**:
```python
# 1. Create specialized agents
security_reviewer = Agent(
    system_prompt="You are a security expert...",
    output_type=SecurityReview
)

performance_reviewer = Agent(
    system_prompt="You are a performance expert...",
    output_type=PerformanceReview
)

# 2. Execute in parallel
async def review_code(code: str):
    tasks = [
        security_reviewer.run(code),
        performance_reviewer.run(code),
        style_reviewer.run(code)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

**Best Practices**:
- **Verify independence**: Tasks must not depend on each other
- **Handle errors**: Use `return_exceptions=True` in `gather()` to handle partial failures
- **Set timeouts**: Prevent hanging tasks with `asyncio.wait_for()`
- **Limit concurrency**: Use semaphores to prevent overwhelming APIs

**Common Mistakes**:
- ❌ Parallelizing dependent tasks (causes race conditions)
- ❌ Not handling partial failures
- ❌ Unbounded concurrency (overwhelming APIs)

**When NOT to Use**:
- Tasks have dependencies (use Chain of Responsibility instead)
- Rate limits prevent parallel execution
- Tasks are CPU-bound (Python's GIL limits benefits)

---

### 4. Chain of Responsibility Pattern (The Assembly Line) ⛓️

#### **Definition**

The Chain of Responsibility Pattern processes data through a sequence of agents where each step depends on the output of the previous step.

#### **Why It Exists**

**Problem**: Some tasks require sequential processing:
- You can't write a blog post until you have an itinerary
- You can't create an itinerary until you have locations
- You can't find locations until you know the destination

**Solution**: Chain agents together, passing output from one to the next.

#### **Real-World Scenarios**

##### Scenario 1: Content Creation Pipeline
**Company**: Content marketing platform

**Problem**: Creating a travel blog post requires: research → planning → writing → SEO optimization.

**Solution**:
```python
# Step 1: Research
scout_result = await scout_agent.run("Find hidden gems in Paris")
# Output: ["Café des Deux Moulins", "Shakespeare and Company", "Montmartre Vineyard"]

# Step 2: Plan itinerary (depends on Step 1)
itinerary_result = await planner_agent.run(
    f"Create itinerary for: {scout_result.gems}"
)
# Output: ["Morning: Café", "Afternoon: Bookstore", "Evening: Vineyard"]

# Step 3: Write blog post (depends on Step 2)
blog_result = await writer_agent.run(
    f"Write blog post about: {itinerary_result.itinerary}"
)
```

**Impact**:
- **High-quality content**: Each step builds on previous expertise
- **Consistent structure**: Enforced workflow ensures completeness
- **Maintainable**: Each agent can be improved independently

##### Scenario 2: Document Processing Pipeline
**Company**: Legal tech platform

**Problem**: Processing legal documents requires: extraction → classification → analysis → summarization.

**Solution**:
```python
# Step 1: Extract text
extracted_text = await extraction_agent.run(document)

# Step 2: Classify document type
document_type = await classifier_agent.run(extracted_text)

# Step 3: Analyze based on type
analysis = await specialized_analyst_agent.run(
    text=extracted_text,
    document_type=document_type
)

# Step 4: Summarize findings
summary = await summarizer_agent.run(analysis)
```

##### Scenario 3: E-commerce Order Processing
**Company**: Online marketplace

**Problem**: Order fulfillment requires: validation → payment → inventory check → shipping → notification.

**Solution**:
```python
# Sequential pipeline (each step depends on previous)
order_validated = await validate_order(order)
payment_processed = await process_payment(order_validated)
inventory_reserved = await reserve_inventory(payment_processed)
shipping_label = await create_shipping_label(inventory_reserved)
await send_notification(shipping_label)
```

#### **Implementation Details**

**Key Components**:
1. **Sequential Agents**: Each agent specializes in one step
2. **Data Flow**: Output of Agent A becomes input to Agent B
3. **Error Handling**: If one step fails, the chain stops

**Code Structure**:
```python
# 1. Define output models for each step
class ScoutResult(BaseModel):
    gems: list[str]

class PlannerResult(BaseModel):
    itinerary: list[str]

class WriterResult(BaseModel):
    blog_post: str

# 2. Create specialized agents
scout_agent = Agent(output_type=ScoutResult, ...)
planner_agent = Agent(output_type=PlannerResult, ...)
writer_agent = Agent(output_type=WriterResult, ...)

# 3. Chain execution
async def create_blog_post(city: str):
    # Step 1
    scout_result = await scout_agent.run(f"Find gems in {city}")
    
    # Step 2 (uses Step 1 output)
    planner_result = await planner_agent.run(
        f"Plan itinerary: {scout_result.gems}"
    )
    
    # Step 3 (uses Step 2 output)
    writer_result = await writer_agent.run(
        f"Write blog: {planner_result.itinerary}"
    )
    
    return writer_result.blog_post
```

**Best Practices**:
- **Validate outputs**: Ensure each step produces valid data before proceeding
- **Handle failures**: Implement retry logic for transient failures
- **Log intermediate results**: Debugging is easier with step-by-step logs
- **Consider timeouts**: Long chains can timeout; set appropriate limits

**Common Mistakes**:
- ❌ Not validating intermediate outputs
- ❌ Continuing chain after failures
- ❌ Not passing enough context between steps

**When to Use vs. Parallelization**:
- **Chain of Responsibility**: Tasks depend on each other (A → B → C)
- **Parallelization**: Tasks are independent (A, B, C run simultaneously)

---

### 5. Orchestrator-Worker Pattern (The Project Plan) 🏗️

#### **Definition**

The Orchestrator-Worker Pattern uses a planning agent (orchestrator) to break down complex tasks into subtasks, then executes them using worker agents.

#### **Why It Exists**

**Problem**: Some tasks are too complex or dynamic to hardcode:
- "Build a login page" requires: database setup, API endpoints, frontend components
- The exact steps depend on the specific requirements
- Steps may vary based on context

**Solution**: Use an AI orchestrator to create a dynamic plan, then execute with workers.

#### **Real-World Scenarios**

##### Scenario 1: Software Development Assistant
**Company**: GitHub Copilot, Cursor AI

**Problem**: User requests complex features: "Add OAuth login with Google"

**Solution**:
```python
# Orchestrator breaks down the task
feature_request = "Add OAuth login with Google"
plan = await orchestrator_agent.run(feature_request)
# Output: TaskList([
#   Task("Setup OAuth credentials", "Configure Google OAuth in dashboard"),
#   Task("Create backend endpoint", "Implement /auth/google endpoint"),
#   Task("Create frontend component", "Build Google login button"),
#   Task("Handle callback", "Process OAuth callback and create session")
# ])

# Workers execute each task
for task in plan.tasks:
    result = await worker_agent.run(task)
    # Execute: Write code, run tests, etc.
```

**Impact**:
- **Handles complexity**: Breaks down any feature request
- **Adaptive**: Plan changes based on existing codebase
- **Maintainable**: Each task is isolated and testable

##### Scenario 2: Research Assistant
**Company**: Academic research platform

**Problem**: User requests: "Research the impact of AI on healthcare"

**Solution**:
```python
research_query = "Research the impact of AI on healthcare"
plan = await orchestrator_agent.run(research_query)
# Output: TaskList([
#   Task("Literature review", "Find recent papers on AI in healthcare"),
#   Task("Data analysis", "Analyze healthcare AI adoption statistics"),
#   Task("Expert interviews", "Summarize expert opinions"),
#   Task("Synthesis", "Combine findings into report")
# ])

for task in plan.tasks:
    result = await research_worker.run(task)
```

##### Scenario 3: Customer Onboarding Automation
**Company**: SaaS platform

**Problem**: Onboarding varies by customer type, industry, and requirements.

**Solution**:
```python
onboarding_request = "Onboard enterprise customer in healthcare"
plan = await orchestrator_agent.run(onboarding_request)
# Output: TaskList([
#   Task("Setup compliance", "Configure HIPAA compliance settings"),
#   Task("Create admin accounts", "Set up admin users"),
#   Task("Import data", "Migrate existing customer data"),
#   Task("Training", "Schedule training sessions")
# ])

for task in plan.tasks:
    await onboarding_worker.execute(task)
```

#### **Implementation Details**

**Key Components**:
1. **Orchestrator Agent**: Plans and breaks down tasks
2. **Task Model**: Structured representation of subtasks
3. **Worker Agents**: Execute individual tasks

**Code Structure**:
```python
# 1. Define task structure
class Task(BaseModel):
    task_id: int
    task_name: str
    task_description: str

class TaskList(BaseModel):
    tasks: list[Task]

# 2. Orchestrator (planner)
orchestrator_agent = Agent(
    system_prompt="You are a Tech Lead. Break down feature requests into tasks.",
    output_type=TaskList
)

# 3. Worker (executor)
worker_agent = Agent(
    system_prompt="You are a Senior Developer. Execute the given task.",
    output_type=CodeOutput
)

# 4. Execution loop
def execute_feature(request: str):
    # Plan
    plan = orchestrator_agent.run_sync(request)
    
    # Execute
    for task in plan.output.tasks:
        result = worker_agent.run_sync(task.task_description)
        # Execute code, update system, etc.
```

**Best Practices**:
- **Limit task count**: Prevent overly granular plans (e.g., max 5-10 tasks)
- **Validate plans**: Check that tasks are actionable and complete
- **Handle failures**: Retry failed tasks or replan
- **Track progress**: Log which tasks completed successfully

**Common Mistakes**:
- ❌ Not validating orchestrator output
- ❌ Infinite loops (orchestrator creates tasks that create more tasks)
- ❌ Not handling worker failures

**When to Use**:
- Tasks are **dynamic** and can't be hardcoded
- Tasks require **planning** based on context
- Tasks are **complex** and need decomposition

**When NOT to Use**:
- Tasks are **simple** and well-defined (use Chain of Responsibility)
- Tasks are **static** (hardcode the steps)
- Tasks require **real-time** execution (orchestration adds latency)

---

## Quality & Refinement Patterns

### 6. Prompt Chaining Pattern (The Thread) 🧵

#### **Definition**

The Prompt Chaining Pattern maintains a "stream of thought" by passing output from one prompt to the next, enabling iterative refinement of quality.

#### **Why It Exists**

**Problem**: Single-shot prompts often produce suboptimal results:
- Model forgets instructions mid-generation
- No self-correction mechanism
- Can't refine based on self-critique

**Solution**: Break generation into steps: Draft → Critique → Refine

#### **Real-World Scenarios**

##### Scenario 1: Email Writing Assistant
**Company**: Professional communication tool

**Problem**: User writes angry email: "Give me a refund NOW! Your product sucks!"

**Solution**:
```python
# Step 1: Draft
raw_input = "Give me a refund NOW! Your product sucks!"
draft = await draft_agent.run(raw_input)
# Output: Professional email structure

# Step 2: Critique
critique = await critique_agent.run(draft.body)
# Output: "Tone is too aggressive, lacks professionalism, score: 3/10"

# Step 3: Refine
final = await refine_agent.run(
    draft=draft.body,
    feedback=critique.feedback
)
# Output: Professional, polite refund request
```

**Impact**:
- **Professional output**: Transforms emotional input into business-appropriate communication
- **Self-correction**: Model critiques and improves its own work
- **Consistent quality**: Multi-step process ensures standards

##### Scenario 2: Code Generation with Review
**Company**: AI coding assistant

**Problem**: Generated code may have bugs, style issues, or missing edge cases.

**Solution**:
```python
# Step 1: Generate
code = await generator_agent.run("Write a function to calculate tax")

# Step 2: Review
review = await reviewer_agent.run(code)
# Output: "Missing error handling, no input validation, score: 5/10"

# Step 3: Improve
improved_code = await improver_agent.run(
    original=code,
    feedback=review.feedback
)
```

##### Scenario 3: Content Creation Pipeline
**Company**: Marketing content platform

**Problem**: First draft of blog post may lack SEO optimization, engaging tone, or clarity.

**Solution**:
```python
# Step 1: Draft
draft = await writer_agent.run("Write blog post about AI trends")

# Step 2: SEO Review
seo_feedback = await seo_agent.run(draft)

# Step 3: Engagement Review
engagement_feedback = await engagement_agent.run(draft)

# Step 4: Refine (combines all feedback)
final = await refine_agent.run(
    draft=draft,
    seo_feedback=seo_feedback,
    engagement_feedback=engagement_feedback
)
```

#### **Implementation Details**

**Key Components**:
1. **Same Agent, Different Prompts**: Reuse one agent with different prompts/output types
2. **Output Passing**: Previous output becomes input to next step
3. **Structured Feedback**: Use Pydantic models for critique structure

**Code Structure**:
```python
# 1. Define models for each step
class EmailDraft(BaseModel):
    subject: str
    body: str

class EmailCritique(BaseModel):
    score: int  # 1-10
    feedback: str
    suggestions: list[str]

class FinalEmail(BaseModel):
    subject: str
    body: str

# 2. Single agent, multiple uses
editor_agent = Agent(
    system_prompt="You are a professional editor."
)

# 3. Chain execution
def improve_email(raw_input: str):
    # Step 1: Draft
    draft = editor_agent.run_sync(
        f"Convert to email: {raw_input}",
        output_type=EmailDraft
    )
    
    # Step 2: Critique
    critique = editor_agent.run_sync(
        f"Critique this email: {draft.body}",
        output_type=EmailCritique
    )
    
    # Step 3: Refine
    final = editor_agent.run_sync(
        f"Improve this email: {draft.body}\nFeedback: {critique.feedback}",
        output_type=FinalEmail
    )
    
    return final
```

**Best Practices**:
- **Pass full context**: Include both original and critique in refinement step
- **Use structured output**: Pydantic models ensure consistent feedback format
- **Limit chain length**: 2-4 steps is optimal (diminishing returns after that)
- **Track improvements**: Log scores to measure refinement effectiveness

**Common Mistakes**:
- ❌ Not passing enough context between steps
- ❌ Using different agents (loses context)
- ❌ Chains that are too long (quality degrades)

**When to Use**:
- Output quality is **critical**
- Single-shot generation is **insufficient**
- You need **self-correction** mechanisms

---

### 7. Evaluator-Optimizer Pattern (The Loop) 🧐

#### **Definition**

The Evaluator-Optimizer Pattern guarantees quality by evaluating output, rejecting substandard results, and forcing retries until a threshold is met.

#### **Why It Exists**

**Problem**: LLMs are probabilistic; they sometimes produce low-quality output:
- Code with bugs
- Inaccurate information
- Poor writing quality
- Missing requirements

**Solution**: Add a quality gate that evaluates output and retries if below threshold.

#### **Real-World Scenarios**

##### Scenario 1: Code Generation with Testing
**Company**: AI coding assistant

**Problem**: Generated code may have bugs that only appear when tested.

**Solution**:
```python
MAX_RETRIES = 3
QUALITY_THRESHOLD = 8  # Score out of 10

while retries < MAX_RETRIES:
    # Generate
    code = await generator_agent.run("Write a function to calculate tax")
    
    # Evaluate (run tests, check style, etc.)
    evaluation = await evaluator_agent.run(code)
    # Output: score=6, feedback="Missing edge cases, no error handling"
    
    if evaluation.score >= QUALITY_THRESHOLD:
        return code  # ✅ Quality gate passed
    
    # Retry with feedback
    retries += 1
    # Next iteration uses feedback to improve
```

**Impact**:
- **Reliable code**: Only accepts code that passes quality checks
- **Self-improving**: Each retry incorporates feedback
- **Production-ready**: Meets quality standards before deployment

##### Scenario 2: Content Quality Assurance
**Company**: Content generation platform

**Problem**: Generated articles may lack depth, accuracy, or engagement.

**Solution**:
```python
while retries < MAX_RETRIES:
    article = await writer_agent.run("Write article about AI trends")
    
    evaluation = await evaluator_agent.run(article)
    # Checks: accuracy, depth, engagement, SEO
    
    if evaluation.score >= 8:
        publish(article)
        break
    
    # Retry with specific feedback
    retries += 1
```

##### Scenario 3: Data Extraction with Validation
**Company**: Document processing platform

**Problem**: Extracted data may be incomplete or inaccurate.

**Solution**:
```python
while retries < MAX_RETRIES:
    extracted_data = await extraction_agent.run(document)
    
    validation = await validator_agent.run(extracted_data)
    # Checks: completeness, format, accuracy
    
    if validation.score >= 9:  # High threshold for data
        return extracted_data
    
    retries += 1
```

#### **Implementation Details**

**Key Components**:
1. **Generator Agent**: Creates output
2. **Evaluator Agent**: Scores output quality
3. **Feedback Loop**: Retries with feedback until threshold met
4. **Retry Limit**: Prevents infinite loops

**Code Structure**:
```python
# 1. Define output and evaluation models
class Joke(BaseModel):
    setup: str
    punchline: str

class Evaluation(BaseModel):
    score: int  # 1-10
    feedback: str

# 2. Create agents
generator_agent = Agent(
    system_prompt="You are a comedian...",
    output_type=Joke
)

evaluator_agent = Agent(
    system_prompt="You are a harsh critic...",
    output_type=Evaluation
)

# 3. Loop until quality threshold
def generate_quality_joke():
    retries = 0
    MAX_RETRIES = 3
    THRESHOLD = 8
    feedback = ""
    
    while retries <= MAX_RETRIES:
        # Generate (with feedback if retry)
        if retries == 0:
            prompt = "Write a funny joke"
        else:
            prompt = f"Previous attempt: {previous_joke}\nFeedback: {feedback}\nImprove it."
        
        joke = generator_agent.run_sync(prompt)
        
        # Evaluate
        evaluation = evaluator_agent.run_sync(
            f"Rate this joke: {joke.setup} - {joke.punchline}"
        )
        
        # Quality gate
        if evaluation.score >= THRESHOLD:
            return joke
        
        # Prepare for retry
        retries += 1
        feedback = evaluation.feedback
        previous_joke = joke
    
    raise Exception("Max retries reached")
```

**Best Practices**:
- **Set realistic thresholds**: Too high = infinite retries, too low = poor quality
- **Limit retries**: Prevent infinite loops (typically 3-5 retries)
- **Incorporate feedback**: Each retry should use previous feedback
- **Log attempts**: Track success rates and common failure modes

**Common Mistakes**:
- ❌ Thresholds too high (never passes) or too low (poor quality)
- ❌ Not incorporating feedback in retries
- ❌ Infinite loops (no retry limit)
- ❌ Evaluating wrong aspects (e.g., checking code style when bugs are the issue)

**When to Use**:
- **Quality is critical**: Output must meet strict standards
- **Probabilistic failures**: LLMs sometimes produce poor output
- **Automated systems**: No human in the loop to catch errors

**When NOT to Use**:
- **Real-time systems**: Retries add latency
- **Creative tasks**: "Quality" is subjective
- **High success rate**: If 95%+ outputs are good, retries aren't worth the cost

---

## Architecture Patterns

### 8. Facade Pattern (The Manager) 💼

#### **Definition**

The Facade Pattern provides a simple, unified interface that hides the complexity of multiple specialized agents behind a single entry point.

#### **Why It Exists**

**Problem**: Users shouldn't need to know about internal complexity:
- User wants "Party Mode" but doesn't care about light agents, music agents, etc.
- User wants "Research Report" but doesn't need to know about data collection, analysis, writing agents

**Solution**: Create a manager agent that coordinates specialized agents via tools.

#### **Real-World Scenarios**

##### Scenario 1: Smart Home Assistant
**Company**: Amazon Alexa, Google Home

**Problem**: User says "Party Time!" but the system has separate agents for lights, music, temperature, etc.

**Solution**:
```python
# User-facing agent (Facade)
manager_agent = Agent(
    tools=[control_lights, control_music, control_temperature],
    system_prompt="You are a Smart Home Manager. Fulfill user requests."
)

# Internal agents (hidden complexity)
light_agent = Agent(...)  # User doesn't know this exists
music_agent = Agent(...)  # User doesn't know this exists

# Tools call internal agents
async def control_lights(action: str):
    return await light_agent.run(action)

async def control_music(genre: str):
    return await music_agent.run(genre)

# User only interacts with manager
result = await manager_agent.run("Party time! Turn on lights and play jazz")
```

**Impact**:
- **Simple UX**: One command does everything
- **Maintainable**: Internal agents can change without affecting users
- **Extensible**: Add new agents without changing user interface

##### Scenario 2: Research Assistant
**Company**: Academic research platform

**Problem**: User wants "Research Report on AI Ethics" but system has: data collection agent, analysis agent, writing agent, citation agent.

**Solution**:
```python
# Facade
research_manager = Agent(
    tools=[collect_data, analyze_data, write_report, add_citations],
    system_prompt="You are a Research Assistant. Create comprehensive reports."
)

# User only sees manager
report = await research_manager.run("Research AI ethics")
# Internally: collects data → analyzes → writes → adds citations
```

##### Scenario 3: Customer Support System
**Company**: Enterprise support platform

**Problem**: User has issue but system has: ticket router, technical specialist, billing specialist, escalation agent.

**Solution**:
```python
# Facade
support_manager = Agent(
    tools=[route_ticket, get_technical_help, process_refund, escalate],
    system_prompt="You are a Support Manager. Resolve customer issues."
)

# User only interacts with manager
resolution = await support_manager.run("My account is locked and I need a refund")
# Internally: routes → technical help → processes refund → escalates if needed
```

#### **Implementation Details**

**Key Components**:
1. **Manager Agent**: User-facing interface
2. **Tool Functions**: Bridge to internal agents
3. **Specialized Agents**: Hidden complexity

**Code Structure**:
```python
# 1. Internal agents (hidden from user)
light_agent = Agent(
    system_prompt="You control lights..."
)

music_agent = Agent(
    system_prompt="You control music..."
)

# 2. Tools that call internal agents (ASYNC REQUIRED)
async def control_lights(ctx: RunContext, action: str) -> str:
    result = await light_agent.run(f"Turn lights {action}")
    return result.output

async def control_music(ctx: RunContext, genre: str) -> str:
    result = await music_agent.run(f"Play {genre}")
    return result.output

# 3. Manager agent (user-facing facade)
manager_agent = Agent(
    tools=[control_lights, control_music],
    system_prompt="You are a Smart Home Manager..."
)

# 4. User only interacts with manager
result = await manager_agent.run("Party time!")
```

**Best Practices**:
- **Tools must be async**: When calling agents from tools, use `async def` and `await`
- **Hide complexity**: User shouldn't know about internal agents
- **Error handling**: Manager should handle failures gracefully
- **Logging**: Track which internal agents were called for debugging

**Common Mistakes**:
- ❌ Not using async in tools (causes blocking)
- ❌ Exposing internal agents to users
- ❌ Manager agent tries to do everything (defeats the purpose)

**When to Use**:
- **Complex systems**: Multiple agents working together
- **User experience**: Want simple interface
- **Maintainability**: Internal structure may change

**When NOT to Use**:
- **Simple systems**: One agent is sufficient
- **User needs control**: User wants to interact with specific agents
- **Performance critical**: Facade adds latency (extra agent call)

---

## Memory & State Management Patterns

### 9. Chat History Pattern (Conversational Memory) 💬

#### **Definition**

The Chat History Pattern maintains conversation context across multiple interactions by storing and passing message history to the agent.

#### **Why It Exists**

**Problem**: Without memory, each interaction is isolated:
```python
# ❌ BAD: No memory
agent.run("My name is John")
agent.run("What's my name?")  # Doesn't know!
```

**Solution**: Store message history and pass it to each agent call.

#### **Real-World Scenarios**

##### Scenario 1: Customer Support Chatbot
**Company**: E-commerce platform

**Problem**: Customer asks follow-up questions that reference previous messages.

**Solution**:
```python
history = []

# First message
response = agent.run("I want to return a product", message_history=history)
history += response.new_messages()  # Store conversation

# Follow-up (has context)
response = agent.run("What's the refund policy?", message_history=history)
# Agent knows: user wants to return a product, asking about refund policy
```

**Impact**:
- **Natural conversation**: Users can reference previous messages
- **Context awareness**: Agent remembers user preferences, history
- **Better UX**: Feels like talking to a human

##### Scenario 2: Personal Assistant
**Company**: Virtual assistant platform

**Problem**: User makes requests that build on previous context.

**Solution**:
```python
history = []

# User: "Set a reminder for tomorrow at 3pm"
response = agent.run(user_input, message_history=history)
history += response.new_messages()

# User: "Change it to 4pm"
response = agent.run(user_input, message_history=history)
# Agent knows: "it" refers to the reminder, change time to 4pm
```

##### Scenario 3: Code Review Assistant
**Company**: Development tool

**Problem**: Developer asks questions about code that was discussed earlier.

**Solution**:
```python
history = []

# Developer: "Review this function: def calculate_tax(...)"
response = agent.run(user_input, message_history=history)
history += response.new_messages()

# Developer: "How can I optimize it?"
response = agent.run(user_input, message_history=history)
# Agent knows: "it" refers to calculate_tax function
```

#### **Implementation Details**

**Key Components**:
1. **History Storage**: List of messages (typically outside agent)
2. **Message Passing**: Include history in each agent call
3. **History Updates**: Append new messages after each interaction

**Code Structure**:
```python
# 1. Initialize history (outside agent)
history = []

# 2. Agent (no special configuration needed)
chat_agent = Agent(
    system_prompt="You are a helpful assistant...",
    output_type=str
)

# 3. Conversation loop
def chat_loop():
    history = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        # Pass history
        response = chat_agent.run_sync(
            user_prompt=user_input,
            message_history=history
        )
        
        # Update history
        history += response.new_messages()
        
        print(f"Assistant: {response.output}")
```

**Best Practices**:
- **Store externally**: History should be outside the agent (database, session storage)
- **Token limits**: Truncate old messages if history exceeds token limits
- **User isolation**: Separate history per user/session
- **Summary**: For long conversations, summarize old messages instead of storing all

**Common Mistakes**:
- ❌ Not storing history between calls
- ❌ Storing history inside agent (loses it on restart)
- ❌ Not handling token limits (history too long)

**Token Management Strategies**:
1. **Sliding Window**: Keep only last N messages
2. **Summarization**: Summarize old messages, keep recent ones
3. **Token Counting**: Truncate when approaching limit

---

### 10. Persistent Memory Pattern (State Persistence) 💾

#### **Definition**

The Persistent Memory Pattern stores agent state (conversations, preferences, context) in a database or file system for long-term persistence across sessions.

#### **Why It Exists**

**Problem**: Chat history pattern only works within a session. When the system restarts or user returns later, context is lost.

**Solution**: Persist state to database/file system and load it when needed.

#### **Real-World Scenarios**

##### Scenario 1: Multi-Session Customer Support
**Company**: SaaS platform

**Problem**: Customer starts support chat, leaves, returns days later. System should remember previous conversation.

**Solution**:
```python
# Save conversation
def save_conversation(user_id: str, messages: list):
    with open(f"conversations/{user_id}.json", "w") as f:
        json.dump(messages, f)

# Load conversation
def load_conversation(user_id: str) -> list:
    if os.path.exists(f"conversations/{user_id}.json"):
        with open(f"conversations/{user_id}.json", "r") as f:
            return json.load(f)
    return []

# Usage
user_id = "user_123"
history = load_conversation(user_id)

response = agent.run(user_input, message_history=history)
history += response.new_messages()

save_conversation(user_id, history)  # Persist
```

**Impact**:
- **Continuity**: Conversations persist across sessions
- **User experience**: Feels like ongoing relationship
- **Context**: Agent remembers user preferences, history

##### Scenario 2: Personal AI Assistant
**Company**: Virtual assistant

**Problem**: User sets preferences, reminders, notes. These should persist.

**Solution**:
```python
# Store user state
user_state = {
    "preferences": {"language": "en", "timezone": "PST"},
    "reminders": [...],
    "notes": [...],
    "conversation_history": [...]
}

# Save to database
save_user_state(user_id, user_state)

# Load on session start
state = load_user_state(user_id)
agent = Agent(deps_type=UserState, ...)
response = agent.run(user_input, deps=state)
```

##### Scenario 3: Research Assistant with Project Memory
**Company**: Research platform

**Problem**: Research projects span multiple sessions. Agent should remember what was researched.

**Solution**:
```python
# Project state
project_state = {
    "project_id": "ai_ethics_research",
    "research_questions": [...],
    "findings": [...],
    "sources": [...],
    "conversation_history": [...]
}

# Persist project
save_project(project_state)

# Load when continuing research
project = load_project("ai_ethics_research")
agent.run("Continue research", deps=project)
```

#### **Implementation Details**

**Key Components**:
1. **Storage Backend**: Database, file system, or cloud storage
2. **Serialization**: Convert agent state to storable format (JSON, etc.)
3. **Loading Logic**: Retrieve and deserialize state when needed

**Code Structure**:
```python
import json
import os

# 1. Storage functions
def save_conversation(user_id: str, history: list):
    os.makedirs("conversations", exist_ok=True)
    with open(f"conversations/{user_id}.json", "w") as f:
        json.dump(history, f, default=str)  # Handle non-serializable types

def load_conversation(user_id: str) -> list:
    path = f"conversations/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

# 2. Agent usage
def chat_with_persistence(user_id: str, user_input: str):
    # Load history
    history = load_conversation(user_id)
    
    # Run agent
    response = agent.run_sync(
        user_prompt=user_input,
        message_history=history
    )
    
    # Update history
    history += response.new_messages()
    
    # Save
    save_conversation(user_id, history)
    
    return response.output
```

**Best Practices**:
- **Choose storage wisely**: JSON files for simple cases, database for production
- **Handle serialization**: Some types (datetimes, custom objects) need special handling
- **Backup**: Regularly backup persistent storage
- **Privacy**: Encrypt sensitive data (conversations, user info)
- **Cleanup**: Implement retention policies (delete old conversations)

**Common Mistakes**:
- ❌ Not handling serialization errors
- ❌ Storing sensitive data unencrypted
- ❌ No backup strategy
- ❌ Storing too much data (token limits still apply)

**Storage Options**:
1. **JSON Files**: Simple, good for development
2. **SQLite**: Lightweight database, good for small-scale production
3. **PostgreSQL/MongoDB**: For large-scale production
4. **Cloud Storage**: S3, Azure Blob for distributed systems

---

## Industry-Standard Advanced Patterns

### 11. RAG Pattern (Retrieval Augmented Generation) 🔍

#### **Definition**

The RAG Pattern enhances LLM responses by retrieving relevant information from a knowledge base (documents, database) and including it in the prompt context.

#### **Why It Exists**

**Problem**: LLMs have training cutoffs and limited context. They can't access:
- Recent information (after training cutoff)
- Private documents (company docs, user data)
- Real-time data (current prices, weather, etc.)

**Solution**: Retrieve relevant information and inject it into the prompt.

#### **Real-World Scenarios**

##### Scenario 1: Company Knowledge Base Assistant
**Company**: Enterprise internal tool

**Problem**: Employees ask questions about company policies, but LLM doesn't know internal docs.

**Solution**:
```python
# 1. User query
query = "What's our refund policy?"

# 2. Retrieve relevant documents
relevant_docs = vector_db.search(query, top_k=3)
# Returns: ["refund_policy.pdf", "customer_service_guide.pdf"]

# 3. Inject into prompt
context = "\n".join([load_document(doc) for doc in relevant_docs])

response = agent.run(
    f"Context: {context}\n\nUser Question: {query}"
)
```

**Impact**:
- **Accurate answers**: Based on actual company documents
- **Up-to-date**: Can update knowledge base without retraining model
- **Private data**: Uses internal documents securely

##### Scenario 2: Customer Support with Product Database
**Company**: E-commerce platform

**Problem**: Support agent needs product information, pricing, availability.

**Solution**:
```python
query = "Do you have iPhone 15 in stock?"

# Retrieve product info
product_info = product_db.search("iPhone 15")
inventory = inventory_db.get_stock("iPhone 15")

# Inject context
response = agent.run(
    f"Product Info: {product_info}\n"
    f"Inventory: {inventory}\n\n"
    f"User Question: {query}"
)
```

##### Scenario 3: Legal Document Assistant
**Company**: Legal tech platform

**Problem**: Lawyers need to search case law, statutes, precedents.

**Solution**:
```python
query = "What are the precedents for breach of contract?"

# Retrieve relevant cases
cases = legal_db.search(query, top_k=5)

# Inject context
response = agent.run(
    f"Relevant Cases:\n{cases}\n\n"
    f"Question: {query}"
)
```

#### **Implementation Details**

**Key Components**:
1. **Vector Database**: Stores document embeddings (Pinecone, Weaviate, Chroma)
2. **Embedding Model**: Converts text to vectors (OpenAI, Cohere)
3. **Retrieval Logic**: Search similar documents
4. **Context Injection**: Add retrieved docs to prompt

**Code Structure**:
```python
from pydantic_ai import Agent
import vector_db  # Hypothetical vector DB client

# 1. Setup vector database (one-time)
def index_documents(documents: list[str]):
    embeddings = embedding_model.encode(documents)
    vector_db.upsert(embeddings, documents)

# 2. RAG agent
rag_agent = Agent(
    system_prompt="You are a helpful assistant. Use the provided context to answer questions.",
    output_type=str
)

# 3. RAG function
def rag_query(user_query: str):
    # Retrieve
    query_embedding = embedding_model.encode(user_query)
    relevant_docs = vector_db.search(query_embedding, top_k=3)
    
    # Inject context
    context = "\n\n".join(relevant_docs)
    
    # Generate
    response = rag_agent.run_sync(
        f"Context:\n{context}\n\nQuestion: {user_query}"
    )
    
    return response.output
```

**Best Practices**:
- **Chunk documents**: Split large documents into smaller chunks (500-1000 tokens)
- **Top-K retrieval**: Retrieve 3-5 most relevant documents (balance between context and relevance)
- **Re-ranking**: Use a second model to re-rank retrieved documents
- **Citation**: Include source documents in response
- **Hybrid search**: Combine vector search with keyword search

**Common Mistakes**:
- ❌ Retrieving too many documents (exceeds token limits)
- ❌ Not chunking documents (loses granularity)
- ❌ No citation (can't verify sources)
- ❌ Stale data (not updating knowledge base)

**When to Use**:
- **Private data**: Company documents, user data
- **Recent information**: After model training cutoff
- **Domain-specific**: Specialized knowledge not in training data

---

### 12. ReAct Pattern (Reasoning + Acting) 🧠

#### **Definition**

The ReAct Pattern combines reasoning (thinking step-by-step) with acting (using tools) in an iterative loop until the task is complete.

#### **Why It Exists**

**Problem**: LLMs sometimes:
- Jump to conclusions without reasoning
- Don't use available tools effectively
- Can't handle multi-step tasks that require planning

**Solution**: Force the model to reason about the problem, then act using tools, then reason about results, repeat.

#### **Real-World Scenarios**

##### Scenario 1: Research Assistant
**Company**: Research platform

**Problem**: User asks complex question requiring multiple steps: search, analyze, synthesize.

**Solution**:
```python
# ReAct loop
while not task_complete:
    # Reasoning: Think about what to do next
    thought = agent.reason(
        f"Current state: {current_state}\n"
        f"Goal: {user_query}\n"
        f"What should I do next?"
    )
    
    # Acting: Use tools based on reasoning
    if "search" in thought.lower():
        results = search_tool(user_query)
        current_state += f"Search results: {results}\n"
    elif "analyze" in thought.lower():
        analysis = analyze_tool(current_state)
        current_state += f"Analysis: {analysis}\n"
    elif "done" in thought.lower():
        task_complete = True
    
    # Continue loop with updated state
```

**Impact**:
- **Better planning**: Model reasons before acting
- **Tool usage**: More effective use of available tools
- **Complex tasks**: Handles multi-step problems

##### Scenario 2: Code Debugging Assistant
**Company**: Development tool

**Problem**: Debugging requires: understanding error, searching solutions, testing fixes.

**Solution**:
```python
# ReAct for debugging
error = "TypeError: cannot concatenate str and int"

while not fixed:
    # Reason
    thought = agent.reason(f"Error: {error}\nWhat's the issue?")
    
    # Act
    if "search" in thought:
        solutions = search_stackoverflow(error)
    elif "test" in thought:
        test_result = run_tests()
        if test_result.passed:
            fixed = True
```

##### Scenario 3: Data Analysis Assistant
**Company**: Analytics platform

**Problem**: Analysis requires: loading data, cleaning, analyzing, visualizing.

**Solution**:
```python
# ReAct for analysis
task = "Analyze sales trends"

while not complete:
    thought = agent.reason(f"Task: {task}\nCurrent step: {current_step}")
    
    if "load" in thought:
        data = load_data_tool()
    elif "clean" in thought:
        data = clean_data_tool(data)
    elif "analyze" in thought:
        results = analyze_tool(data)
    elif "visualize" in thought:
        chart = visualize_tool(results)
        complete = True
```

#### **Implementation Details**

**Key Components**:
1. **Reasoning Step**: Model thinks about next action
2. **Acting Step**: Model uses tools
3. **Observation Step**: Model sees tool results
4. **Loop**: Repeat until task complete

**Code Structure**:
```python
# ReAct agent with tools
react_agent = Agent(
    tools=[search_web, calculate, get_weather],
    system_prompt="""You are a ReAct agent. 
    Think step-by-step about the problem.
    Use tools when needed.
    Format: Thought: [your reasoning] Action: [tool_name] Action Input: [input]"""
)

def react_loop(user_query: str):
    max_iterations = 10
    current_state = ""
    
    for i in range(max_iterations):
        # Reasoning + Acting (agent decides)
        response = react_agent.run_sync(
            f"Query: {user_query}\n"
            f"Current State: {current_state}\n"
            f"What should I do next?"
        )
        
        # Parse response (extract thought, action, input)
        thought, action, action_input = parse_react_response(response)
        
        # Execute action
        if action:
            result = execute_tool(action, action_input)
            current_state += f"Action: {action}\nResult: {result}\n"
        else:
            # Task complete
            break
    
    return current_state
```

**Best Practices**:
- **Limit iterations**: Prevent infinite loops (typically 5-10 iterations)
- **Clear formatting**: Use structured output for thought/action/observation
- **Tool validation**: Verify tool exists before calling
- **Error handling**: Handle tool failures gracefully

**Common Mistakes**:
- ❌ No iteration limit (infinite loops)
- ❌ Unclear reasoning format (hard to parse)
- ❌ Not using tools effectively

**When to Use**:
- **Complex tasks**: Require multiple steps and tools
- **Planning needed**: Can't solve in one shot
- **Tool-heavy**: Many tools available, need to choose wisely

---

### 13. Self-Consistency Pattern (Ensemble Voting) 🗳️

#### **Definition**

The Self-Consistency Pattern generates multiple candidate outputs, evaluates them, and selects the best one based on voting or scoring.

#### **Why It Exists**

**Problem**: Single LLM outputs are probabilistic and may be wrong. Multiple attempts increase chances of correctness.

**Solution**: Generate N candidates, evaluate each, select the best (or majority vote).

#### **Real-World Scenarios**

##### Scenario 1: Code Generation with Testing
**Company**: AI coding assistant

**Problem**: Generated code may have bugs. Multiple attempts increase chance of correct code.

**Solution**:
```python
# Generate multiple candidates
candidates = []
for i in range(5):
    code = generator_agent.run("Write a function to calculate tax")
    candidates.append(code)

# Evaluate each
scores = []
for code in candidates:
    score = evaluator_agent.run(f"Test this code: {code}")
    scores.append((code, score))

# Select best
best_code = max(scores, key=lambda x: x[1])[0]
```

**Impact**:
- **Higher accuracy**: 5 attempts → higher chance of correct code
- **Quality assurance**: Only use code that passes tests
- **Reliability**: Reduces production bugs

##### Scenario 2: Factual Question Answering
**Company**: Q&A platform

**Problem**: LLMs may hallucinate facts. Multiple answers increase confidence.

**Solution**:
```python
question = "What is the capital of France?"

# Generate multiple answers
answers = []
for i in range(5):
    answer = agent.run(question)
    answers.append(answer)

# Majority vote
from collections import Counter
most_common = Counter(answers).most_common(1)[0][0]
# If 4/5 say "Paris", use "Paris"
```

##### Scenario 3: Translation with Quality Check
**Company**: Translation service

**Problem**: Translations may be inaccurate. Multiple translations increase quality.

**Solution**:
```python
text = "Hello, how are you?"
target_language = "Spanish"

# Generate multiple translations
translations = []
for i in range(3):
    translation = translator_agent.run(f"Translate to {target_language}: {text}")
    translations.append(translation)

# Evaluate quality
best_translation = max(
    translations,
    key=lambda t: quality_evaluator.run(t).score
)
```

#### **Implementation Details**

**Key Components**:
1. **Multiple Generations**: Generate N candidates
2. **Evaluation**: Score or vote on candidates
3. **Selection**: Choose best or majority

**Code Structure**:
```python
# Self-consistency for code generation
def generate_with_consistency(prompt: str, n_candidates: int = 5):
    candidates = []
    
    # Generate candidates
    for i in range(n_candidates):
        code = generator_agent.run_sync(prompt)
        candidates.append(code.output)
    
    # Evaluate each
    evaluations = []
    for code in candidates:
        eval_result = evaluator_agent.run_sync(
            f"Evaluate this code: {code}"
        )
        evaluations.append((code, eval_result.output.score))
    
    # Select best
    best_code = max(evaluations, key=lambda x: x[1])[0]
    return best_code
```

**Best Practices**:
- **Odd number of candidates**: For voting, use odd numbers (3, 5, 7)
- **Diversity**: Use temperature variation to get diverse candidates
- **Evaluation criteria**: Clear criteria for selecting best
- **Cost consideration**: More candidates = higher cost

**Common Mistakes**:
- ❌ Too many candidates (expensive, diminishing returns)
- ❌ Not evaluating properly (bad selection)
- ❌ Same candidates (need diversity)

**When to Use**:
- **Critical tasks**: Where accuracy is essential
- **Probabilistic failures**: High failure rate on single attempts
- **Quality over speed**: Willing to pay cost for quality

**When NOT to Use**:
- **Real-time systems**: Latency is critical
- **Simple tasks**: Single attempt is sufficient
- **Cost-sensitive**: Can't afford multiple generations

---

## Pattern Selection Guide

### Decision Tree

```
Start: What is your task?

├─ Need to classify/route requests?
│  └─ Use: Router Pattern
│
├─ Need different behavior per user/context?
│  └─ Use: Strategy Pattern
│
├─ Tasks are independent?
│  ├─ Yes → Use: Parallelization Pattern
│  └─ No → Continue...
│
├─ Tasks must execute in sequence?
│  └─ Use: Chain of Responsibility Pattern
│
├─ Tasks are dynamic/unpredictable?
│  └─ Use: Orchestrator-Worker Pattern
│
├─ Need iterative refinement?
│  └─ Use: Prompt Chaining Pattern
│
├─ Need quality guarantees?
│  └─ Use: Evaluator-Optimizer Pattern
│
├─ Want to hide complexity?
│  └─ Use: Facade Pattern
│
├─ Need conversation memory?
│  └─ Use: Chat History Pattern
│
├─ Need persistence across sessions?
│  └─ Use: Persistent Memory Pattern
│
├─ Need private/recent data?
│  └─ Use: RAG Pattern
│
├─ Need multi-step reasoning with tools?
│  └─ Use: ReAct Pattern
│
└─ Need higher accuracy?
   └─ Use: Self-Consistency Pattern
```

### Pattern Combinations

Real-world systems often combine multiple patterns:

**Example: Enterprise Support System**
```
Router Pattern → Classify ticket
    ↓
Strategy Pattern → Select agent based on user tier
    ↓
Facade Pattern → Manager agent coordinates specialists
    ↓
Chat History Pattern → Maintain conversation context
    ↓
Persistent Memory Pattern → Save conversation to database
    ↓
RAG Pattern → Retrieve relevant knowledge base articles
```

**Example: Code Generation Assistant**
```
Orchestrator-Worker Pattern → Break down feature request
    ↓
Parallelization Pattern → Review code in parallel (security, style, performance)
    ↓
Evaluator-Optimizer Pattern → Ensure code quality
    ↓
Self-Consistency Pattern → Generate multiple candidates, select best
```

---

## Common Anti-Patterns to Avoid

### 1. The "God Prompt" Anti-Pattern ❌

**What it is**: One massive prompt trying to do everything.

**Why it's bad**:
- Token explosion
- Poor performance
- Unmaintainable

**Solution**: Use Router Pattern + specialized agents.

### 2. The "Sequential Everything" Anti-Pattern ❌

**What it is**: Running independent tasks sequentially.

**Why it's bad**:
- Slow (wastes time)
- Higher latency

**Solution**: Use Parallelization Pattern for independent tasks.

### 3. The "No Memory" Anti-Pattern ❌

**What it is**: Each interaction is isolated, no context.

**Why it's bad**:
- Poor user experience
- Can't handle follow-ups
- Feels robotic

**Solution**: Use Chat History Pattern.

### 4. The "Trust Everything" Anti-Pattern ❌

**What it is**: Using LLM output without validation.

**Why it's bad**:
- LLMs are probabilistic (sometimes wrong)
- No quality guarantees
- Production failures

**Solution**: Use Evaluator-Optimizer Pattern or Self-Consistency Pattern.

### 5. The "Hardcode Everything" Anti-Pattern ❌

**What it is**: Hardcoding all possible workflows.

**Why it's bad**:
- Inflexible
- Can't handle new scenarios
- Maintenance nightmare

**Solution**: Use Orchestrator-Worker Pattern for dynamic tasks.

---

## Conclusion

Mastering these design patterns is essential for building production-grade AI systems. Each pattern solves specific problems:

- **Routing & Classification**: Router, Strategy
- **Execution**: Parallelization, Chain of Responsibility, Orchestrator-Worker
- **Quality**: Prompt Chaining, Evaluator-Optimizer
- **Architecture**: Facade
- **Memory**: Chat History, Persistent Memory
- **Advanced**: RAG, ReAct, Self-Consistency

**Key Takeaways**:
1. **No one-size-fits-all**: Choose patterns based on requirements
2. **Combine patterns**: Real systems use multiple patterns together
3. **Start simple**: Begin with basic patterns, add complexity as needed
4. **Measure impact**: Track metrics (latency, cost, quality) when using patterns
5. **Avoid anti-patterns**: Learn from common mistakes

**Next Steps**:
1. Study the code examples for each pattern
2. Implement patterns in your own projects
3. Experiment with pattern combinations
4. Measure and optimize based on real-world usage

Remember: **Patterns are tools, not rules**. Use them when they solve your problem, not because they exist.

---

## References

- Code Examples: See `18_pattern_*.py` through `27_memory_*.py` in this directory
- Design Patterns Catalog: `design_patterns_catalog.txt`
- PydanticAI Documentation: https://pydantic.ai
- Industry Best Practices: Based on production systems at major AI companies

---

*Last Updated: February 2026*
*Author: Senior AI Engineer*
*For: Junior AI Engineers*
