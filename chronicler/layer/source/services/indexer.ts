import { createClient } from '@supabase/supabase-js';
import { ethers } from 'ethers';
import { create } from 'ipfs-http-client';
import { v4 as uuidv4 } from 'uuid';
import { ChroniclerAccessControl } from '../contracts/ChroniclerAccessControl';
import { ChroniclerAuditLog } from '../contracts/ChroniclerAuditLog';
import { ChroniclerRegistry } from '../contracts/ChroniclerRegistry';
import {
    AuditEvent,
    IndexerConfig
} from '../types';

export class IndexerService {
    private registry: ChroniclerRegistry;
    private auditLog: ChroniclerAuditLog;
    private accessControl: ChroniclerAccessControl;
    private supabase: any;
    private ipfs: any;
    private config: IndexerConfig;
    private isRunning: boolean = false;

    constructor(
        provider: ethers.Provider,
        registry: ChroniclerRegistry,
        auditLog: ChroniclerAuditLog,
        accessControl: ChroniclerAccessControl,
        supabaseUrl: string,
        supabaseKey: string,
        config: IndexerConfig
    ) {
        this.registry = registry;
        this.auditLog = auditLog;
        this.accessControl = accessControl;
        this.supabase = createClient(supabaseUrl, supabaseKey);
        this.ipfs = create({ url: config.ipfsGateway });
        this.config = config;
    }

    async start(): Promise<void> {
        if (this.isRunning) {
            throw new Error('Indexer is already running');
        }

        this.isRunning = true;
        console.log('Starting Chronicler Indexer...');

        // Set up event listeners
        this.setupEventListeners();

        // Start batch processing
        this.startBatchProcessing();

        console.log('Chronicler Indexer started successfully');
    }

    async stop(): Promise<void> {
        this.isRunning = false;
        console.log('Chronicler Indexer stopped');
    }

    private setupEventListeners(): void {
        // Registry events
        this.registry.onAgentRegistered(async (agentId, operator, metadataURI) => {
            await this.handleAgentRegistered(agentId, operator, metadataURI);
        });

        this.registry.onToolRegistered(async (toolId, name, riskLevel, metadataURI) => {
            await this.handleToolRegistered(toolId, name, riskLevel, metadataURI);
        });

        this.registry.onCategoryRegistered(async (categoryId, name, riskMultiplier) => {
            await this.handleCategoryRegistered(categoryId, name, riskMultiplier);
        });

        // Audit log events
        this.auditLog.onActionLogged(async (actionIndex, agentId, toolId, actionId, status, gasUsed) => {
            await this.handleActionLogged(actionIndex, agentId, toolId, actionId, status, gasUsed);
        });

        this.auditLog.onBatchCommitted(async (batchId, merkleRoot, startIndex, endIndex, ipfsHash, actionCount) => {
            await this.handleBatchCommitted(batchId, merkleRoot, startIndex, endIndex, ipfsHash, actionCount);
        });

        // Access control events
        this.accessControl.onPolicyCreated(async (policyId, dailyLimit, maxGas, maxRisk) => {
            await this.handlePolicyCreated(policyId, dailyLimit, maxGas, maxRisk);
        });

        this.accessControl.onPolicyAssigned(async (agentId, policyId, isAgent) => {
            await this.handlePolicyAssigned(agentId, policyId, isAgent);
        });
    }

    private async handleAgentRegistered(agentId: string, operator: string, metadataURI: string): Promise<void> {
        try {
            const agent = await this.registry.getAgent(agentId);

            const event: AuditEvent = {
                type: 'AgentRegistered',
                timestamp: Date.now(),
                data: {
                    agentId,
                    operator,
                    metadataURI,
                    agent
                }
            };

            await this.storeEvent(event);
            console.log(`Agent registered: ${agentId}`);
        } catch (error) {
            console.error('Error handling agent registration:', error);
        }
    }

    private async handleToolRegistered(toolId: string, name: string, riskLevel: number, metadataURI: string): Promise<void> {
        try {
            const tool = await this.registry.getTool(toolId);

            const event: AuditEvent = {
                type: 'ToolRegistered',
                timestamp: Date.now(),
                data: {
                    toolId,
                    name,
                    riskLevel,
                    metadataURI,
                    tool
                }
            };

            await this.storeEvent(event);
            console.log(`Tool registered: ${toolId}`);
        } catch (error) {
            console.error('Error handling tool registration:', error);
        }
    }

    private async handleCategoryRegistered(categoryId: string, name: string, riskMultiplier: number): Promise<void> {
        try {
            const category = await this.registry.getCategory(categoryId);

            const event: AuditEvent = {
                type: 'CategoryRegistered',
                timestamp: Date.now(),
                data: {
                    categoryId,
                    name,
                    riskMultiplier,
                    category
                }
            };

            await this.storeEvent(event);
            console.log(`Category registered: ${categoryId}`);
        } catch (error) {
            console.error('Error handling category registration:', error);
        }
    }

    private async handleActionLogged(
        actionIndex: number,
        agentId: string,
        toolId: string,
        actionId: string,
        status: number,
        gasUsed: number
    ): Promise<void> {
        try {
            const actionLog = await this.auditLog.getActionLog(actionIndex);

            const event: AuditEvent = {
                type: 'ActionLogged',
                timestamp: Date.now(),
                data: {
                    actionIndex,
                    agentId,
                    toolId,
                    actionId,
                    status,
                    gasUsed,
                    actionLog
                }
            };

            await this.storeEvent(event);
            console.log(`Action logged: ${actionId}`);
        } catch (error) {
            console.error('Error handling action log:', error);
        }
    }

    private async handleBatchCommitted(
        batchId: number,
        merkleRoot: string,
        startIndex: number,
        endIndex: number,
        ipfsHash: string,
        actionCount: number
    ): Promise<void> {
        try {
            const batchCommitment = await this.auditLog.getBatchCommitment(batchId);

            const event: AuditEvent = {
                type: 'BatchCommitted',
                timestamp: Date.now(),
                data: {
                    batchId,
                    merkleRoot,
                    startIndex,
                    endIndex,
                    ipfsHash,
                    actionCount,
                    batchCommitment
                }
            };

            await this.storeEvent(event);
            console.log(`Batch committed: ${batchId}`);
        } catch (error) {
            console.error('Error handling batch commit:', error);
        }
    }

    private async handlePolicyCreated(policyId: number, dailyLimit: number, maxGas: number, maxRisk: number): Promise<void> {
        try {
            const policy = await this.accessControl.getPolicy(policyId);

            const event: AuditEvent = {
                type: 'PolicyCreated',
                timestamp: Date.now(),
                data: {
                    policyId,
                    dailyLimit,
                    maxGas,
                    maxRisk,
                    policy
                }
            };

            await this.storeEvent(event);
            console.log(`Policy created: ${policyId}`);
        } catch (error) {
            console.error('Error handling policy creation:', error);
        }
    }

    private async handlePolicyAssigned(agentId: string, policyId: number, isAgent: boolean): Promise<void> {
        try {
            const event: AuditEvent = {
                type: 'PolicyAssigned',
                timestamp: Date.now(),
                data: {
                    agentId,
                    policyId,
                    isAgent
                }
            };

            await this.storeEvent(event);
            console.log(`Policy assigned: ${policyId} to ${isAgent ? 'agent' : 'tool'} ${agentId}`);
        } catch (error) {
            console.error('Error handling policy assignment:', error);
        }
    }

    private async storeEvent(event: AuditEvent): Promise<void> {
        try {
            const { error } = await this.supabase
                .from('audit_events')
                .insert({
                    id: uuidv4(),
                    type: event.type,
                    timestamp: new Date(event.timestamp).toISOString(),
                    data: event.data,
                    tx_hash: event.txHash,
                    block_number: event.blockNumber
                });

            if (error) {
                throw error;
            }
        } catch (error) {
            console.error('Error storing event:', error);
            throw error;
        }
    }

    private startBatchProcessing(): void {
        setInterval(async () => {
            if (!this.isRunning) return;

            try {
                const pendingCount = await this.auditLog.getPendingActionsCount();

                if (pendingCount >= this.config.batchSize) {
                    await this.processBatch();
                }
            } catch (error) {
                console.error('Error in batch processing:', error);
            }
        }, this.config.commitInterval);
    }

    private async processBatch(): Promise<void> {
        try {
            // Get pending actions
            const pendingCount = await this.auditLog.getPendingActionsCount();

            if (pendingCount === 0) return;

            // Create IPFS hash for batch data
            const batchData = await this.getBatchData();
            const ipfsHash = await this.uploadToIPFS(batchData);

            // Commit batch
            await this.auditLog.commitBatch(ipfsHash);

            console.log(`Batch processed and committed to IPFS: ${ipfsHash}`);
        } catch (error) {
            console.error('Error processing batch:', error);
        }
    }

    private async getBatchData(): Promise<any> {
        // This would collect all pending action data
        // Implementation depends on specific requirements
        return {
            timestamp: Date.now(),
            actions: []
        };
    }

    private async uploadToIPFS(data: any): Promise<string> {
        try {
            const result = await this.ipfs.add(JSON.stringify(data));
            return result.path;
        } catch (error) {
            console.error('Error uploading to IPFS:', error);
            throw error;
        }
    }

    // Public methods for querying indexed data
    async getEventsByType(type: string, limit: number = 100): Promise<AuditEvent[]> {
        const { data, error } = await this.supabase
            .from('audit_events')
            .select('*')
            .eq('type', type)
            .order('timestamp', { ascending: false })
            .limit(limit);

        if (error) throw error;
        return data || [];
    }

    async getEventsByAgent(agentId: string, limit: number = 100): Promise<AuditEvent[]> {
        const { data, error } = await this.supabase
            .from('audit_events')
            .select('*')
            .contains('data', { agentId })
            .order('timestamp', { ascending: false })
            .limit(limit);

        if (error) throw error;
        return data || [];
    }

    async getEventsByTool(toolId: string, limit: number = 100): Promise<AuditEvent[]> {
        const { data, error } = await this.supabase
            .from('audit_events')
            .select('*')
            .contains('data', { toolId })
            .order('timestamp', { ascending: false })
            .limit(limit);

        if (error) throw error;
        return data || [];
    }
}
