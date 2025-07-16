import { config } from 'dotenv';
import { ethers } from 'ethers';
import { ChroniclerAccessControl } from './contracts/ChroniclerAccessControl';
import { ChroniclerAuditLog } from './contracts/ChroniclerAuditLog';
import { ChroniclerRegistry } from './contracts/ChroniclerRegistry';
import { DashboardService } from './services/dashboard';
import { IndexerService } from './services/indexer';
import { OracleService } from './services/oracle';
import {
    DashboardConfig,
    IndexerConfig,
    NetworkConfig,
    OracleConfig
} from './types';

// Load environment variables
config();

export class ChroniclerLayer {
    private provider: ethers.Provider;
    private registry: ChroniclerRegistry;
    private auditLog: ChroniclerAuditLog;
    private accessControl: ChroniclerAccessControl;
    private indexer: IndexerService;
    private oracle: OracleService;
    private dashboard: DashboardService;
    private networkConfig: NetworkConfig;
    private isRunning: boolean = false;

    constructor(networkConfig: NetworkConfig) {
        this.networkConfig = networkConfig;
        this.initializeServices();
    }

    private initializeServices(): void {
        // Initialize provider
        this.provider = new ethers.JsonRpcProvider(this.networkConfig.rpcUrl);

        // Load contract ABIs (these would be compiled from Solidity)
        const registryAbi = this.loadContractAbi('ChroniclerRegistry');
        const auditLogAbi = this.loadContractAbi('ChroniclerAuditLog');
        const accessControlAbi = this.loadContractAbi('ChroniclerAccessControl');

        // Initialize contract interfaces
        this.registry = new ChroniclerRegistry(
            this.networkConfig.contracts.registry,
            registryAbi,
            this.provider
        );

        this.auditLog = new ChroniclerAuditLog(
            this.networkConfig.contracts.auditLog,
            auditLogAbi,
            this.provider
        );

        this.accessControl = new ChroniclerAccessControl(
            this.networkConfig.contracts.accessControl,
            accessControlAbi,
            this.provider
        );

        // Initialize services
        const indexerConfig: IndexerConfig = {
            batchSize: 100,
            maxBatchSize: 1000,
            commitInterval: 30000, // 30 seconds
            ipfsGateway: process.env.IPFS_GATEWAY || 'https://ipfs.io'
        };

        const oracleConfig: OracleConfig = {
            minConfirmations: 3,
            maxRetries: 5,
            retryDelay: 1000,
            timeout: 30000
        };

        const dashboardConfig: DashboardConfig = {
            port: parseInt(process.env.DASHBOARD_PORT || '3000'),
            cors: true,
            rateLimit: 100,
            auth: false
        };

        this.indexer = new IndexerService(
            this.provider,
            this.registry,
            this.auditLog,
            this.accessControl,
            process.env.SUPABASE_URL!,
            process.env.SUPABASE_KEY!,
            indexerConfig
        );

        this.oracle = new OracleService(
            this.provider,
            this.auditLog,
            this.accessControl,
            process.env.SUPABASE_URL!,
            process.env.SUPABASE_KEY!,
            oracleConfig
        );

        this.dashboard = new DashboardService(
            this.registry,
            this.auditLog,
            this.accessControl,
            process.env.SUPABASE_URL!,
            process.env.SUPABASE_KEY!,
            dashboardConfig
        );
    }

    private loadContractAbi(contractName: string): any {
        // In a real implementation, this would load compiled ABI files
        // For now, we'll return a placeholder
        return [];
    }

    async start(): Promise<void> {
        if (this.isRunning) {
            throw new Error('Chronicler Layer is already running');
        }

        console.log('Starting Chronicler Layer...');

        try {
            // Start services in order
            await this.indexer.start();
            await this.oracle.start();
            await this.dashboard.start();

            this.isRunning = true;
            console.log('Chronicler Layer started successfully');
        } catch (error) {
            console.error('Failed to start Chronicler Layer:', error);
            throw error;
        }
    }

    async stop(): Promise<void> {
        if (!this.isRunning) {
            return;
        }

        console.log('Stopping Chronicler Layer...');

        try {
            // Stop services in reverse order
            await this.dashboard.stop();
            await this.oracle.stop();
            await this.indexer.stop();

            this.isRunning = false;
            console.log('Chronicler Layer stopped successfully');
        } catch (error) {
            console.error('Error stopping Chronicler Layer:', error);
            throw error;
        }
    }

    // Public getters for accessing services
    getRegistry(): ChroniclerRegistry {
        return this.registry;
    }

    getAuditLog(): ChroniclerAuditLog {
        return this.auditLog;
    }

    getAccessControl(): ChroniclerAccessControl {
        return this.accessControl;
    }

    getIndexer(): IndexerService {
        return this.indexer;
    }

    getOracle(): OracleService {
        return this.oracle;
    }

    getDashboard(): DashboardService {
        return this.dashboard;
    }

    isServiceRunning(): boolean {
        return this.isRunning;
    }
}

// Main execution function
async function main(): Promise<void> {
    try {
        // Network configuration
        const networkConfig: NetworkConfig = {
            chainId: parseInt(process.env.CHAIN_ID || '1'),
            rpcUrl: process.env.RPC_URL || 'http://localhost:8545',
            contracts: {
                registry: process.env.REGISTRY_ADDRESS || '',
                auditLog: process.env.AUDIT_LOG_ADDRESS || '',
                accessControl: process.env.ACCESS_CONTROL_ADDRESS || ''
            }
        };

        // Validate configuration
        if (!networkConfig.contracts.registry ||
            !networkConfig.contracts.auditLog ||
            !networkConfig.contracts.accessControl) {
            throw new Error('Contract addresses not configured');
        }

        if (!process.env.SUPABASE_URL || !process.env.SUPABASE_KEY) {
            throw new Error('Supabase configuration not found');
        }

        // Create and start the layer
        const layer = new ChroniclerLayer(networkConfig);
        await layer.start();

        // Handle graceful shutdown
        process.on('SIGINT', async () => {
            console.log('Received SIGINT, shutting down gracefully...');
            await layer.stop();
            process.exit(0);
        });

        process.on('SIGTERM', async () => {
            console.log('Received SIGTERM, shutting down gracefully...');
            await layer.stop();
            process.exit(0);
        });

    } catch (error) {
        console.error('Failed to start Chronicler Layer:', error);
        process.exit(1);
    }
}

// Run if this is the main module
if (require.main === module) {
    main();
}
