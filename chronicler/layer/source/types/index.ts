// Core types for the Chronicler system

export interface Agent {
    id: string;
    operator: string;
    metadataURI: string;
    isActive: boolean;
    createdAt: number;
    lastActionAt: number;
    totalActions: number;
}

export interface Tool {
    id: string;
    name: string;
    metadataURI: string;
    categoryId: string;
    isActive: boolean;
    riskLevel: number;
    usageCount: number;
    lastUsedAt: number;
}

export interface Category {
    id: string;
    name: string;
    description: string;
    isActive: boolean;
    riskMultiplier: number;
}

export interface ActionLog {
    actionId: string;
    agentId: string;
    toolId: string;
    dataHash: string;
    timestamp: number;
    status: ActionStatus;
    gasUsed: number;
    batchId: number;
}

export interface BatchCommitment {
    merkleRoot: string;
    startIndex: number;
    endIndex: number;
    timestamp: number;
    ipfsHash: string;
    actionCount: number;
    isCommitted: boolean;
}

export interface Policy {
    dailyLimit: number;
    maxGas: number;
    maxRisk: number;
    cooldownPeriod: number;
    isActive: boolean;
    createdAt: number;
    updatedAt: number;
}

export interface RateLimit {
    lastActionTime: number;
    dailyActionCount: number;
    lastResetTime: number;
    totalActions: number;
    totalGasUsed: number;
}

export interface AgentPolicy {
    agentId: string;
    policyId: number;
    isActive: boolean;
    assignedAt: number;
}

export interface ToolPolicy {
    toolId: string;
    policyId: number;
    isActive: boolean;
    assignedAt: number;
}

export enum ActionStatus {
    PENDING = 0,
    SUCCESS = 1,
    FAILED = 2,
    CANCELLED = 3
}

export enum ContractRole {
    ADMIN_ROLE = "ADMIN_ROLE",
    OPERATOR_ROLE = "OPERATOR_ROLE",
    REGISTRAR_ROLE = "REGISTRAR_ROLE",
    LOGGER_ROLE = "LOGGER_ROLE",
    BATCH_COMMITTER_ROLE = "BATCH_COMMITTER_ROLE",
    POLICY_ADMIN_ROLE = "POLICY_ADMIN_ROLE",
    RATE_LIMITER_ROLE = "RATE_LIMITER_ROLE"
}

export interface ContractAddresses {
    registry: string;
    auditLog: string;
    accessControl: string;
}

export interface NetworkConfig {
    chainId: number;
    rpcUrl: string;
    contracts: ContractAddresses;
}

export interface ActionData {
    actionId: string;
    agentId: string;
    toolId: string;
    input: any;
    output: any;
    metadata?: Record<string, any>;
}

export interface AuditEvent {
    type: string;
    timestamp: number;
    data: any;
    txHash?: string;
    blockNumber?: number;
}

export interface IndexerConfig {
    batchSize: number;
    maxBatchSize: number;
    commitInterval: number;
    ipfsGateway: string;
}

export interface OracleConfig {
    minConfirmations: number;
    maxRetries: number;
    retryDelay: number;
    timeout: number;
}

export interface DashboardConfig {
    port: number;
    cors: boolean;
    rateLimit: number;
    auth: boolean;
}