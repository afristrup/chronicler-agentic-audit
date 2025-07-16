# Data Flow

Information architecture and data flow in Chronicler.

## Overview

Chronicler processes data through multiple layers with specific responsibilities.

## Data Flow Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Agent      │    │   Function      │    │   Decorator     │
│   Execution     │───▶│   Call          │───▶│   Capture       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Blockchain    │◀───│   Client SDK    │◀───│   Validation    │
│   Storage       │    │   Processing    │    │   & Metadata    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Indexer       │───▶│   Database      │───▶│   Dashboard     │
│   Processing    │    │   (Supabase)    │    │   Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Data Types

### Input Data
- **Function parameters** - Original function inputs
- **Metadata** - Agent, tool, and action metadata
- **Configuration** - Audit and network settings

### Processing Data
- **Action ID** - Unique identifier for each action
- **Timestamps** - Creation and completion times
- **Status** - Success, failure, pending states
- **Gas usage** - Blockchain transaction costs

### Output Data
- **Function results** - Original function outputs
- **Audit logs** - Blockchain transaction hashes
- **Analytics** - Performance and usage metrics

## Storage Layers

### On-Chain Storage
- **Action logs** - Minimal data for verification
- **Merkle roots** - Batch commitment hashes
- **Registry data** - Agent and tool registrations

### Off-Chain Storage
- **Detailed logs** - Full input/output data
- **Analytics** - Performance metrics
- **Metadata** - Extended information

### IPFS Storage
- **Batch data** - Complete action batches
- **Detailed logs** - Full audit information
- **Metadata** - Extended action metadata

## Data Validation

### Pre-Processing
- **Input validation** - Parameter type checking
- **Permission checks** - Access control validation
- **Rate limiting** - Usage limit enforcement

### Post-Processing
- **Output validation** - Result verification
- **Gas optimization** - Transaction cost analysis
- **Error handling** - Failure logging and recovery

## Security Considerations

- **Data encryption** - Sensitive data protection
- **Access control** - Permission-based access
- **Audit trails** - Complete action history
- **Data integrity** - Hash-based verification