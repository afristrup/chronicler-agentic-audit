# Architecture Overview

Chronicler's system architecture and component design.

## System Layers

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

## Components

- **[Smart Contracts](./smart-contracts.md)** - On-chain logic
- **[Client SDK](./client-sdk.md)** - Python integration
- **[Services](./services.md)** - Off-chain processing
- **[Data Flow](./data-flow.md)** - Information architecture