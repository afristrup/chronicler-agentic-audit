import { createClient } from '@supabase/supabase-js';
import compression from 'compression';
import cors from 'cors';
import express from 'express';
import helmet from 'helmet';
import { ChroniclerAccessControl } from '../contracts/ChroniclerAccessControl';
import { ChroniclerAuditLog } from '../contracts/ChroniclerAuditLog';
import { ChroniclerRegistry } from '../contracts/ChroniclerRegistry';
import {
    ActionLog,
    Agent,
    BatchCommitment,
    Category,
    DashboardConfig,
    Policy,
    Tool
} from '../types';

export class DashboardService {
    private app: express.Application;
    private registry: ChroniclerRegistry;
    private auditLog: ChroniclerAuditLog;
    private accessControl: ChroniclerAccessControl;
    private supabase: any;
    private config: DashboardConfig;
    private server: any;

    constructor(
        registry: ChroniclerRegistry,
        auditLog: ChroniclerAuditLog,
        accessControl: ChroniclerAccessControl,
        supabaseUrl: string,
        supabaseKey: string,
        config: DashboardConfig
    ) {
        this.registry = registry;
        this.auditLog = auditLog;
        this.accessControl = accessControl;
        this.supabase = createClient(supabaseUrl, supabaseKey);
        this.config = config;

        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
    }

    private setupMiddleware(): void {
        // Security middleware
        this.app.use(helmet());

        // CORS
        if (this.config.cors) {
            this.app.use(cors());
        }

        // Compression
        this.app.use(compression());

        // Body parsing
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true }));

        // Rate limiting
        if (this.config.rateLimit > 0) {
            this.app.use(this.rateLimitMiddleware());
        }
    }

    private rateLimitMiddleware() {
        const requests = new Map();

        return (req: express.Request, res: express.Response, next: express.NextFunction) => {
            const ip = req.ip;
            const now = Date.now();
            const windowMs = 60000; // 1 minute

            if (!requests.has(ip)) {
                requests.set(ip, []);
            }

            const userRequests = requests.get(ip);
            const validRequests = userRequests.filter((timestamp: number) => now - timestamp < windowMs);

            if (validRequests.length >= this.config.rateLimit) {
                return res.status(429).json({ error: 'Rate limit exceeded' });
            }

            validRequests.push(now);
            requests.set(ip, validRequests);
            next();
        };
    }

    private setupRoutes(): void {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ status: 'healthy', timestamp: new Date().toISOString() });
        });

        // Registry routes
        this.app.get('/api/agents', this.getAgents.bind(this));
        this.app.get('/api/agents/:id', this.getAgent.bind(this));
        this.app.get('/api/tools', this.getTools.bind(this));
        this.app.get('/api/tools/:id', this.getTool.bind(this));
        this.app.get('/api/categories', this.getCategories.bind(this));
        this.app.get('/api/categories/:id', this.getCategory.bind(this));

        // Audit log routes
        this.app.get('/api/actions', this.getActions.bind(this));
        this.app.get('/api/actions/:id', this.getAction.bind(this));
        this.app.get('/api/batches', this.getBatches.bind(this));
        this.app.get('/api/batches/:id', this.getBatch.bind(this));

        // Access control routes
        this.app.get('/api/policies', this.getPolicies.bind(this));
        this.app.get('/api/policies/:id', this.getPolicy.bind(this));
        this.app.get('/api/rate-limits/:agentId', this.getRateLimit.bind(this));

        // Events routes
        this.app.get('/api/events', this.getEvents.bind(this));
        this.app.get('/api/events/:type', this.getEventsByType.bind(this));

        // Analytics routes
        this.app.get('/api/analytics/overview', this.getAnalyticsOverview.bind(this));
        this.app.get('/api/analytics/agents/:agentId', this.getAgentAnalytics.bind(this));
        this.app.get('/api/analytics/tools/:toolId', this.getToolAnalytics.bind(this));

        // Compliance routes
        this.app.get('/api/compliance/report', this.getComplianceReport.bind(this));
        this.app.get('/api/compliance/agents/:agentId', this.getAgentCompliance.bind(this));

        // Error handling
        this.app.use(this.errorHandler.bind(this));
    }

    // Registry endpoints
    private async getAgents(req: express.Request, res: express.Response): Promise<void> {
        try {
            const agentIds = await this.registry.getAllAgents();
            const agents: Agent[] = [];

            for (const agentId of agentIds) {
                const agent = await this.registry.getAgent(agentId);
                agents.push(agent);
            }

            res.json(agents);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch agents' });
        }
    }

    private async getAgent(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const agent = await this.registry.getAgent(id);
            res.json(agent);
        } catch (error) {
            res.status(404).json({ error: 'Agent not found' });
        }
    }

    private async getTools(req: express.Request, res: express.Response): Promise<void> {
        try {
            const toolIds = await this.registry.getAllTools();
            const tools: Tool[] = [];

            for (const toolId of toolIds) {
                const tool = await this.registry.getTool(toolId);
                tools.push(tool);
            }

            res.json(tools);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch tools' });
        }
    }

    private async getTool(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const tool = await this.registry.getTool(id);
            res.json(tool);
        } catch (error) {
            res.status(404).json({ error: 'Tool not found' });
        }
    }

    private async getCategories(req: express.Request, res: express.Response): Promise<void> {
        try {
            const categoryIds = await this.registry.getAllCategories();
            const categories: Category[] = [];

            for (const categoryId of categoryIds) {
                const category = await this.registry.getCategory(categoryId);
                categories.push(category);
            }

            res.json(categories);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch categories' });
        }
    }

    private async getCategory(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const category = await this.registry.getCategory(id);
            res.json(category);
        } catch (error) {
            res.status(404).json({ error: 'Category not found' });
        }
    }

    // Audit log endpoints
    private async getActions(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { limit = 100, offset = 0 } = req.query;
            const actionCounter = await this.auditLog.getActionCounter();

            const actions: ActionLog[] = [];
            const startIndex = Math.max(0, actionCounter - Number(limit) - Number(offset));
            const endIndex = Math.max(0, actionCounter - Number(offset));

            for (let i = startIndex; i < endIndex; i++) {
                const action = await this.auditLog.getActionLog(i);
                actions.push(action);
            }

            res.json({
                actions,
                total: actionCounter,
                limit: Number(limit),
                offset: Number(offset)
            });
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch actions' });
        }
    }

    private async getAction(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const action = await this.auditLog.getActionLog(Number(id));
            res.json(action);
        } catch (error) {
            res.status(404).json({ error: 'Action not found' });
        }
    }

    private async getBatches(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { limit = 50 } = req.query;
            const batchCounter = await this.auditLog.getBatchCounter();

            const batches: BatchCommitment[] = [];
            const startIndex = Math.max(0, batchCounter - Number(limit));

            for (let i = startIndex; i < batchCounter; i++) {
                const batch = await this.auditLog.getBatchCommitment(i);
                batches.push(batch);
            }

            res.json({
                batches,
                total: batchCounter,
                limit: Number(limit)
            });
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch batches' });
        }
    }

    private async getBatch(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const batch = await this.auditLog.getBatchCommitment(Number(id));
            res.json(batch);
        } catch (error) {
            res.status(404).json({ error: 'Batch not found' });
        }
    }

    // Access control endpoints
    private async getPolicies(req: express.Request, res: express.Response): Promise<void> {
        try {
            const policyCount = await this.accessControl.getPolicyCount();
            const policies: Policy[] = [];

            for (let i = 1; i <= policyCount; i++) {
                const policy = await this.accessControl.getPolicy(i);
                policies.push(policy);
            }

            res.json(policies);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch policies' });
        }
    }

    private async getPolicy(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { id } = req.params;
            const policy = await this.accessControl.getPolicy(Number(id));
            res.json(policy);
        } catch (error) {
            res.status(404).json({ error: 'Policy not found' });
        }
    }

    private async getRateLimit(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { agentId } = req.params;
            const rateLimit = await this.accessControl.getAgentRateLimit(agentId);
            res.json(rateLimit);
        } catch (error) {
            res.status(404).json({ error: 'Rate limit not found' });
        }
    }

    // Events endpoints
    private async getEvents(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { limit = 100 } = req.query;
            const { data, error } = await this.supabase
                .from('audit_events')
                .select('*')
                .order('timestamp', { ascending: false })
                .limit(Number(limit));

            if (error) throw error;
            res.json(data || []);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch events' });
        }
    }

    private async getEventsByType(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { type } = req.params;
            const { limit = 100 } = req.query;
            const { data, error } = await this.supabase
                .from('audit_events')
                .select('*')
                .eq('type', type)
                .order('timestamp', { ascending: false })
                .limit(Number(limit));

            if (error) throw error;
            res.json(data || []);
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch events' });
        }
    }

    // Analytics endpoints
    private async getAnalyticsOverview(req: express.Request, res: express.Response): Promise<void> {
        try {
            const agentCount = await this.registry.getAgentCount();
            const toolCount = await this.registry.getToolCount();
            const actionCounter = await this.auditLog.getActionCounter();
            const batchCounter = await this.auditLog.getBatchCounter();

            res.json({
                agents: agentCount,
                tools: toolCount,
                actions: actionCounter,
                batches: batchCounter,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            res.status(500).json({ error: 'Failed to fetch analytics' });
        }
    }

    private async getAgentAnalytics(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { agentId } = req.params;
            const agent = await this.registry.getAgent(agentId);
            const actionIndices = await this.auditLog.getAgentActionIndices(agentId);
            const rateLimit = await this.accessControl.getAgentRateLimit(agentId);

            res.json({
                agent,
                totalActions: actionIndices.length,
                rateLimit,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            res.status(404).json({ error: 'Agent analytics not found' });
        }
    }

    private async getToolAnalytics(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { toolId } = req.params;
            const tool = await this.registry.getTool(toolId);
            const actionIndices = await this.auditLog.getToolActionIndices(toolId);

            res.json({
                tool,
                totalUsage: actionIndices.length,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            res.status(404).json({ error: 'Tool analytics not found' });
        }
    }

    // Compliance endpoints
    private async getComplianceReport(req: express.Request, res: express.Response): Promise<void> {
        try {
            const agentCount = await this.registry.getAgentCount();
            const toolCount = await this.registry.getToolCount();
            const actionCounter = await this.auditLog.getActionCounter();

            // Get recent events for compliance analysis
            const { data: events } = await this.supabase
                .from('audit_events')
                .select('*')
                .order('timestamp', { ascending: false })
                .limit(1000);

            const complianceReport = {
                summary: {
                    totalAgents: agentCount,
                    totalTools: toolCount,
                    totalActions: actionCounter,
                    lastUpdated: new Date().toISOString()
                },
                recentActivity: events || [],
                recommendations: this.generateComplianceRecommendations(events || [])
            };

            res.json(complianceReport);
        } catch (error) {
            res.status(500).json({ error: 'Failed to generate compliance report' });
        }
    }

    private async getAgentCompliance(req: express.Request, res: express.Response): Promise<void> {
        try {
            const { agentId } = req.params;
            const agent = await this.registry.getAgent(agentId);
            const rateLimit = await this.accessControl.getAgentRateLimit(agentId);

            // Get agent-specific events
            const { data: events } = await this.supabase
                .from('audit_events')
                .select('*')
                .contains('data', { agentId })
                .order('timestamp', { ascending: false })
                .limit(100);

            const compliance = {
                agent,
                rateLimit,
                recentActivity: events || [],
                complianceScore: this.calculateComplianceScore(events || []),
                timestamp: new Date().toISOString()
            };

            res.json(compliance);
        } catch (error) {
            res.status(404).json({ error: 'Agent compliance not found' });
        }
    }

    private generateComplianceRecommendations(events: any[]): string[] {
        const recommendations: string[] = [];

        // Analyze events and generate recommendations
        const actionEvents = events.filter(e => e.type === 'ActionLogged');
        const policyEvents = events.filter(e => e.type === 'PolicyCreated');

        if (actionEvents.length > 1000) {
            recommendations.push('Consider implementing stricter rate limiting policies');
        }

        if (policyEvents.length < 5) {
            recommendations.push('Consider creating more granular access control policies');
        }

        return recommendations;
    }

    private calculateComplianceScore(events: any[]): number {
        // Simple compliance score calculation
        const totalEvents = events.length;
        const complianceEvents = events.filter(e =>
            e.type === 'ActionLogged' && e.data?.status === 1
        ).length;

        return totalEvents > 0 ? (complianceEvents / totalEvents) * 100 : 100;
    }

    private errorHandler(err: any, req: express.Request, res: express.Response, next: express.NextFunction): void {
        console.error('Dashboard error:', err);
        res.status(500).json({ error: 'Internal server error' });
    }

    async start(): Promise<void> {
        return new Promise((resolve) => {
            this.server = this.app.listen(this.config.port, () => {
                console.log(`Dashboard server running on port ${this.config.port}`);
                resolve();
            });
        });
    }

    async stop(): Promise<void> {
        if (this.server) {
            return new Promise((resolve) => {
                this.server.close(() => {
                    console.log('Dashboard server stopped');
                    resolve();
                });
            });
        }
    }

    getApp(): express.Application {
        return this.app;
    }
}
