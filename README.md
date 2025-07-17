# Chronicler: The Agentic Audit

## Overview

Chronicler is a comprehensive blockchain-based audit system designed to provide complete transparency and accountability for the actions of AI agents. By capturing every agent action, validating tool usage, and ensuring compliance transparency, Chronicler eliminates the need to manually explain what your AI agents did—the complete story is automatically recorded and verifiable on-chain.

## Structure

```text
/chronicler/layer          # the blockchain layer (solidity/bun)
/chronicler/client         # the application integration (python/uv)
/chronicler/landing        # the landing page (nextjs/bun)
```
## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          AI AGENT LAYER                             │
├─────────────────────┬───────────────────┬─────────────────────────┤
│   OpenAI Agents     │  LangChain Agents │   Custom AI Agents      │
└──────────┬──────────┴─────────┬─────────┴──────────┬──────────────┘
           │                    │                     │
           └────────────────────┴─────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Chronicler Agent    │
                    │      Wrapper          │
                    └───────────┬───────────┘
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                      MCP SECURITY LAYER                            │
├─────────────────┬──────────────────┬──────────────────────────────┤
│  Pre-Validation │  Tool Execution  │  Post-Validation             │
└─────────────────┴──────────────────┴──────────────────────────────┘
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                    BLOCKCHAIN LAYER (ON-CHAIN)                     │
├───────────────┬────────────────┬────────────────┬─────────────────┤
│   Registry    │  Access Control│   Audit Log    │  MCP Gateway    │
│               │                │                 │                 │
│ • Agents      │ • Permissions  │ • Action Logs  │ • Validation    │
│ • Tools       │ • Rate Limits  │ • Merkle Roots │ • Execution     │
│ • Operators   │ • Policies     │ • Batch Commits│ • Callbacks     │
└───────────────┴────────────────┴────────────────┴─────────────────┘
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                      OFF-CHAIN LAYER                               │
├─────────────────┬──────────────────┬──────────────────────────────┤
│    Indexer      │   IPFS Storage   │    Oracle Network           │
│                 │                  │                              │
│ • Event Logs    │ • Detailed Logs  │ • Data Verification         │
│ • Metrics       │ • Input/Output   │ • Multi-sig Confirmation    │
│ • Analytics     │ • Batch Data     │ • Off-chain Computation     │
└─────────────────┴──────────────────┴──────────────────────────────┘
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                     MONITORING & COMPLIANCE                        │
├─────────────────┬──────────────────┬──────────────────────────────┤
│   Dashboard     │  Alert System    │   Compliance Reports        │
└─────────────────┴──────────────────┴──────────────────────────────┘
```

TODO: Rewrite this. Haha Haha
