// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title IChroniclerRegistry
 * @dev Interface for the Chronicler Registry contract
 */
interface IChroniclerRegistry {
    struct Agent {
        bytes32 id;
        address operator;
        string metadataURI;
        bool isActive;
        uint256 createdAt;
        uint256 lastActionAt;
        uint256 totalActions;
    }

    struct Tool {
        bytes32 id;
        string name;
        string metadataURI;
        bytes32 categoryId;
        bool isActive;
        uint256 riskLevel;
        uint256 usageCount;
        uint256 lastUsedAt;
    }

    struct Category {
        bytes32 id;
        string name;
        string description;
        bool isActive;
        uint256 riskMultiplier;
    }

    // Events
    event AgentRegistered(
        bytes32 indexed agentId,
        address indexed operator,
        string metadataURI
    );
    event AgentStatusChanged(bytes32 indexed agentId, bool isActive);
    event AgentOperatorChanged(
        bytes32 indexed agentId,
        address indexed oldOperator,
        address indexed newOperator
    );
    event AgentMetadataUpdated(bytes32 indexed agentId, string metadataURI);

    event ToolRegistered(
        bytes32 indexed toolId,
        string name,
        uint256 riskLevel,
        string metadataURI
    );
    event ToolStatusChanged(bytes32 indexed toolId, bool isActive);
    event ToolRiskLevelUpdated(
        bytes32 indexed toolId,
        uint256 oldRisk,
        uint256 newRisk
    );
    event ToolMetadataUpdated(bytes32 indexed toolId, string metadataURI);

    event CategoryRegistered(
        bytes32 indexed categoryId,
        string name,
        uint256 riskMultiplier
    );
    event CategoryStatusChanged(bytes32 indexed categoryId, bool isActive);
    event CategoryRiskMultiplierUpdated(
        bytes32 indexed categoryId,
        uint256 oldMultiplier,
        uint256 newMultiplier
    );

    // Agent functions
    function registerAgent(
        bytes32 agentId,
        address operator,
        string calldata metadataURI
    ) external;
    function updateAgentStatus(bytes32 agentId, bool isActive) external;
    function updateAgentOperator(bytes32 agentId, address newOperator) external;
    function updateAgentMetadata(
        bytes32 agentId,
        string calldata metadataURI
    ) external;

    // Tool functions
    function registerTool(
        bytes32 toolId,
        string calldata name,
        string calldata metadataURI,
        bytes32 categoryId,
        uint256 riskLevel
    ) external;
    function updateToolStatus(bytes32 toolId, bool isActive) external;
    function updateToolRiskLevel(bytes32 toolId, uint256 newRiskLevel) external;
    function updateToolMetadata(
        bytes32 toolId,
        string calldata metadataURI
    ) external;

    // Category functions
    function registerCategory(
        bytes32 categoryId,
        string calldata name,
        string calldata description,
        uint256 riskMultiplier
    ) external;
    function updateCategoryStatus(bytes32 categoryId, bool isActive) external;
    function updateCategoryRiskMultiplier(
        bytes32 categoryId,
        uint256 newMultiplier
    ) external;

    // Query functions
    function getAgent(bytes32 agentId) external view returns (Agent memory);
    function getTool(bytes32 toolId) external view returns (Tool memory);
    function getCategory(
        bytes32 categoryId
    ) external view returns (Category memory);
    function isValidAgent(bytes32 agentId) external view returns (bool);
    function isValidTool(bytes32 toolId) external view returns (bool);
    function isValidCategory(bytes32 categoryId) external view returns (bool);

    // Statistics functions
    function incrementAgentActions(bytes32 agentId) external;
    function incrementToolUsage(bytes32 toolId) external;

    // Enumeration functions
    function getAllAgents() external view returns (bytes32[] memory);
    function getAllTools() external view returns (bytes32[] memory);
    function getAllCategories() external view returns (bytes32[] memory);
    function getAgentCount() external view returns (uint256);
    function getToolCount() external view returns (uint256);
    function getCategoryCount() external view returns (uint256);
}
