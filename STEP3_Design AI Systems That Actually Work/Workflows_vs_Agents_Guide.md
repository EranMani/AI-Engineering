# Workflows vs Agents: A Senior AI Engineer's Guide

> **Mission**: Learn when to use workflows (reliable systems) vs agents (magical systems). This guide will transform you from a junior engineer who builds "magic" into a senior engineer who builds "reliable systems."

---

## Table of Contents

1. [The Core Debate: Workflows vs Agents](#the-core-debate-workflows-vs-agents)
2. [The 3 Layers of Engineering Maturity](#the-3-layers-of-engineering-maturity)
3. [Layer 1: Understanding the Vocabulary](#layer-1-understanding-the-vocabulary)
4. [Layer 2: The 5 Control Flow Patterns](#layer-2-the-5-control-flow-patterns)
5. [Layer 3: Senior Implementation Guidelines](#layer-3-senior-implementation-guidelines)
6. [Real-World Case Studies](#real-world-case-studies)
7. [Decision Framework: When to Use What](#decision-framework-when-to-use-what)
8. [Common Mistakes and How to Avoid Them](#common-mistakes-and-how-to-avoid-them)

---

## The Core Debate: Workflows vs Agents

### The Fundamental Question

As a junior AI engineer, you might think: "Why not just build an agent that can do everything?" 

**The answer**: Because reliability matters more than magic.

### The Reality Check

- **Agents (Magic)**: Work 20% of the time, break 80% of the time
- **Workflows (Reliable)**: Work 99% of the time, break 1% of the time

**Senior Rule**: Default to Workflows. Only build an Agent if a Workflow is impossible.

---

## The 3 Layers of Engineering Maturity

Think of your journey as climbing three layers:

```
Layer 3: Senior Implementation Guidelines (The "How")
         ↑
Layer 2: The 5 Control Flow Patterns (The "What")
         ↑
Layer 1: Understanding the Vocabulary (The "Foundation")
```

As a junior, you start at Layer 1. You only move up when you are forced to (usually by production failures).

---

## Layer 1: Understanding the Vocabulary

### The Problem: Industry Hype vs Engineering Reality

The AI industry uses words loosely. As an engineer, you must be precise.

### What People Call "Agents" (The Hype)

**The Hype Definition**: A magical system where you say "Make me a website," and the AI:
- Figures out every step automatically
- Writes code
- Tests it
- Fixes errors
- Deploys it
- All without human help

**Reality**: These systems break 80% of the time.

**Example**: Devin (the "AI Software Engineer") - impressive demos, but fails in production because:
- It makes unpredictable decisions
- It can't handle edge cases
- It hallucinates solutions
- It's impossible to debug when it fails

### What Engineers Call "Workflows" (The Reality)

**The Engineering Definition**: A system where **YOU** define the path (the train tracks). The AI just pushes the train along the tracks.

**Reality**: These work 99% of the time.

**Key Difference**: 
- **Agent**: AI decides the path
- **Workflow**: You decide the path, AI executes steps

### The Analogy: Train Tracks vs Free-Roaming Train

**Workflow (Reliable)**:
```
You build the tracks: A → B → C → D
AI follows the tracks: Step A → Step B → Step C → Step D
```

**Agent (Unreliable)**:
```
You say: "Go to D"
AI decides: "Maybe I'll go A → X → Y → Z → D?"
Sometimes it works. Sometimes it goes to F instead.
```

### Why This Matters

When you're building production systems:
- **Reliability** > **Magic**
- **Predictability** > **Autonomy**
- **Debuggability** > **Flexibility**

---

## Layer 2: The 5 Control Flow Patterns

These are your **Lego blocks**. You don't need fancy frameworks (like LangChain) to build these. You can build them with simple Python functions.

### Pattern 1: Prompt Chaining (The "Relay Race") 🏃‍♂️➡️🏃

#### What It Is

Output of Step A becomes Input of Step B. Like a relay race where one runner passes the baton to the next.

#### When to Use

- The task is too big for one prompt
- You need to break down complex tasks into smaller steps
- Each step depends on the previous step's output

#### Simple Example

**Task**: Write a book

**Workflow**:
1. Step 1: Generate Outline → Output: Book Outline
2. Step 2: Write Chapter 1 (using Outline) → Output: Chapter 1
3. Step 3: Write Chapter 2 (using Outline) → Output: Chapter 2
4. Step 4: Write Chapter 3 (using Outline) → Output: Chapter 3

**Why This Works**: 
- Each chapter is written with the same outline context
- You can validate the outline before writing chapters
- If Chapter 2 fails, you don't lose Chapter 1

#### Code Example (Pseudocode)

```python
def write_book(topic):
    # Step 1: Generate outline
    outline = llm_call(
        prompt=f"Create a detailed outline for a book about {topic}",
        output_format="json"
    )
    
    # Step 2: Write chapters (each uses the outline)
    chapters = []
    for chapter_num in outline['chapters']:
        chapter = llm_call(
            prompt=f"Write Chapter {chapter_num} based on this outline: {outline}",
            output_format="text"
        )
        chapters.append(chapter)
    
    return {"outline": outline, "chapters": chapters}
```

#### Real-World Use Case: Customer Support Email Generator

**Scenario**: A customer complains about a delayed order. You need to:
1. Extract key information (order ID, delay reason, customer email)
2. Generate a personalized apology email
3. Include order tracking information

**Workflow**:
```
Email Input → [Extract Info] → Structured Data → [Generate Email] → Final Email
```

**Why Workflow, Not Agent**:
- You know the exact steps needed
- Each step has a clear input/output
- You can test each step independently
- If extraction fails, you don't waste time generating an email

---

### Pattern 2: Routing (The "Traffic Cop") 🚦

#### What It Is

Classify input, then send it to the right worker. Like a traffic cop directing cars to different lanes.

#### When to Use

- You have distinct categories of requests
- Different categories need different handling
- You can classify requests reliably

#### Simple Example

**Task**: Handle customer support tickets

**Workflow**:
1. Step 1: Classify ticket → "Is this a Refund Request or Technical Bug?"
2. Step 2: Route based on classification
   - If Refund → Go to Finance System
   - If Bug → Go to Jira System
   - If Question → Go to Knowledge Base

**Why This Works**:
- Each category gets specialized handling
- You can optimize each route independently
- Easy to add new categories

#### Code Example (Pseudocode)

```python
def handle_support_ticket(ticket_text):
    # Step 1: Classify
    classification = llm_call(
        prompt=f"Classify this ticket: {ticket_text}\nCategories: refund, bug, question",
        output_format="json"
    )
    
    # Step 2: Route (deterministic code, not LLM)
    if classification['category'] == 'refund':
        return finance_system.process(ticket_text)
    elif classification['category'] == 'bug':
        return jira_system.create_ticket(ticket_text)
    elif classification['category'] == 'question':
        return knowledge_base.answer(ticket_text)
    else:
        return default_handler.process(ticket_text)
```

#### Real-World Use Case: E-commerce Order Processing

**Scenario**: Process incoming orders that could be:
- Regular orders (ship immediately)
- Pre-orders (wait for stock)
- Custom orders (need human review)
- Bulk orders (need pricing approval)

**Workflow**:
```
Order Input → [Classify Order Type] → Route to Appropriate Handler
```

**Why Workflow, Not Agent**:
- You have a finite set of order types
- Each type has a clear processing path
- You can use deterministic code for routing (faster, cheaper, more reliable)
- Easy to add new order types

**Senior Tip**: Use keyword matching or simple rules for routing when possible. Only use LLM classification when the categories are semantically complex.

---

### Pattern 3: Parallelization (The "Swarm") 🐝🐝🐝

#### What It Is

Run multiple independent tasks at the same time (Async). Like a swarm of bees working simultaneously.

#### When to Use

- Speed matters
- Tasks don't rely on each other
- You can run them independently

#### Simple Example

**Task**: Validate user-generated content

**Workflow**:
- Task A: Check for profanity (runs in parallel)
- Task B: Check for factual accuracy (runs in parallel)
- Task C: Check for spam patterns (runs in parallel)

**Result**: If ANY task fails, block the message. All tasks run simultaneously, so it's fast.

**Why This Works**:
- 3x faster than running sequentially
- Each check is independent
- You get all results at once

#### Code Example (Pseudocode)

```python
import asyncio

async def validate_content(content):
    # Run all checks in parallel
    results = await asyncio.gather(
        check_profanity(content),
        check_factual_accuracy(content),
        check_spam_patterns(content)
    )
    
    # If any check fails, block
    if any(not result['passed'] for result in results):
        return {"status": "blocked", "reasons": [r['reason'] for r in results if not r['passed']]}
    
    return {"status": "approved"}
```

#### Real-World Use Case: Document Processing Pipeline

**Scenario**: Process a legal contract document. You need to:
- Extract key dates
- Identify parties involved
- Check for compliance clauses
- Summarize main terms

**Workflow**:
```
Document → [Extract Dates] ┐
         → [Identify Parties] ├─ (All run in parallel)
         → [Check Compliance] │
         → [Summarize Terms] ┘
         → Combine Results
```

**Why Workflow, Not Agent**:
- Each extraction task is independent
- You know exactly what to extract
- Parallel execution is 4x faster
- If one extraction fails, others still succeed

---

### Pattern 4: Orchestrator-Worker (The "Manager") 👷‍♂️👷

#### What It Is

A central LLM (Manager) breaks down a plan and assigns tasks to other LLMs (Workers), then compiles the results.

#### When to Use

- The sub-tasks are dynamic (you don't know ahead of time how many steps are needed)
- The task is too complex for a single LLM
- You need specialized workers for different tasks

#### Simple Example

**Task**: Research a topic and write a report

**Workflow**:
1. **Orchestrator**: "To research 'Climate Change', I need to:
   - Research scientific data (Worker A)
   - Research economic impact (Worker B)
   - Research policy changes (Worker C)
   - Write synthesis report (Worker D)"

2. **Workers**: Each worker does their specialized task
3. **Orchestrator**: Combines all results into final report

**Why This Works**:
- Each worker is specialized (better quality)
- Orchestrator can adapt the plan dynamically
- Failures are isolated (if Worker B fails, others continue)

#### Code Example (Pseudocode)

```python
def research_and_report(topic):
    # Step 1: Orchestrator creates plan
    plan = orchestrator_llm.call(
        prompt=f"Create a research plan for: {topic}",
        output_format="json"  # Returns: {"steps": ["research_science", "research_economics", ...]}
    )
    
    # Step 2: Execute each step with specialized workers
    results = []
    for step in plan['steps']:
        worker = get_worker_for_step(step)  # Returns specialized worker
        result = worker.execute(step, topic)
        results.append(result)
    
    # Step 3: Orchestrator synthesizes results
    final_report = orchestrator_llm.call(
        prompt=f"Combine these research results into a report: {results}",
        output_format="text"
    )
    
    return final_report
```

#### Real-World Use Case: Customer Onboarding System

**Scenario**: Onboard a new enterprise customer. The steps vary based on:
- Customer type (SMB vs Enterprise)
- Product selection
- Compliance requirements
- Integration needs

**Workflow**:
```
Customer Data → [Orchestrator: Create Onboarding Plan] → Dynamic Steps
                                                              ↓
                    [Worker: Collect Data] → [Worker: Validate] → [Worker: Create Account] → [Worker: Send Welcome]
```

**Why Orchestrator-Worker, Not Simple Workflow**:
- Steps are dynamic (different customers need different steps)
- You can't hardcode the sequence
- But you still control the overall structure (it's a workflow, not a free agent)

**Senior Tip**: This is the closest to an "agent" you should get. The key difference: the orchestrator creates a PLAN, and you execute that plan deterministically. You don't let it make decisions during execution.

---

### Pattern 5: Evaluator-Optimizer (The "Loop") 🔄

#### What It Is

Generate → Critique → Fix. A feedback loop that improves quality.

#### When to Use

- Quality is more important than speed
- You need to ensure output meets specific criteria
- You can define clear evaluation criteria

#### Simple Example

**Task**: Write a professional email

**Workflow**:
1. **Generate**: Write an email draft
2. **Evaluate**: "Is this tone polite?" → No
3. **Optimize**: Rewrite to be polite
4. **Evaluate**: "Is this tone polite?" → Yes
5. **Done**: Return final email

**Why This Works**:
- Ensures quality before sending
- Can iterate until criteria are met
- Prevents embarrassing mistakes

#### Code Example (Pseudocode)

```python
def write_polite_email(request):
    max_iterations = 3
    
    for iteration in range(max_iterations):
        # Step 1: Generate
        email = generator_llm.call(
            prompt=f"Write an email: {request}",
            output_format="text"
        )
        
        # Step 2: Evaluate
        evaluation = evaluator_llm.call(
            prompt=f"Evaluate this email for politeness (1-10): {email}",
            output_format="json"
        )
        
        # Step 3: Check if good enough
        if evaluation['politeness_score'] >= 8:
            return email
        
        # Step 4: Optimize (if not good enough)
        email = optimizer_llm.call(
            prompt=f"Rewrite this email to be more polite: {email}",
            output_format="text"
        )
    
    # If we've tried 3 times, return best attempt
    return email
```

#### Real-World Use Case: Code Generation with Quality Checks

**Scenario**: Generate API endpoint code that must:
- Follow company coding standards
- Include error handling
- Have proper documentation
- Pass security checks

**Workflow**:
```
Requirements → [Generate Code] → [Evaluate: Standards?] → Not Good
                                                              ↓
                                    [Optimize: Fix Standards] → [Evaluate: Error Handling?] → Not Good
                                                              ↓
                                    [Optimize: Add Error Handling] → [Evaluate: All Checks?] → Pass ✓
```

**Why Evaluator-Optimizer, Not One-Shot Generation**:
- Code quality is critical
- Multiple criteria must be met
- One-shot generation often misses requirements
- Iterative improvement ensures quality

**Senior Tip**: Set a maximum iteration limit to prevent infinite loops. Also, make evaluation criteria very specific (not vague like "is this good?").

---

## Layer 3: Senior Implementation Guidelines

These are the principles that separate juniors from seniors.

### Guideline 1: Deterministic > Probabilistic

**The Rule**: Use if statements (deterministic code) whenever possible. Don't ask an LLM to route if a keyword search works.

#### Why This Matters

**Junior Approach**:
```python
# Using LLM for everything (slow, expensive, unreliable)
category = llm_call(f"Classify this: {text}")
```

**Senior Approach**:
```python
# Use deterministic code first
if "refund" in text.lower():
    category = "refund"
elif "bug" in text.lower() or "error" in text.lower():
    category = "bug"
else:
    # Only use LLM when deterministic methods fail
    category = llm_call(f"Classify this: {text}")
```

#### Real-World Example: Email Routing

**Scenario**: Route customer emails to the right department.

**Junior Approach**: Use LLM to classify every email.

**Senior Approach**:
1. Check for keywords first (fast, free, reliable)
2. Use LLM only for ambiguous cases
3. Cache common patterns

**Result**: 
- 80% of emails routed instantly (keyword matching)
- 20% use LLM (ambiguous cases)
- 10x faster, 10x cheaper, more reliable

### Guideline 2: Start Vertical, then Horizontal

**The Rule**: Don't build a "General Customer Support Bot." Build a "Order Tracking Bot." Perfect it. Then add "Refunds." Then add "Technical Support."

#### Why This Matters

**Junior Mistake**: Trying to handle everything at once.

**Result**: 
- System is mediocre at everything
- Hard to debug
- Hard to improve
- Users frustrated

**Senior Approach**: Build one thing perfectly, then expand.

#### Real-World Example: Customer Support System

**Phase 1 (Vertical)**: Build "Where is my order?" bot
- Handles 100% of order tracking questions perfectly
- Users love it
- You understand the patterns

**Phase 2 (Horizontal)**: Add "Refund Requests"
- Reuse patterns from Phase 1
- Users already trust the system
- Easy to debug (isolated feature)

**Phase 3 (Horizontal)**: Add "Technical Support"
- System is now comprehensive
- But each feature is well-built
- Easy to maintain

**Result**: 
- Each feature works perfectly
- Easy to test and debug
- Users have confidence
- You can iterate quickly

### Guideline 3: Guardrails are Non-Negotiable

**The Rule**: Never ship without a "Judge" (Evaluator) at the end.

#### Why This Matters

**The Amazon Example**: Amazon's bot gave away proprietary code because it had no guardrails.

**What Happened**:
1. User asked: "Show me the code for X feature"
2. Bot: Generated code (hallucinated or from training data)
3. No guardrail: Code was sent to user
4. Result: Security breach

**The Fix**: Always add a guardrail evaluator.

#### Real-World Example: Code Generation System

**Workflow**:
```
User Request → [Generate Code] → [Guardrail: Check Policy] → Safe? → Send to User
                                                              ↓
                                                          Not Safe → "I cannot answer that"
```

**Guardrail Checks**:
- Does this output violate company policy?
- Does this contain sensitive information?
- Is this output harmful?
- Does this output make sense?

**Code Example**:
```python
def generate_code_with_guardrails(request):
    # Step 1: Generate
    code = code_generator.call(request)
    
    # Step 2: Guardrail (ALWAYS check)
    guardrail_check = evaluator_llm.call(
        prompt=f"Does this code violate company policy or contain sensitive info? {code}",
        output_format="json"
    )
    
    # Step 3: Decision (deterministic)
    if guardrail_check['violates_policy']:
        return "I cannot provide that information due to company policy."
    
    return code
```

**Senior Tip**: Guardrails should be the LAST step before output. Even if everything else fails, the guardrail should catch issues.

---

## Real-World Case Studies

### Case Study 1: E-commerce Customer Support System

#### The Problem

An e-commerce company receives 10,000 support tickets per day. They need to:
- Route tickets to the right department
- Generate personalized responses
- Track resolution times

#### Junior Approach (Agent)

Build a "magical agent" that:
- Understands any question
- Generates perfect responses
- Routes automatically

**Result**: 
- Works 20% of the time
- Generates incorrect information
- Routes to wrong departments
- Impossible to debug

#### Senior Approach (Workflow)

**Architecture**:
```
Ticket Input → [Router: Classify] → Route to Handler
                                    ↓
                    [Refund Handler] → [Extract Info] → [Generate Email] → [Guardrail] → Send
                    [Bug Handler] → [Create Jira Ticket] → [Notify Team]
                    [Question Handler] → [Search KB] → [Generate Answer] → [Guardrail] → Send
```

**Patterns Used**:
1. **Routing** (Pattern 2): Classify ticket type
2. **Prompt Chaining** (Pattern 1): Extract info → Generate email
3. **Evaluator-Optimizer** (Pattern 5): Check email quality before sending
4. **Guardrails**: Always validate output

**Why This Works**:
- Each step is testable
- Easy to debug (know exactly where it failed)
- Reliable (99% success rate)
- Can improve each component independently

**Implementation Details**:
- Use keyword matching for 80% of routing (fast, free)
- Use LLM only for ambiguous cases
- Cache common responses
- Monitor each step for failures

### Case Study 2: Document Processing Pipeline

#### The Problem

A law firm receives 500 legal documents per day. They need to:
- Extract key information (dates, parties, amounts)
- Classify document type
- Flag important clauses
- Generate summaries

#### Junior Approach (Agent)

Build an agent that "understands" any legal document and extracts everything automatically.

**Result**:
- Misses critical information
- Hallucinates data
- Inconsistent results
- Can't handle edge cases

#### Senior Approach (Workflow)

**Architecture**:
```
Document → [Parallel Extraction] → Combine Results
         ├─ [Extract Dates]
         ├─ [Extract Parties]
         ├─ [Extract Amounts]
         └─ [Classify Type]
         → [Validate] → [Generate Summary] → [Guardrail] → Store
```

**Patterns Used**:
1. **Parallelization** (Pattern 3): Extract multiple fields simultaneously
2. **Prompt Chaining** (Pattern 1): Extract → Validate → Summarize
3. **Evaluator-Optimizer** (Pattern 5): Validate extracted data quality
4. **Guardrails**: Check for sensitive information

**Why This Works**:
- Fast (parallel extraction)
- Reliable (validation step catches errors)
- Consistent (same extraction logic for all documents)
- Easy to improve (can tune each extractor independently)

**Implementation Details**:
- Use specialized prompts for each extraction task
- Validate extracted data against schemas
- Retry failed extractions
- Log all extractions for monitoring

### Case Study 3: Content Moderation System

#### The Problem

A social media platform needs to moderate user-generated content:
- Check for profanity
- Check for hate speech
- Check for spam
- Check for misinformation

#### Junior Approach (Agent)

Build an agent that "understands" content and makes moderation decisions.

**Result**:
- Inconsistent decisions
- Misses subtle violations
- False positives
- Can't explain decisions

#### Senior Approach (Workflow)

**Architecture**:
```
Content → [Parallel Checks] → [Decision Logic] → Action
        ├─ [Profanity Check]
        ├─ [Hate Speech Check]
        ├─ [Spam Check]
        └─ [Fact Check]
        → [Combine Results] → [Apply Rules] → Block/Approve/Flag
```

**Patterns Used**:
1. **Parallelization** (Pattern 3): Run all checks simultaneously
2. **Routing** (Pattern 2): Route based on violation type
3. **Evaluator-Optimizer** (Pattern 5): Improve detection accuracy
4. **Guardrails**: Always human review for edge cases

**Why This Works**:
- Fast (parallel checks)
- Transparent (can explain each decision)
- Reliable (multiple checks catch violations)
- Improvable (can tune each check independently)

**Implementation Details**:
- Use specialized models for each check type
- Combine results with deterministic logic
- Flag uncertain cases for human review
- Monitor false positive/negative rates

### Case Study 4: Research Assistant System

#### The Problem

A research team needs to:
- Research topics across multiple sources
- Synthesize findings
- Generate reports
- Answer follow-up questions

#### Junior Approach (Agent)

Build an agent that "researches anything" and generates perfect reports.

**Result**:
- Hallucinates sources
- Misses important information
- Inconsistent report quality
- Can't handle complex queries

#### Senior Approach (Workflow)

**Architecture**:
```
Query → [Orchestrator: Plan Research] → [Workers: Execute Research] → [Synthesize] → [Generate Report] → [Guardrail]
        ↓
    [Researcher Worker] → [Analyst Worker] → [Writer Worker] → [Reviewer Worker]
```

**Patterns Used**:
1. **Orchestrator-Worker** (Pattern 4): Dynamic research planning
2. **Prompt Chaining** (Pattern 1): Research → Analyze → Write → Review
3. **Evaluator-Optimizer** (Pattern 5): Improve report quality
4. **Guardrails**: Verify sources and facts

**Why This Works**:
- Adapts to different research needs
- Specialized workers produce better results
- Can verify each step
- Easy to add new research sources

**Implementation Details**:
- Orchestrator creates research plan based on query
- Each worker specializes in one task
- Synthesize results before writing
- Always cite sources
- Validate facts before output

---

## Decision Framework: When to Use What

### Use Workflows When:

✅ **You know the steps ahead of time**
- Example: Process order → Validate → Charge → Ship

✅ **You need reliability**
- Example: Financial transactions, medical diagnoses

✅ **You need debuggability**
- Example: Production systems where failures cost money

✅ **You can define clear success criteria**
- Example: Email must be polite, code must pass tests

### Use Agents (Orchestrator-Worker) When:

⚠️ **Steps are dynamic but bounded**
- Example: Research tasks (plan varies, but structure is known)

⚠️ **You need some flexibility but still want control**
- Example: Customer onboarding (steps vary by customer type)

❌ **Never use free-roaming agents in production**
- They're too unreliable
- They're impossible to debug
- They're unpredictable

### Decision Tree

```
Start Here: Do I know the steps?
│
├─ YES → Use Workflow
│   │
│   ├─ Steps are sequential? → Prompt Chaining
│   ├─ Steps are independent? → Parallelization
│   ├─ Need to route? → Routing
│   └─ Need quality checks? → Evaluator-Optimizer
│
└─ NO → Can I bound the problem?
    │
    ├─ YES → Use Orchestrator-Worker
    │   └─ Orchestrator creates plan, Workers execute deterministically
    │
    └─ NO → Reconsider the problem
        └─ Maybe break it into smaller, known steps?
```

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Using Agents When Workflows Would Work

**Symptom**: "My agent is unreliable. It works sometimes but fails randomly."

**Fix**: Break down the problem into known steps. Use a workflow instead.

**Example**:
- ❌ Agent: "Generate a complete marketing campaign"
- ✅ Workflow: "Generate headline → Generate body → Generate CTA → Combine"

### Mistake 2: Not Using Deterministic Code First

**Symptom**: "My system is slow and expensive. Every request uses the LLM."

**Fix**: Use if statements, keyword matching, or rules first. Only use LLM when necessary.

**Example**:
- ❌ LLM classifies every email
- ✅ Keyword matching for 80%, LLM for 20%

### Mistake 3: Building Everything at Once

**Symptom**: "My system handles 10 different tasks, but none of them work well."

**Fix**: Build one thing perfectly, then expand.

**Example**:
- ❌ General customer support bot (handles everything, works poorly)
- ✅ Order tracking bot (handles one thing, works perfectly) → Then add refunds → Then add tech support

### Mistake 4: Skipping Guardrails

**Symptom**: "My system generated inappropriate content" or "My system leaked sensitive data."

**Fix**: Always add a guardrail evaluator as the last step.

**Example**:
- ❌ Generate code → Send to user
- ✅ Generate code → Check guardrails → Send to user (if safe)

### Mistake 5: Not Setting Iteration Limits

**Symptom**: "My evaluator-optimizer loop runs forever."

**Fix**: Set a maximum iteration limit.

**Example**:
```python
max_iterations = 3  # Don't loop forever
for i in range(max_iterations):
    # ... generate and evaluate ...
    if good_enough:
        break
```

### Mistake 6: Using LLMs for Everything

**Symptom**: "My system is slow and expensive."

**Fix**: Use LLMs only for tasks that require understanding. Use deterministic code for everything else.

**Example**:
- ❌ LLM routes emails, LLM formats responses, LLM sends emails
- ✅ Keyword matching routes emails, LLM generates responses, deterministic code sends emails

---

## Summary: The Senior Engineer's Answer

### If an Interviewer Asks: "How do you build AI Agents?"

**Your Answer**:

> "I prefer to start with **Workflows**, not Agents. I use deterministic code for routing and state management, and I only use LLMs for the specific cognitive steps (like summarization or generation).
>
> I typically use patterns like **Prompt Chaining** or **Evaluator-Optimizer loops** to ensure quality, and I always wrap the output in **Guardrails** to prevent hallucinations.
>
> I only consider an Orchestrator-Worker pattern (the closest thing to an agent) when the steps are dynamic but bounded. Even then, the orchestrator creates a PLAN that is executed deterministically.
>
> The key principle: **Reliability > Magic**. I'd rather build a system that works 99% of the time than one that's impressive 20% of the time."

### Key Takeaways

1. **Default to Workflows**: They're more reliable, debuggable, and maintainable
2. **Use the 5 Patterns**: They're your building blocks for any AI system
3. **Deterministic First**: Use if statements before LLMs
4. **Start Vertical**: Build one thing perfectly, then expand
5. **Guardrails Always**: Never ship without output validation
6. **Reliability > Magic**: Production systems need to work, not impress

---

## Next Steps

Now that you understand workflows vs agents:

1. **Practice**: Build a simple workflow using one of the 5 patterns
2. **Analyze**: Look at existing AI systems and identify which patterns they use
3. **Refactor**: Take a "magical agent" idea and break it into a reliable workflow
4. **Learn**: Study production AI systems to see how they balance flexibility and reliability

Remember: As a junior engineer, you're tempted to build magic. As a senior engineer, you build reliability.

---

## Additional Resources

- **Pattern 1 (Prompt Chaining)**: Study how content generation pipelines work
- **Pattern 2 (Routing)**: Study how customer support systems route tickets
- **Pattern 3 (Parallelization)**: Study async programming and parallel processing
- **Pattern 4 (Orchestrator-Worker)**: Study microservices architecture (similar concepts)
- **Pattern 5 (Evaluator-Optimizer)**: Study quality assurance and testing workflows

**The Golden Rule**: If you can solve it with a workflow, use a workflow. Only use an agent (orchestrator-worker) when a workflow is impossible.
