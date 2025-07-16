import { ethers } from 'ethers';
import { Agent, Category, Tool } from '../types';

export class ChroniclerRegistry {
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

    // Agent functions
    async registerAgent(
        agentId: string,
        operator: string,
        metadataURI: string
    ): Promise<ethers.ContractTransaction> {
        return this.contract.registerAgent(agentId, operator, metadataURI);
    }

    async updateAgentStatus(
        agentId: string,
        isActive: boolean
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateAgentStatus(agentId, isActive);
    }

    async updateAgentOperator(
        agentId: string,
        newOperator: string
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateAgentOperator(agentId, newOperator);
    }

    async updateAgentMetadata(
        agentId: string,
        metadataURI: string
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateAgentMetadata(agentId, metadataURI);
    }

    // Tool functions
    async registerTool(
        toolId: string,
        name: string,
        metadataURI: string,
        categoryId: string,
        riskLevel: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.registerTool(toolId, name, metadataURI, categoryId, riskLevel);
    }

    async updateToolStatus(
        toolId: string,
        isActive: boolean
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateToolStatus(toolId, isActive);
    }

    async updateToolRiskLevel(
        toolId: string,
        newRiskLevel: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateToolRiskLevel(toolId, newRiskLevel);
    }

    async updateToolMetadata(
        toolId: string,
        metadataURI: string
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateToolMetadata(toolId, metadataURI);
    }

    // Category functions
    async registerCategory(
        categoryId: string,
        name: string,
        description: string,
        riskMultiplier: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.registerCategory(categoryId, name, description, riskMultiplier);
    }

    async updateCategoryStatus(
        categoryId: string,
        isActive: boolean
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateCategoryStatus(categoryId, isActive);
    }

    async updateCategoryRiskMultiplier(
        categoryId: string,
        newMultiplier: number
    ): Promise<ethers.ContractTransaction> {
        return this.contract.updateCategoryRiskMultiplier(categoryId, newMultiplier);
    }

    // Query functions
    async getAgent(agentId: string): Promise<Agent> {
        const agent = await this.contract.getAgent(agentId);
        return {
            id: agent.id,
            operator: agent.operator,
            metadataURI: agent.metadataURI,
            isActive: agent.isActive,
            createdAt: Number(agent.createdAt),
            lastActionAt: Number(agent.lastActionAt),
            totalActions: Number(agent.totalActions)
        };
    }

    async getTool(toolId: string): Promise<Tool> {
        const tool = await this.contract.getTool(toolId);
        return {
            id: tool.id,
            name: tool.name,
            metadataURI: tool.metadataURI,
            categoryId: tool.categoryId,
            isActive: tool.isActive,
            riskLevel: Number(tool.riskLevel),
            usageCount: Number(tool.usageCount),
            lastUsedAt: Number(tool.lastUsedAt)
        };
    }

    async getCategory(categoryId: string): Promise<Category> {
        const category = await this.contract.getCategory(categoryId);
        return {
            id: category.id,
            name: category.name,
            description: category.description,
            isActive: category.isActive,
            riskMultiplier: Number(category.riskMultiplier)
        };
    }

    async isValidAgent(agentId: string): Promise<boolean> {
        return this.contract.isValidAgent(agentId);
    }

    async isValidTool(toolId: string): Promise<boolean> {
        return this.contract.isValidTool(toolId);
    }

    async isValidCategory(categoryId: string): Promise<boolean> {
        return this.contract.isValidCategory(categoryId);
    }

    // Statistics functions
    async incrementAgentActions(agentId: string): Promise<ethers.ContractTransaction> {
        return this.contract.incrementAgentActions(agentId);
    }

    async incrementToolUsage(toolId: string): Promise<ethers.ContractTransaction> {
        return this.contract.incrementToolUsage(toolId);
    }

    // Enumeration functions
    async getAllAgents(): Promise<string[]> {
        return this.contract.getAllAgents();
    }

    async getAllTools(): Promise<string[]> {
        return this.contract.getAllTools();
    }

    async getAllCategories(): Promise<string[]> {
        return this.contract.getAllCategories();
    }

    async getAgentCount(): Promise<number> {
        const count = await this.contract.getAgentCount();
        return Number(count);
    }

    async getToolCount(): Promise<number> {
        const count = await this.contract.getToolCount();
        return Number(count);
    }

    async getCategoryCount(): Promise<number> {
        const count = await this.contract.getCategoryCount();
        return Number(count);
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
    onAgentRegistered(
        callback: (agentId: string, operator: string, metadataURI: string) => void
    ): void {
        this.contract.on('AgentRegistered', callback);
    }

    onToolRegistered(
        callback: (toolId: string, name: string, riskLevel: number, metadataURI: string) => void
    ): void {
        this.contract.on('ToolRegistered', callback);
    }

    onCategoryRegistered(
        callback: (categoryId: string, name: string, riskMultiplier: number) => void
    ): void {
        this.contract.on('CategoryRegistered', callback);
    }

    // Get contract instance
    getContract(): ethers.Contract {
        return this.contract;
    }

    // Get contract address
    getAddress(): string {
        return this.contract.target as string;
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

    // Enhanced query functions
    async getActiveAgents(): Promise<Agent[]> {
        const agentIds = await this.getAllAgents();
        const agents: Agent[] = [];

        for (const agentId of agentIds) {
            try {
                const agent = await this.getAgent(agentId);
                if (agent.isActive) {
                    agents.push(agent);
                }
            } catch (error) {
                continue;
            }
        }

        return agents;
    }

    async getActiveTools(): Promise<Tool[]> {
        const toolIds = await this.getAllTools();
        const tools: Tool[] = [];

        for (const toolId of toolIds) {
            try {
                const tool = await this.getTool(toolId);
                if (tool.isActive) {
                    tools.push(tool);
                }
            } catch (error) {
                continue;
            }
        }

        return tools;
    }

    async getActiveCategories(): Promise<Category[]> {
        const categoryIds = await this.getAllCategories();
        const categories: Category[] = [];

        for (const categoryId of categoryIds) {
            try {
                const category = await this.getCategory(categoryId);
                if (category.isActive) {
                    categories.push(category);
                }
            } catch (error) {
                continue;
            }
        }

        return categories;
    }

    // Search and filter functions
    async getAgentsByOperator(operator: string): Promise<Agent[]> {
        const agentIds = await this.getAllAgents();
        const agents: Agent[] = [];

        for (const agentId of agentIds) {
            try {
                const agent = await this.getAgent(agentId);
                if (agent.operator.toLowerCase() === operator.toLowerCase()) {
                    agents.push(agent);
                }
            } catch (error) {
                continue;
            }
        }

        return agents;
    }

    async getToolsByCategory(categoryId: string): Promise<Tool[]> {
        const toolIds = await this.getAllTools();
        const tools: Tool[] = [];

        for (const toolId of toolIds) {
            try {
                const tool = await this.getTool(toolId);
                if (tool.categoryId === categoryId) {
                    tools.push(tool);
                }
            } catch (error) {
                continue;
            }
        }

        return tools;
    }

    async getToolsByRiskLevel(minRisk: number, maxRisk: number): Promise<Tool[]> {
        const toolIds = await this.getAllTools();
        const tools: Tool[] = [];

        for (const toolId of toolIds) {
            try {
                const tool = await this.getTool(toolId);
                if (tool.riskLevel >= minRisk && tool.riskLevel <= maxRisk) {
                    tools.push(tool);
                }
            } catch (error) {
                continue;
            }
        }

        return tools;
    }

    // Statistics and analytics
    async getRegistryStats(): Promise<{
        totalAgents: number;
        activeAgents: number;
        totalTools: number;
        activeTools: number;
        totalCategories: number;
        activeCategories: number;
        totalActions: number;
    }> {
        const totalAgents = await this.getAgentCount();
        const totalTools = await this.getToolCount();
        const totalCategories = await this.getCategoryCount();

        const activeAgents = (await this.getActiveAgents()).length;
        const activeTools = (await this.getActiveTools()).length;
        const activeCategories = (await this.getActiveCategories()).length;

        // Calculate total actions across all agents
        let totalActions = 0;
        const agents = await this.getActiveAgents();
        for (const agent of agents) {
            totalActions += agent.totalActions;
        }

        return {
            totalAgents,
            activeAgents,
            totalTools,
            activeTools,
            totalCategories,
            activeCategories,
            totalActions
        };
    }

    // Validation functions
    async validateAgent(agentId: string): Promise<[boolean, string]> {
        try {
            const isValid = await this.isValidAgent(agentId);
            if (!isValid) {
                return [false, 'Agent not found or inactive'];
            }

            const agent = await this.getAgent(agentId);
            if (!agent.isActive) {
                return [false, 'Agent is inactive'];
            }

            return [true, 'Agent is valid'];
        } catch (error) {
            return [false, 'Validation failed'];
        }
    }

    async validateTool(toolId: string): Promise<[boolean, string]> {
        try {
            const isValid = await this.isValidTool(toolId);
            if (!isValid) {
                return [false, 'Tool not found or inactive'];
            }

            const tool = await this.getTool(toolId);
            if (!tool.isActive) {
                return [false, 'Tool is inactive'];
            }

            return [true, 'Tool is valid'];
        } catch (error) {
            return [false, 'Validation failed'];
        }
    }

    async validateCategory(categoryId: string): Promise<[boolean, string]> {
        try {
            const isValid = await this.isValidCategory(categoryId);
            if (!isValid) {
                return [false, 'Category not found or inactive'];
            }

            const category = await this.getCategory(categoryId);
            if (!category.isActive) {
                return [false, 'Category is inactive'];
            }

            return [true, 'Category is valid'];
        } catch (error) {
            return [false, 'Validation failed'];
        }
    }

    // Signer-based functions
    async getSignerAddress(): Promise<string | null> {
        if (!this.signer) {
            return null;
        }
        return await this.signer.getAddress();
    }

    async hasSigner(): Promise<boolean> {
        return this.signer !== undefined;
    }

    async signMessage(message: string): Promise<string> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return await this.signer.signMessage(message);
    }

    async signTypedData(domain: any, types: any, value: any): Promise<string> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return await this.signer.signTypedData(domain, types, value);
    }

    // Enhanced transaction functions with signer
    async registerAgentWithSignature(
        agentId: string,
        operator: string,
        metadataURI: string,
        signature: string
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.registerAgent(agentId, operator, metadataURI, { signature });
    }

    async registerToolWithSignature(
        toolId: string,
        name: string,
        metadataURI: string,
        categoryId: string,
        riskLevel: number,
        signature: string
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.registerTool(toolId, name, metadataURI, categoryId, riskLevel, { signature });
    }

    // Batch operations with signer
    async batchRegisterAgents(agents: Array<{ agentId: string, operator: string, metadataURI: string }>): Promise<ethers.ContractTransaction[]> {
        if (!this.signer) {
            throw new Error('No signer available');
        }

        const transactions: ethers.ContractTransaction[] = [];
        for (const agent of agents) {
            const tx = await this.registerAgent(agent.agentId, agent.operator, agent.metadataURI);
            transactions.push(tx);
        }
        return transactions;
    }

    async batchRegisterTools(tools: Array<{ toolId: string, name: string, metadataURI: string, categoryId: string, riskLevel: number }>): Promise<ethers.ContractTransaction[]> {
        if (!this.signer) {
            throw new Error('No signer available');
        }

        const transactions: ethers.ContractTransaction[] = [];
        for (const tool of tools) {
            const tx = await this.registerTool(tool.toolId, tool.name, tool.metadataURI, tool.categoryId, tool.riskLevel);
            transactions.push(tx);
        }
        return transactions;
    }

    // Gas estimation functions
    async estimateRegisterAgentGas(agentId: string, operator: string, metadataURI: string): Promise<bigint> {
        return await this.contract.registerAgent.estimateGas(agentId, operator, metadataURI);
    }

    async estimateRegisterToolGas(toolId: string, name: string, metadataURI: string, categoryId: string, riskLevel: number): Promise<bigint> {
        return await this.contract.registerTool.estimateGas(toolId, name, metadataURI, categoryId, riskLevel);
    }

    // Transaction with custom gas
    async registerAgentWithGasLimit(
        agentId: string,
        operator: string,
        metadataURI: string,
        gasLimit: bigint
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.registerAgent(agentId, operator, metadataURI, { gasLimit });
    }

    async registerToolWithGasLimit(
        toolId: string,
        name: string,
        metadataURI: string,
        categoryId: string,
        riskLevel: number,
        gasLimit: bigint
    ): Promise<ethers.ContractTransaction> {
        if (!this.signer) {
            throw new Error('No signer available');
        }
        return this.contract.registerTool(toolId, name, metadataURI, categoryId, riskLevel, { gasLimit });
    }
}