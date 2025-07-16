# Client SDK

Python SDK architecture and design.

## Overview

The Chronicler Client SDK provides seamless integration with the blockchain layer through decorators and services.

## Core Components

### Decorators
- **@chronicler** - Main decorator for function/class decoration
- **ActionMetadata** - Metadata for agent actions
- **AuditConfig** - Configuration for audit logging

### Services
- **ChroniclerService** - Blockchain interaction service
- **RegistryService** - Agent and tool registration
- **AuditService** - Action logging service

### Configuration
- **Environment variables** - Network and contract configuration
- **Programmatic config** - Runtime configuration
- **Validation** - Input validation and error handling

## Integration Flow

1. **Function Decoration** - Decorator captures function metadata
2. **Pre-validation** - Check permissions and rate limits
3. **Function Execution** - Execute the original function
4. **Post-processing** - Log action to blockchain
5. **Result Return** - Return function result with audit info

## Error Handling

- **Network errors** - Retry with exponential backoff
- **Contract errors** - Graceful degradation
- **Validation errors** - Clear error messages
- **Timeout handling** - Configurable timeouts

## Performance

- **Batch processing** - Group multiple actions
- **Async support** - Non-blocking operations
- **Caching** - Cache contract calls
- **Connection pooling** - Efficient network usage