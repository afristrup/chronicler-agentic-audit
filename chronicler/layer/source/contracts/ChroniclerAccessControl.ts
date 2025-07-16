import { ethers } from 'ethers';
import { AgentPolicy, Policy, RateLimit, ToolPolicy } from '../types';

export class ChroniclerAccessControl {
    private contract: ethers.Contract;
    private provider: ethers.Provider;
    private signer?: ethers.Signer;

    constructor(
        address: string,
        abi: any,
        provider: ethers.Provider,
        signer?: ethers.Signer
    ) {
        this.contract = new ethers.Contract(address, abi, signer || provider);
        this.provider = provider;
        this.signer = signer;
    }

    // Policy management functions
    async createPolicy(
        dailyLimit: number,
        maxGas: number,
        maxRisk: number,
        cooldownPeriod: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.createPolicy(dailyLimit, maxGas, maxRisk, cooldownPeriod);
    }

    async updatePolicy(
        policyId: number,
        dailyLimit: number,
        maxGas: number,
        maxRisk: number,
        cooldownPeriod: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updatePolicy(policyId, dailyLimit, maxGas, maxRisk, cooldownPeriod);
    }

    // Policy assignment functions
    async assignPolicyToAgent(
        agentId: string,
        policyId: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.assignPolicyToAgent(agentId, policyId);
    }

    async assignPolicyToTool(
        toolId: string,
        policyId: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.assignPolicyToTool(toolId, policyId);
    }

    async revokePolicyFromAgent(agentId: string): Promise<ethers.ContractTransaction> {
        return this.contract.revokePolicyFromAgent(agentId);
    }

    async revokePolicyFromTool(toolId: string): Promise<ethers.ContractTransaction> {
        return this.contract.revokePolicyFromTool(toolId);
    }

    // Access control functions
    async checkActionAllowed(
        agentId: string,
        toolId: string,
        gasUsed: number
    ): Promise<[boolean, string]> {
        return this.contract.checkActionAllowed(agentId, toolId, gasUsed);
    }

    async recordAction(
        agentId: string,
        gasUsed: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.recordAction(agentId, gasUsed);
    }

    // Query functions
    async getPolicy(policyId: number): Promise<Policy> {
        const policy = await this.contract.getPolicy(policyId);
        return {
            dailyLimit: Number(policy.dailyLimit),
            maxGas: Number(policy.maxGas),
            maxRisk: Number(policy.maxRisk),
            cooldownPeriod: Number(policy.cooldownPeriod),
            isActive: policy.isActive,
            createdAt: Number(policy.createdAt),
            updatedAt: Number(policy.updatedAt)
        };
    }

    async getAgentRateLimit(agentId: string): Promise<RateLimit> {
        const rateLimit = await this.contract.getAgentRateLimit(agentId);
        return {
            lastActionTime: Number(rateLimit.lastActionTime),
            dailyActionCount: Number(rateLimit.dailyActionCount),
            lastResetTime: Number(rateLimit.lastResetTime),
            totalActions: Number(rateLimit.totalActions),
            totalGasUsed: Number(rateLimit.totalGasUsed)
        };
    }

    async getAgentPolicy(agentId: string): Promise<AgentPolicy> {
        const policy = await this.contract.getAgentPolicy(agentId);
        return {
            agentId: policy.agentId,
            policyId: Number(policy.policyId),
            isActive: policy.isActive,
            assignedAt: Number(policy.assignedAt)
        };
    }

    async getToolPolicy(toolId: string): Promise<ToolPolicy> {
        const policy = await this.contract.getToolPolicy(toolId);
        return {
            toolId: policy.toolId,
            policyId: Number(policy.policyId),
            isActive: policy.isActive,
            assignedAt: Number(policy.assignedAt)
        };
    }

    async getPolicyCount(): Promise<number> {
        const count = await this.contract.getPolicyCount();
        return Number(count);
    }

    // Constants
    async getDefaultPolicyId(): Promise<number> {
        const id = await this.contract.DEFAULT_POLICY_ID();
        return Number(id);
    }

    // Admin functions
    async pause(): Promise<ethers.ContractTransaction> {
        return this.contract.pause();
    }

    async unpause(): Promise<ethers.ContractTransaction> {
        return this.contract.unpause();
    }

    // Role management
    async hasRole(role: string, account: string): Promise<boolean> {
        return this.contract.hasRole(role, account);
    }

    async grantRole(role: string, account: string): Promise<ethers.ContractTransaction> {
        return this.contract.grantRole(role, account);
    }

    async revokeRole(role: string, account: string): Promise<ethers.ContractTransaction> {
        return this.contract.revokeRole(role, account);
    }

    // Event listeners
    onPolicyCreated(
        callback: (policyId: number, dailyLimit: number, maxGas: number, maxRisk: number) => void
    ): void {
        this.contract.on('PolicyCreated', callback);
    }

    onPolicyUpdated(
        callback: (policyId: number, dailyLimit: number, maxGas: number, maxRisk: number) => void
    ): void {
        this.contract.on('PolicyUpdated', callback);
    }

    onPolicyAssigned(
        callback: (agentId: string, policyId: number, isAgent: boolean) => void
    ): void {
        this.contract.on('PolicyAssigned', callback);
    }

    onPolicyRevoked(
        callback: (agentId: string, policyId: number, isAgent: boolean) => void
    ): void {
        this.contract.on('PolicyRevoked', callback);
    }

    onRateLimitExceeded(
        callback: (agentId: string, limit: number, current: number) => void
    ): void {
        this.contract.on('RateLimitExceeded', callback);
    }

    onRiskLevelExceeded(
        callback: (agentId: string, toolId: string, risk: number, maxRisk: number) => void
    ): void {
        this.contract.on('RiskLevelExceeded', callback);
    }

    // Get contract instance
    getContract(): ethers.Contract {
        return this.contract;
    }

    // Get contract address
    getAddress(): string {
        return this.contract.target as string;
    }

    // Get registry address
    async getRegistry(): Promise<string> {
        return this.contract.registry();
    }

    // Provider-based functions
    async getBlockNumber(): Promise<number> {
        return await this.provider.getBlockNumber();
    }

    async getBlockTimestamp(): Promise<number> {
        const block = await this.provider.getBlock('latest');
        return block?.timestamp || 0;
    }

    async waitForTransaction(txHash: string, confirmations: number = 1): Promise<ethers.TransactionReceipt | null> {
        return await this.provider.waitForTransaction(txHash, confirmations);
    }

    // Enhanced policy functions
    async getActivePolicies(): Promise<Policy[]> {
        const policyCount = await this.getPolicyCount();
        const policies: Policy[] = [];

        for (let i = 1; i <= policyCount; i++) {
            try {
                const policy = await this.getPolicy(i);
                if (policy.isActive) {
                    policies.push(policy);
                }
            } catch (error) {
                // Skip invalid policies
                continue;
            }
        }

        return policies;
    }

    async getAgentPolicies(): Promise<Map<string, AgentPolicy>> {
        // This would require additional contract methods to get all agent policies
        // For now, return empty map - implement when contract supports it
        return new Map();
    }

    async getToolPolicies(): Promise<Map<string, ToolPolicy>> {
        // This would require additional contract methods to get all tool policies
        // For now, return empty map - implement when contract supports it
        return new Map();
    }

    // Rate limiting utilities
    async isRateLimitExceeded(agentId: string): Promise<boolean> {
        const rateLimit = await this.getAgentRateLimit(agentId);
        const policy = await this.getAgentPolicy(agentId);
        const agentPolicy = await this.getPolicy(policy.policyId);

        return rateLimit.dailyActionCount >= agentPolicy.dailyLimit;
    }

    async getRemainingActions(agentId: string): Promise<number> {
        const rateLimit = await this.getAgentRateLimit(agentId);
        const policy = await this.getAgentPolicy(agentId);
        const agentPolicy = await this.getPolicy(policy.policyId);

        return Math.max(0, agentPolicy.dailyLimit - rateLimit.dailyActionCount);
    }

    // Validation functions
    async validatePolicy(policyId: number): Promise<boolean> {
        try {
            const policy = await this.getPolicy(policyId);
            return policy.isActive;
        } catch (error) {
            return false;
        }
    }

    async validateAgentAccess(agentId: string, toolId: string): Promise<[boolean, string]> {
        try {
            const [isAllowed, reason] = await this.checkActionAllowed(agentId, toolId, 0);
            return [isAllowed, reason];
        } catch (error) {
            return [false, 'Validation failed'];
        }
    }
}