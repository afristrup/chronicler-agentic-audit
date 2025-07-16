// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./interfaces/IChroniclerRegistry.sol";

/**
 * @title ChroniclerRegistry
 * @dev Central registry for agents, tools, and operators with comprehensive management
 */
contract ChroniclerRegistry is
    IChroniclerRegistry,
    AccessControl,
    Pausable,
    ReentrancyGuard
{
    using Strings for uint256;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    bytes32 public constant REGISTRAR_ROLE = keccak256("REGISTRAR_ROLE");

    // Storage mappings
    mapping(bytes32 => Agent) private _agents;
    mapping(bytes32 => Tool) private _tools;
    mapping(bytes32 => Category) private _categories;

    // Index mappings for efficient queries
    mapping(address => bytes32[]) private _operatorAgents;
    mapping(bytes32 => bytes32[]) private _categoryTools;

    // Counters
    uint256 private _agentCount;
    uint256 private _toolCount;
    uint256 private _categoryCount;

    // Arrays for enumeration
    bytes32[] private _allAgents;
    bytes32[] private _allTools;
    bytes32[] private _allCategories;

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(REGISTRAR_ROLE, msg.sender);

        // Register default category
        _registerDefaultCategory();
    }

    // ============ AGENT FUNCTIONS ============

    function registerAgent(
        bytes32 agentId,
        address operator,
        string calldata metadataURI
    ) external onlyRole(REGISTRAR_ROLE) whenNotPaused {
        require(agentId != bytes32(0), "Invalid agent ID");
        require(_agents[agentId].createdAt == 0, "Agent already exists");
        require(operator != address(0), "Invalid operator address");
        require(bytes(metadataURI).length > 0, "Metadata URI required");

        Agent memory newAgent = Agent({
            id: agentId,
            operator: operator,
            metadataURI: metadataURI,
            isActive: true,
            createdAt: block.timestamp,
            lastActionAt: 0,
            totalActions: 0
        });

        _agents[agentId] = newAgent;
        _operatorAgents[operator].push(agentId);
        _allAgents.push(agentId);
        _agentCount++;

        emit AgentRegistered(agentId, operator, metadataURI);
    }

    function updateAgentStatus(
        bytes32 agentId,
        bool isActive
    ) external onlyRole(ADMIN_ROLE) {
        require(_agents[agentId].createdAt != 0, "Agent does not exist");
        require(_agents[agentId].isActive != isActive, "Status already set");

        _agents[agentId].isActive = isActive;
        emit AgentStatusChanged(agentId, isActive);
    }

    function updateAgentOperator(
        bytes32 agentId,
        address newOperator
    ) external onlyRole(ADMIN_ROLE) {
        require(_agents[agentId].createdAt != 0, "Agent does not exist");
        require(newOperator != address(0), "Invalid operator address");
        require(
            _agents[agentId].operator != newOperator,
            "Operator already set"
        );

        address oldOperator = _agents[agentId].operator;
        _agents[agentId].operator = newOperator;

        // Update operator mappings
        _removeAgentFromOperator(oldOperator, agentId);
        _operatorAgents[newOperator].push(agentId);

        emit AgentOperatorChanged(agentId, oldOperator, newOperator);
    }

    function updateAgentMetadata(
        bytes32 agentId,
        string calldata metadataURI
    ) external onlyRole(ADMIN_ROLE) {
        require(_agents[agentId].createdAt != 0, "Agent does not exist");
        require(bytes(metadataURI).length > 0, "Metadata URI required");

        _agents[agentId].metadataURI = metadataURI;
        emit AgentMetadataUpdated(agentId, metadataURI);
    }

    // ============ TOOL FUNCTIONS ============

    function registerTool(
        bytes32 toolId,
        string calldata name,
        string calldata metadataURI,
        bytes32 categoryId,
        uint256 riskLevel
    ) external onlyRole(REGISTRAR_ROLE) whenNotPaused {
        require(toolId != bytes32(0), "Invalid tool ID");
        require(_tools[toolId].riskLevel == 0, "Tool already exists");
        require(bytes(name).length > 0, "Tool name required");
        require(bytes(metadataURI).length > 0, "Metadata URI required");
        require(_categories[categoryId].isActive, "Invalid category");
        require(riskLevel <= 100, "Risk level must be 0-100");

        Tool memory newTool = Tool({
            id: toolId,
            name: name,
            metadataURI: metadataURI,
            categoryId: categoryId,
            isActive: true,
            riskLevel: riskLevel,
            usageCount: 0,
            lastUsedAt: 0
        });

        _tools[toolId] = newTool;
        _categoryTools[categoryId].push(toolId);
        _allTools.push(toolId);
        _toolCount++;

        emit ToolRegistered(toolId, name, riskLevel, metadataURI);
    }

    function updateToolStatus(
        bytes32 toolId,
        bool isActive
    ) external onlyRole(ADMIN_ROLE) {
        require(_tools[toolId].riskLevel != 0, "Tool does not exist");
        require(_tools[toolId].isActive != isActive, "Status already set");

        _tools[toolId].isActive = isActive;
        emit ToolStatusChanged(toolId, isActive);
    }

    function updateToolRiskLevel(
        bytes32 toolId,
        uint256 newRiskLevel
    ) external onlyRole(ADMIN_ROLE) {
        require(_tools[toolId].riskLevel != 0, "Tool does not exist");
        require(newRiskLevel <= 100, "Risk level must be 0-100");

        uint256 oldRisk = _tools[toolId].riskLevel;
        _tools[toolId].riskLevel = newRiskLevel;

        emit ToolRiskLevelUpdated(toolId, oldRisk, newRiskLevel);
    }

    function updateToolMetadata(
        bytes32 toolId,
        string calldata metadataURI
    ) external onlyRole(ADMIN_ROLE) {
        require(_tools[toolId].riskLevel != 0, "Tool does not exist");
        require(bytes(metadataURI).length > 0, "Metadata URI required");

        _tools[toolId].metadataURI = metadataURI;
        emit ToolMetadataUpdated(toolId, metadataURI);
    }

    // ============ CATEGORY FUNCTIONS ============

    function registerCategory(
        bytes32 categoryId,
        string calldata name,
        string calldata description,
        uint256 riskMultiplier
    ) external onlyRole(REGISTRAR_ROLE) whenNotPaused {
        require(categoryId != bytes32(0), "Invalid category ID");
        require(
            _categories[categoryId].isActive == false,
            "Category already exists"
        );
        require(bytes(name).length > 0, "Category name required");
        require(
            riskMultiplier > 0 && riskMultiplier <= 100,
            "Invalid risk multiplier"
        );

        Category memory newCategory = Category({
            id: categoryId,
            name: name,
            description: description,
            isActive: true,
            riskMultiplier: riskMultiplier
        });

        _categories[categoryId] = newCategory;
        _allCategories.push(categoryId);
        _categoryCount++;

        emit CategoryRegistered(categoryId, name, riskMultiplier);
    }

    function updateCategoryStatus(
        bytes32 categoryId,
        bool isActive
    ) external onlyRole(ADMIN_ROLE) {
        require(
            _categories[categoryId].isActive != false,
            "Category does not exist"
        );
        require(
            _categories[categoryId].isActive != isActive,
            "Status already set"
        );

        _categories[categoryId].isActive = isActive;
        emit CategoryStatusChanged(categoryId, isActive);
    }

    function updateCategoryRiskMultiplier(
        bytes32 categoryId,
        uint256 newMultiplier
    ) external onlyRole(ADMIN_ROLE) {
        require(
            _categories[categoryId].isActive != false,
            "Category does not exist"
        );
        require(
            newMultiplier > 0 && newMultiplier <= 100,
            "Invalid risk multiplier"
        );

        uint256 oldMultiplier = _categories[categoryId].riskMultiplier;
        _categories[categoryId].riskMultiplier = newMultiplier;

        emit CategoryRiskMultiplierUpdated(
            categoryId,
            oldMultiplier,
            newMultiplier
        );
    }

    // ============ QUERY FUNCTIONS ============

    function getAgent(bytes32 agentId) external view returns (Agent memory) {
        return _agents[agentId];
    }

    function getTool(bytes32 toolId) external view returns (Tool memory) {
        return _tools[toolId];
    }

    function getCategory(
        bytes32 categoryId
    ) external view returns (Category memory) {
        return _categories[categoryId];
    }

    function isValidAgent(bytes32 agentId) external view returns (bool) {
        return _agents[agentId].createdAt != 0 && _agents[agentId].isActive;
    }

    function isValidTool(bytes32 toolId) external view returns (bool) {
        return _tools[toolId].riskLevel != 0 && _tools[toolId].isActive;
    }

    function isValidCategory(bytes32 categoryId) external view returns (bool) {
        return _categories[categoryId].isActive;
    }

    // ============ STATISTICS FUNCTIONS ============

    function incrementAgentActions(bytes32 agentId) external {
        require(_agents[agentId].createdAt != 0, "Agent does not exist");
        _agents[agentId].totalActions++;
        _agents[agentId].lastActionAt = block.timestamp;
    }

    function incrementToolUsage(bytes32 toolId) external {
        require(_tools[toolId].riskLevel != 0, "Tool does not exist");
        _tools[toolId].usageCount++;
        _tools[toolId].lastUsedAt = block.timestamp;
    }

    // ============ ENUMERATION FUNCTIONS ============

    function getAllAgents() external view returns (bytes32[] memory) {
        return _allAgents;
    }

    function getAllTools() external view returns (bytes32[] memory) {
        return _allTools;
    }

    function getAllCategories() external view returns (bytes32[] memory) {
        return _allCategories;
    }

    function getAgentCount() external view returns (uint256) {
        return _agentCount;
    }

    function getToolCount() external view returns (uint256) {
        return _toolCount;
    }

    function getCategoryCount() external view returns (uint256) {
        return _categoryCount;
    }

    // ============ INTERNAL FUNCTIONS ============

    function _registerDefaultCategory() private {
        bytes32 defaultCategoryId = keccak256("DEFAULT_CATEGORY");
        Category memory defaultCategory = Category({
            id: defaultCategoryId,
            name: "Default",
            description: "Default category for tools",
            isActive: true,
            riskMultiplier: 1
        });

        _categories[defaultCategoryId] = defaultCategory;
        _allCategories.push(defaultCategoryId);
        _categoryCount++;
    }

    function _removeAgentFromOperator(
        address operator,
        bytes32 agentId
    ) private {
        bytes32[] storage agents = _operatorAgents[operator];
        for (uint256 i = 0; i < agents.length; i++) {
            if (agents[i] == agentId) {
                agents[i] = agents[agents.length - 1];
                agents.pop();
                break;
            }
        }
    }

    // ============ ADMIN FUNCTIONS ============

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
