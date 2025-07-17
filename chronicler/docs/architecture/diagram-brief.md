# Chronicler Architecture Diagram: Brief Explanation

This document provides a concise overview of each layer in the Chronicler system architecture diagram.

---

## AI Agent Layer
- **OpenAI Agents, LangChain Agents, Custom AI Agents:**
  - These are the intelligent agents that perform actions, make decisions, and interact with users or data. They are the entry point for all activity in the system.

## Chronicler Agent Wrapper
- **Purpose:**
  - Captures every action performed by the AI agents and prepares it for secure logging and validation.

## MCP Security Layer
- **Pre-Validation, Tool Execution, Post-Validation:**
  - Validates agent actions, enforces permissions and policies, and ensures only authorized, compliant actions are processed and logged.

## Blockchain Layer (On-Chain)
- **Registry, Access Control, Audit Log, MCP Gateway:**
  - Provides tamper-proof, decentralized storage for agent actions, permissions, and audit logs using smart contracts. Ensures transparency and verifiability.

## Off-Chain Layer
- **Indexer, IPFS Storage, Oracle Network:**
  - Handles detailed analytics, large data storage, and off-chain computation. Supports scalability and advanced features not feasible on-chain.

## Supabase (Off-Chain Database)
- **Role:**
  - Stores indexed events, analytics, and supports dashboard queries for real-time monitoring and compliance.

## Monitoring & Compliance
- **Dashboard, Alert System, Compliance Reports:**
  - Provides user interfaces and tools for monitoring system activity, receiving alerts, and generating compliance reports for regulatory needs.

---

This layered approach ensures that all AI agent actions are securely captured, validated, logged, and made available for monitoring and compliance, combining the strengths of on-chain and off-chain technologies.