import { ethers } from 'ethers';
import { ChroniclerRegistry } from '../../source/contracts/ChroniclerRegistry';
import { TestUtils } from '../utils/test-utils';

describe('ChroniclerRegistry', () => {
    let registry: ChroniclerRegistry;
    let mockProvider: ethers.Provider;
    let mockSigner: ethers.Signer;
    let mockContract: any;
    let contractAddress: string;

    beforeEach(() => {
        mockProvider = TestUtils.createMockProvider();
        mockSigner = TestUtils.createMockSigner();
        contractAddress = TestUtils.generateRandomAddress();
        mockContract = {
            registerAgent: jest.fn(),
            updateAgentStatus: jest.fn(),
            updateAgentOperator: jest.fn(),
            updateAgentMetadata: jest.fn(),
            registerTool: jest.fn(),
            updateToolStatus: jest.fn(),
            updateToolRiskLevel: jest.fn(),
            updateToolMetadata: jest.fn(),
            registerCategory: jest.fn(),
            updateCategoryStatus: jest.fn(),
            updateCategoryRiskMultiplier: jest.fn(),
            getAgent: jest.fn(),
            getTool: jest.fn(),
            getCategory: jest.fn(),
            isValidAgent: jest.fn(),
            isValidTool: jest.fn(),
            isValidCategory: jest.fn(),
            incrementAgentActions: jest.fn(),
            incrementToolUsage: jest.fn(),
            getAllAgents: jest.fn(),
            getAllTools: jest.fn(),
            getAllCategories: jest.fn(),
            getAgentCount: jest.fn(),
            getToolCount: jest.fn(),
            getCategoryCount: jest.fn(),
            pause: jest.fn(),
            unpause: jest.fn(),
            hasRole: jest.fn(),
            grantRole: jest.fn(),
            revokeRole: jest.fn(),
            on: jest.fn(),
            target: contractAddress
        };

        // Mock ethers.Contract constructor
        jest.spyOn(ethers, 'Contract').mockImplementation(() => mockContract);

        registry = new ChroniclerRegistry(
            contractAddress,
            TestUtils.createMockContractAbi(),
            mockProvider,
            mockSigner
        );
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    describe('Constructor', () => {
        it('should create a ChroniclerRegistry instance', () => {
            expect(registry).toBeInstanceOf(ChroniclerRegistry);
        });

        it('should initialize with correct contract address', () => {
            expect(registry.getAddress()).toBe(contractAddress);
        });

        it('should return contract instance', () => {
            expect(registry.getContract()).toBe(mockContract);
        });
    });

    describe('Agent Management', () => {
        const mockAgent = TestUtils.createMockAgent();

        describe('registerAgent', () => {
            it('should call registerAgent on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.registerAgent.mockResolvedValue(tx);

                const result = await registry.registerAgent(
                    mockAgent.id,
                    mockAgent.operator,
                    mockAgent.metadataURI
                );

                expect(mockContract.registerAgent).toHaveBeenCalledWith(
                    mockAgent.id,
                    mockAgent.operator,
                    mockAgent.metadataURI
                );
                expect(result).toBe(tx);
            });

            it('should handle registration errors', async () => {
                const error = new Error('Registration failed');
                mockContract.registerAgent.mockRejectedValue(error);

                await expect(
                    registry.registerAgent(mockAgent.id, mockAgent.operator, mockAgent.metadataURI)
                ).rejects.toThrow('Registration failed');
            });
        });

        describe('updateAgentStatus', () => {
            it('should call updateAgentStatus on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.updateAgentStatus.mockResolvedValue(tx);

                const result = await registry.updateAgentStatus(mockAgent.id, false);

                expect(mockContract.updateAgentStatus).toHaveBeenCalledWith(mockAgent.id, false);
                expect(result).toBe(tx);
            });
        });

        describe('updateAgentOperator', () => {
            it('should call updateAgentOperator on contract', async () => {
                const newOperator = TestUtils.generateRandomAddress();
                const tx = { hash: '0x123' };
                mockContract.updateAgentOperator.mockResolvedValue(tx);

                const result = await registry.updateAgentOperator(mockAgent.id, newOperator);

                expect(mockContract.updateAgentOperator).toHaveBeenCalledWith(mockAgent.id, newOperator);
                expect(result).toBe(tx);
            });
        });

        describe('updateAgentMetadata', () => {
            it('should call updateAgentMetadata on contract', async () => {
                const newMetadataURI = 'ipfs://new-metadata';
                const tx = { hash: '0x123' };
                mockContract.updateAgentMetadata.mockResolvedValue(tx);

                const result = await registry.updateAgentMetadata(mockAgent.id, newMetadataURI);

                expect(mockContract.updateAgentMetadata).toHaveBeenCalledWith(mockAgent.id, newMetadataURI);
                expect(result).toBe(tx);
            });
        });

        describe('getAgent', () => {
            it('should return agent data', async () => {
                const contractAgent = {
                    id: mockAgent.id,
                    operator: mockAgent.operator,
                    metadataURI: mockAgent.metadataURI,
                    isActive: mockAgent.isActive,
                    createdAt: mockAgent.createdAt,
                    lastActionAt: mockAgent.lastActionAt,
                    totalActions: mockAgent.totalActions
                };
                mockContract.getAgent.mockResolvedValue(contractAgent);

                const result = await registry.getAgent(mockAgent.id);

                expect(mockContract.getAgent).toHaveBeenCalledWith(mockAgent.id);
                expect(result).toEqual(mockAgent);
                expect(TestUtils.validateAgent(result)).toBe(true);
            });
        });

        describe('isValidAgent', () => {
            it('should return true for valid agent', async () => {
                mockContract.isValidAgent.mockResolvedValue(true);

                const result = await registry.isValidAgent(mockAgent.id);

                expect(mockContract.isValidAgent).toHaveBeenCalledWith(mockAgent.id);
                expect(result).toBe(true);
            });

            it('should return false for invalid agent', async () => {
                mockContract.isValidAgent.mockResolvedValue(false);

                const result = await registry.isValidAgent(mockAgent.id);

                expect(result).toBe(false);
            });
        });
    });

    describe('Tool Management', () => {
        const mockTool = TestUtils.createMockTool();

        describe('registerTool', () => {
            it('should call registerTool on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.registerTool.mockResolvedValue(tx);

                const result = await registry.registerTool(
                    mockTool.id,
                    mockTool.name,
                    mockTool.metadataURI,
                    mockTool.categoryId,
                    mockTool.riskLevel
                );

                expect(mockContract.registerTool).toHaveBeenCalledWith(
                    mockTool.id,
                    mockTool.name,
                    mockTool.metadataURI,
                    mockTool.categoryId,
                    mockTool.riskLevel
                );
                expect(result).toBe(tx);
            });
        });

        describe('updateToolStatus', () => {
            it('should call updateToolStatus on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.updateToolStatus.mockResolvedValue(tx);

                const result = await registry.updateToolStatus(mockTool.id, false);

                expect(mockContract.updateToolStatus).toHaveBeenCalledWith(mockTool.id, false);
                expect(result).toBe(tx);
            });
        });

        describe('updateToolRiskLevel', () => {
            it('should call updateToolRiskLevel on contract', async () => {
                const newRiskLevel = 75;
                const tx = { hash: '0x123' };
                mockContract.updateToolRiskLevel.mockResolvedValue(tx);

                const result = await registry.updateToolRiskLevel(mockTool.id, newRiskLevel);

                expect(mockContract.updateToolRiskLevel).toHaveBeenCalledWith(mockTool.id, newRiskLevel);
                expect(result).toBe(tx);
            });
        });

        describe('updateToolMetadata', () => {
            it('should call updateToolMetadata on contract', async () => {
                const newMetadataURI = 'ipfs://new-tool-metadata';
                const tx = { hash: '0x123' };
                mockContract.updateToolMetadata.mockResolvedValue(tx);

                const result = await registry.updateToolMetadata(mockTool.id, newMetadataURI);

                expect(mockContract.updateToolMetadata).toHaveBeenCalledWith(mockTool.id, newMetadataURI);
                expect(result).toBe(tx);
            });
        });

        describe('getTool', () => {
            it('should return tool data', async () => {
                const contractTool = {
                    id: mockTool.id,
                    name: mockTool.name,
                    metadataURI: mockTool.metadataURI,
                    categoryId: mockTool.categoryId,
                    isActive: mockTool.isActive,
                    riskLevel: mockTool.riskLevel,
                    usageCount: mockTool.usageCount,
                    lastUsedAt: mockTool.lastUsedAt
                };
                mockContract.getTool.mockResolvedValue(contractTool);

                const result = await registry.getTool(mockTool.id);

                expect(mockContract.getTool).toHaveBeenCalledWith(mockTool.id);
                expect(result).toEqual(mockTool);
                expect(TestUtils.validateTool(result)).toBe(true);
            });
        });

        describe('isValidTool', () => {
            it('should return true for valid tool', async () => {
                mockContract.isValidTool.mockResolvedValue(true);

                const result = await registry.isValidTool(mockTool.id);

                expect(mockContract.isValidTool).toHaveBeenCalledWith(mockTool.id);
                expect(result).toBe(true);
            });
        });
    });

    describe('Category Management', () => {
        const mockCategory = TestUtils.createMockCategory();

        describe('registerCategory', () => {
            it('should call registerCategory on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.registerCategory.mockResolvedValue(tx);

                const result = await registry.registerCategory(
                    mockCategory.id,
                    mockCategory.name,
                    mockCategory.description,
                    mockCategory.riskMultiplier
                );

                expect(mockContract.registerCategory).toHaveBeenCalledWith(
                    mockCategory.id,
                    mockCategory.name,
                    mockCategory.description,
                    mockCategory.riskMultiplier
                );
                expect(result).toBe(tx);
            });
        });

        describe('updateCategoryStatus', () => {
            it('should call updateCategoryStatus on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.updateCategoryStatus.mockResolvedValue(tx);

                const result = await registry.updateCategoryStatus(mockCategory.id, false);

                expect(mockContract.updateCategoryStatus).toHaveBeenCalledWith(mockCategory.id, false);
                expect(result).toBe(tx);
            });
        });

        describe('updateCategoryRiskMultiplier', () => {
            it('should call updateCategoryRiskMultiplier on contract', async () => {
                const newMultiplier = 50;
                const tx = { hash: '0x123' };
                mockContract.updateCategoryRiskMultiplier.mockResolvedValue(tx);

                const result = await registry.updateCategoryRiskMultiplier(mockCategory.id, newMultiplier);

                expect(mockContract.updateCategoryRiskMultiplier).toHaveBeenCalledWith(mockCategory.id, newMultiplier);
                expect(result).toBe(tx);
            });
        });

        describe('getCategory', () => {
            it('should return category data', async () => {
                const contractCategory = {
                    id: mockCategory.id,
                    name: mockCategory.name,
                    description: mockCategory.description,
                    isActive: mockCategory.isActive,
                    riskMultiplier: mockCategory.riskMultiplier
                };
                mockContract.getCategory.mockResolvedValue(contractCategory);

                const result = await registry.getCategory(mockCategory.id);

                expect(mockContract.getCategory).toHaveBeenCalledWith(mockCategory.id);
                expect(result).toEqual(mockCategory);
                expect(TestUtils.validateCategory(result)).toBe(true);
            });
        });

        describe('isValidCategory', () => {
            it('should return true for valid category', async () => {
                mockContract.isValidCategory.mockResolvedValue(true);

                const result = await registry.isValidCategory(mockCategory.id);

                expect(mockContract.isValidCategory).toHaveBeenCalledWith(mockCategory.id);
                expect(result).toBe(true);
            });
        });
    });

    describe('Statistics Functions', () => {
        describe('incrementAgentActions', () => {
            it('should call incrementAgentActions on contract', async () => {
                const agentId = TestUtils.generateRandomBytes32();
                const tx = { hash: '0x123' };
                mockContract.incrementAgentActions.mockResolvedValue(tx);

                const result = await registry.incrementAgentActions(agentId);

                expect(mockContract.incrementAgentActions).toHaveBeenCalledWith(agentId);
                expect(result).toBe(tx);
            });
        });

        describe('incrementToolUsage', () => {
            it('should call incrementToolUsage on contract', async () => {
                const toolId = TestUtils.generateRandomBytes32();
                const tx = { hash: '0x123' };
                mockContract.incrementToolUsage.mockResolvedValue(tx);

                const result = await registry.incrementToolUsage(toolId);

                expect(mockContract.incrementToolUsage).toHaveBeenCalledWith(toolId);
                expect(result).toBe(tx);
            });
        });
    });

    describe('Enumeration Functions', () => {
        describe('getAllAgents', () => {
            it('should return all agent IDs', async () => {
                const agentIds = [
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32()
                ];
                mockContract.getAllAgents.mockResolvedValue(agentIds);

                const result = await registry.getAllAgents();

                expect(mockContract.getAllAgents).toHaveBeenCalled();
                expect(result).toEqual(agentIds);
            });
        });

        describe('getAllTools', () => {
            it('should return all tool IDs', async () => {
                const toolIds = [
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32()
                ];
                mockContract.getAllTools.mockResolvedValue(toolIds);

                const result = await registry.getAllTools();

                expect(mockContract.getAllTools).toHaveBeenCalled();
                expect(result).toEqual(toolIds);
            });
        });

        describe('getAllCategories', () => {
            it('should return all category IDs', async () => {
                const categoryIds = [
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32(),
                    TestUtils.generateRandomBytes32()
                ];
                mockContract.getAllCategories.mockResolvedValue(categoryIds);

                const result = await registry.getAllCategories();

                expect(mockContract.getAllCategories).toHaveBeenCalled();
                expect(result).toEqual(categoryIds);
            });
        });

        describe('getAgentCount', () => {
            it('should return agent count', async () => {
                const count = 42;
                mockContract.getAgentCount.mockResolvedValue(count);

                const result = await registry.getAgentCount();

                expect(mockContract.getAgentCount).toHaveBeenCalled();
                expect(result).toBe(count);
            });
        });

        describe('getToolCount', () => {
            it('should return tool count', async () => {
                const count = 15;
                mockContract.getToolCount.mockResolvedValue(count);

                const result = await registry.getToolCount();

                expect(mockContract.getToolCount).toHaveBeenCalled();
                expect(result).toBe(count);
            });
        });

        describe('getCategoryCount', () => {
            it('should return category count', async () => {
                const count = 8;
                mockContract.getCategoryCount.mockResolvedValue(count);

                const result = await registry.getCategoryCount();

                expect(mockContract.getCategoryCount).toHaveBeenCalled();
                expect(result).toBe(count);
            });
        });
    });

    describe('Admin Functions', () => {
        describe('pause', () => {
            it('should call pause on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.pause.mockResolvedValue(tx);

                const result = await registry.pause();

                expect(mockContract.pause).toHaveBeenCalled();
                expect(result).toBe(tx);
            });
        });

        describe('unpause', () => {
            it('should call unpause on contract', async () => {
                const tx = { hash: '0x123' };
                mockContract.unpause.mockResolvedValue(tx);

                const result = await registry.unpause();

                expect(mockContract.unpause).toHaveBeenCalled();
                expect(result).toBe(tx);
            });
        });
    });

    describe('Role Management', () => {
        describe('hasRole', () => {
            it('should check if account has role', async () => {
                const role = 'ADMIN_ROLE';
                const account = TestUtils.generateRandomAddress();
                mockContract.hasRole.mockResolvedValue(true);

                const result = await registry.hasRole(role, account);

                expect(mockContract.hasRole).toHaveBeenCalledWith(role, account);
                expect(result).toBe(true);
            });
        });

        describe('grantRole', () => {
            it('should grant role to account', async () => {
                const role = 'OPERATOR_ROLE';
                const account = TestUtils.generateRandomAddress();
                const tx = { hash: '0x123' };
                mockContract.grantRole.mockResolvedValue(tx);

                const result = await registry.grantRole(role, account);

                expect(mockContract.grantRole).toHaveBeenCalledWith(role, account);
                expect(result).toBe(tx);
            });
        });

        describe('revokeRole', () => {
            it('should revoke role from account', async () => {
                const role = 'OPERATOR_ROLE';
                const account = TestUtils.generateRandomAddress();
                const tx = { hash: '0x123' };
                mockContract.revokeRole.mockResolvedValue(tx);

                const result = await registry.revokeRole(role, account);

                expect(mockContract.revokeRole).toHaveBeenCalledWith(role, account);
                expect(result).toBe(tx);
            });
        });
    });

    describe('Event Listeners', () => {
        describe('onAgentRegistered', () => {
            it('should set up agent registered event listener', () => {
                const callback = jest.fn();
                registry.onAgentRegistered(callback);

                expect(mockContract.on).toHaveBeenCalledWith('AgentRegistered', callback);
            });
        });

        describe('onToolRegistered', () => {
            it('should set up tool registered event listener', () => {
                const callback = jest.fn();
                registry.onToolRegistered(callback);

                expect(mockContract.on).toHaveBeenCalledWith('ToolRegistered', callback);
            });
        });

        describe('onCategoryRegistered', () => {
            it('should set up category registered event listener', () => {
                const callback = jest.fn();
                registry.onCategoryRegistered(callback);

                expect(mockContract.on).toHaveBeenCalledWith('CategoryRegistered', callback);
            });
        });
    });
});