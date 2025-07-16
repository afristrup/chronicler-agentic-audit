import { ethers } from 'ethers';
import { ActionStatus, Agent, Category, Tool } from '../../source/types';

export class TestUtils {
    static createMockProvider(): ethers.Provider {
        return new ethers.JsonRpcProvider('http://localhost:8545');
    }

    static createMockSigner(): ethers.Signer {
        const provider = this.createMockProvider();
        return new ethers.Wallet(ethers.Wallet.createRandom().privateKey, provider);
    }

    static generateRandomAddress(): string {
        return ethers.Wallet.createRandom().address;
    }

    static generateRandomBytes32(): string {
        return ethers.hexlify(ethers.randomBytes(32));
    }

    static generateRandomString(length: number = 10): string {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    static createMockAgent(overrides: Partial<Agent> = {}): Agent {
        return {
            id: this.generateRandomBytes32(),
            operator: this.generateRandomAddress(),
            metadataURI: `ipfs://${this.generateRandomString(46)}`,
            isActive: true,
            createdAt: Date.now(),
            lastActionAt: 0,
            totalActions: 0,
            ...overrides
        };
    }

    static createMockTool(overrides: Partial<Tool> = {}): Tool {
        return {
            id: this.generateRandomBytes32(),
            name: this.generateRandomString(10),
            metadataURI: `ipfs://${this.generateRandomString(46)}`,
            categoryId: this.generateRandomBytes32(),
            isActive: true,
            riskLevel: Math.floor(Math.random() * 100),
            usageCount: 0,
            lastUsedAt: 0,
            ...overrides
        };
    }

    static createMockCategory(overrides: Partial<Category> = {}): Category {
        return {
            id: this.generateRandomBytes32(),
            name: this.generateRandomString(10),
            description: this.generateRandomString(50),
            isActive: true,
            riskMultiplier: Math.floor(Math.random() * 100) + 1,
            ...overrides
        };
    }

    static createMockActionData(): any {
        return {
            actionId: this.generateRandomBytes32(),
            agentId: this.generateRandomBytes32(),
            toolId: this.generateRandomBytes32(),
            input: { test: 'data' },
            output: { result: 'success' },
            metadata: { timestamp: Date.now() }
        };
    }

    static createMockAuditEvent(type: string, data: any = {}): any {
        return {
            type,
            timestamp: Date.now(),
            data,
            txHash: this.generateRandomBytes32(),
            blockNumber: Math.floor(Math.random() * 1000000)
        };
    }

    static async wait(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    static createMockContractAbi(): any[] {
        return [
            {
                inputs: [],
                name: 'testFunction',
                outputs: [{ type: 'bool' }],
                stateMutability: 'view',
                type: 'function'
            }
        ];
    }

    static createMockNetworkConfig(): any {
        return {
            chainId: 1,
            rpcUrl: 'http://localhost:8545',
            contracts: {
                registry: this.generateRandomAddress(),
                auditLog: this.generateRandomAddress(),
                accessControl: this.generateRandomAddress()
            }
        };
    }

    static createMockIndexerConfig(): any {
        return {
            batchSize: 100,
            maxBatchSize: 1000,
            commitInterval: 30000,
            ipfsGateway: 'https://ipfs.io'
        };
    }

    static createMockOracleConfig(): any {
        return {
            minConfirmations: 3,
            maxRetries: 5,
            retryDelay: 1000,
            timeout: 30000
        };
    }

    static createMockDashboardConfig(): any {
        return {
            port: 3000,
            cors: true,
            rateLimit: 100,
            auth: false
        };
    }

    static mockSupabaseClient(): any {
        return {
            from: () => this.mockSupabaseClient(),
            select: () => this.mockSupabaseClient(),
            insert: () => this.mockSupabaseClient(),
            update: () => this.mockSupabaseClient(),
            eq: () => this.mockSupabaseClient(),
            contains: () => this.mockSupabaseClient(),
            order: () => this.mockSupabaseClient(),
            limit: () => this.mockSupabaseClient(),
            single: () => this.mockSupabaseClient(),
            data: [],
            error: null
        };
    }

    static mockIpfsClient(): any {
        return {
            add: async () => ({ path: 'QmTestHash' }),
            cat: async () => Buffer.from('{"test": "data"}')
        };
    }

    static createMockExpressApp(): any {
        return {
            use: () => { },
            get: () => { },
            post: () => { },
            put: () => { },
            delete: () => { },
            listen: () => ({
                close: () => { }
            })
        };
    }

    static createMockRequest(params: any = {}, query: any = {}, body: any = {}): any {
        return {
            params,
            query,
            body,
            ip: '127.0.0.1'
        };
    }

    static createMockResponse(): any {
        const res: any = {};
        res.status = () => res;
        res.json = () => res;
        res.send = () => res;
        return res;
    }

    static createMockNextFunction(): any {
        return () => { };
    }

    static validateAgent(agent: Agent): boolean {
        return (
            Boolean(agent.id) &&
            Boolean(agent.operator) &&
            Boolean(agent.metadataURI) &&
            typeof agent.isActive === 'boolean' &&
            typeof agent.createdAt === 'number' &&
            typeof agent.lastActionAt === 'number' &&
            typeof agent.totalActions === 'number'
        );
    }

    static validateTool(tool: Tool): boolean {
        return (
            Boolean(tool.id) &&
            Boolean(tool.name) &&
            Boolean(tool.metadataURI) &&
            Boolean(tool.categoryId) &&
            typeof tool.isActive === 'boolean' &&
            typeof tool.riskLevel === 'number' &&
            tool.riskLevel >= 0 &&
            tool.riskLevel <= 100 &&
            typeof tool.usageCount === 'number' &&
            typeof tool.lastUsedAt === 'number'
        );
    }

    static validateCategory(category: Category): boolean {
        return (
            Boolean(category.id) &&
            Boolean(category.name) &&
            Boolean(category.description) &&
            typeof category.isActive === 'boolean' &&
            typeof category.riskMultiplier === 'number' &&
            category.riskMultiplier > 0 &&
            category.riskMultiplier <= 100
        );
    }

    static validateActionLog(actionLog: any): boolean {
        return (
            actionLog.actionId &&
            actionLog.agentId &&
            actionLog.toolId &&
            actionLog.dataHash &&
            typeof actionLog.timestamp === 'number' &&
            Object.values(ActionStatus).includes(actionLog.status) &&
            typeof actionLog.gasUsed === 'number' &&
            typeof actionLog.batchId === 'number'
        );
    }

    static validateBatchCommitment(batch: any): boolean {
        return (
            batch.merkleRoot &&
            typeof batch.startIndex === 'number' &&
            typeof batch.endIndex === 'number' &&
            typeof batch.timestamp === 'number' &&
            batch.ipfsHash &&
            typeof batch.actionCount === 'number' &&
            typeof batch.isCommitted === 'boolean'
        );
    }

    static validateAuditEvent(event: any): boolean {
        return (
            event.type &&
            typeof event.timestamp === 'number' &&
            event.data &&
            (event.txHash === undefined || typeof event.txHash === 'string') &&
            (event.blockNumber === undefined || typeof event.blockNumber === 'number')
        );
    }
}