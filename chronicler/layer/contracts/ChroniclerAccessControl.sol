// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./interfaces/IChroniclerRegistry.sol";

/**
 * @title ChroniclerAccessControl
 * @dev Fine-grained permission management with rate limiting and risk controls
 */
contract ChroniclerAccessControl is AccessControl, Pausable, ReentrancyGuard {
    IChroniclerRegistry public immutable registry;

    bytes32 public constant POLICY_ADMIN_ROLE = keccak256("POLICY_ADMIN_ROLE");
    bytes32 public constant RATE_LIMITER_ROLE = keccak256("RATE_LIMITER_ROLE");

    struct Policy {
        uint256 dailyLimit; // Maximum actions per day
        uint256 maxGas; // Maximum gas per action
        uint256 maxRisk; // Maximum risk level allowed
        uint256 cooldownPeriod; // Cooldown between actions (seconds)
        bool isActive;
        uint256 createdAt;
        uint256 updatedAt;
    }

    struct RateLimit {
        uint256 lastActionTime;
        uint256 dailyActionCount;
        uint256 lastResetTime;
        uint256 totalActions;
        uint256 totalGasUsed;
    }

    struct AgentPolicy {
        bytes32 agentId;
        uint256 policyId;
        bool isActive;
        uint256 assignedAt;
    }

    struct ToolPolicy {
        bytes32 toolId;
        uint256 policyId;
        bool isActive;
        uint256 assignedAt;
    }

    // Storage mappings
    mapping(uint256 => Policy) public policies;
    mapping(bytes32 => RateLimit) public agentRateLimits;
    mapping(bytes32 => AgentPolicy) public agentPolicies;
    mapping(bytes32 => ToolPolicy) public toolPolicies;
    mapping(bytes32 => uint256) public agentPolicyIds;
    mapping(bytes32 => uint256) public toolPolicyIds;

    // Counters
    uint256 private _policyCounter;

    // Default policy ID
    uint256 public constant DEFAULT_POLICY_ID = 1;

    // Events
    event PolicyCreated(
        uint256 indexed policyId,
        uint256 dailyLimit,
        uint256 maxGas,
        uint256 maxRisk
    );
    event PolicyUpdated(
        uint256 indexed policyId,
        uint256 dailyLimit,
        uint256 maxGas,
        uint256 maxRisk
    );
    event PolicyAssigned(
        bytes32 indexed agentId,
        uint256 indexed policyId,
        bool isAgent
    );
    event PolicyRevoked(
        bytes32 indexed agentId,
        uint256 indexed policyId,
        bool isAgent
    );
    event RateLimitExceeded(
        bytes32 indexed agentId,
        uint256 limit,
        uint256 current
    );
    event RiskLevelExceeded(
        bytes32 indexed agentId,
        bytes32 indexed toolId,
        uint256 risk,
        uint256 maxRisk
    );

    constructor(address _registry) {
        require(_registry != address(0), "Invalid registry address");
        registry = IChroniclerRegistry(_registry);

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(POLICY_ADMIN_ROLE, msg.sender);
        _grantRole(RATE_LIMITER_ROLE, msg.sender);

        // Create default policy
        _createDefaultPolicy();
    }

    /**
     * @dev Create a new policy
     */
    function createPolicy(
        uint256 dailyLimit,
        uint256 maxGas,
        uint256 maxRisk,
        uint256 cooldownPeriod
    ) external onlyRole(POLICY_ADMIN_ROLE) returns (uint256) {
        require(dailyLimit > 0, "Daily limit must be positive");
        require(maxGas > 0, "Max gas must be positive");
        require(maxRisk <= 100, "Max risk must be 0-100");
        require(cooldownPeriod <= 86400, "Cooldown must be <= 24 hours");

        _policyCounter++;
        uint256 policyId = _policyCounter;

        policies[policyId] = Policy({
            dailyLimit: dailyLimit,
            maxGas: maxGas,
            maxRisk: maxRisk,
            cooldownPeriod: cooldownPeriod,
            isActive: true,
            createdAt: block.timestamp,
            updatedAt: block.timestamp
        });

        emit PolicyCreated(policyId, dailyLimit, maxGas, maxRisk);
        return policyId;
    }

    /**
     * @dev Update an existing policy
     */
    function updatePolicy(
        uint256 policyId,
        uint256 dailyLimit,
        uint256 maxGas,
        uint256 maxRisk,
        uint256 cooldownPeriod
    ) external onlyRole(POLICY_ADMIN_ROLE) {
        require(
            policyId > 0 && policyId <= _policyCounter,
            "Invalid policy ID"
        );
        require(dailyLimit > 0, "Daily limit must be positive");
        require(maxGas > 0, "Max gas must be positive");
        require(maxRisk <= 100, "Max risk must be 0-100");
        require(cooldownPeriod <= 86400, "Cooldown must be <= 24 hours");

        Policy storage policy = policies[policyId];
        policy.dailyLimit = dailyLimit;
        policy.maxGas = maxGas;
        policy.maxRisk = maxRisk;
        policy.cooldownPeriod = cooldownPeriod;
        policy.updatedAt = block.timestamp;

        emit PolicyUpdated(policyId, dailyLimit, maxGas, maxRisk);
    }

    /**
     * @dev Assign policy to agent
     */
    function assignPolicyToAgent(
        bytes32 agentId,
        uint256 policyId
    ) external onlyRole(POLICY_ADMIN_ROLE) {
        require(registry.isValidAgent(agentId), "Invalid agent");
        require(
            policyId > 0 && policyId <= _policyCounter,
            "Invalid policy ID"
        );
        require(policies[policyId].isActive, "Policy not active");

        agentPolicyIds[agentId] = policyId;
        agentPolicies[agentId] = AgentPolicy({
            agentId: agentId,
            policyId: policyId,
            isActive: true,
            assignedAt: block.timestamp
        });

        emit PolicyAssigned(agentId, policyId, true);
    }

    /**
     * @dev Assign policy to tool
     */
    function assignPolicyToTool(
        bytes32 toolId,
        uint256 policyId
    ) external onlyRole(POLICY_ADMIN_ROLE) {
        require(registry.isValidTool(toolId), "Invalid tool");
        require(
            policyId > 0 && policyId <= _policyCounter,
            "Invalid policy ID"
        );
        require(policies[policyId].isActive, "Policy not active");

        toolPolicyIds[toolId] = policyId;
        toolPolicies[toolId] = ToolPolicy({
            toolId: toolId,
            policyId: policyId,
            isActive: true,
            assignedAt: block.timestamp
        });

        emit PolicyAssigned(toolId, policyId, false);
    }

    /**
     * @dev Revoke policy from agent
     */
    function revokePolicyFromAgent(
        bytes32 agentId
    ) external onlyRole(POLICY_ADMIN_ROLE) {
        require(agentPolicyIds[agentId] != 0, "No policy assigned");

        uint256 policyId = agentPolicyIds[agentId];
        delete agentPolicyIds[agentId];
        delete agentPolicies[agentId];

        emit PolicyRevoked(agentId, policyId, true);
    }

    /**
     * @dev Revoke policy from tool
     */
    function revokePolicyFromTool(
        bytes32 toolId
    ) external onlyRole(POLICY_ADMIN_ROLE) {
        require(toolPolicyIds[toolId] != 0, "No policy assigned");

        uint256 policyId = toolPolicyIds[toolId];
        delete toolPolicyIds[toolId];
        delete toolPolicies[toolId];

        emit PolicyRevoked(toolId, policyId, false);
    }

    /**
     * @dev Check if action is allowed based on policies
     */
    function checkActionAllowed(
        bytes32 agentId,
        bytes32 toolId,
        uint256 gasUsed
    ) external view returns (bool, string memory) {
        // Check if agent and tool are valid
        if (!registry.isValidAgent(agentId)) {
            return (false, "Invalid agent");
        }

        if (!registry.isValidTool(toolId)) {
            return (false, "Invalid tool");
        }

        // Get agent policy
        uint256 agentPolicyId = agentPolicyIds[agentId];
        if (agentPolicyId == 0) {
            agentPolicyId = DEFAULT_POLICY_ID;
        }

        Policy memory agentPolicy = policies[agentPolicyId];
        if (!agentPolicy.isActive) {
            return (false, "Agent policy not active");
        }

        // Get tool policy
        uint256 toolPolicyId = toolPolicyIds[toolId];
        if (toolPolicyId == 0) {
            toolPolicyId = DEFAULT_POLICY_ID;
        }

        Policy memory toolPolicy = policies[toolPolicyId];
        if (!toolPolicy.isActive) {
            return (false, "Tool policy not active");
        }

        // Check gas limits
        if (gasUsed > agentPolicy.maxGas || gasUsed > toolPolicy.maxGas) {
            return (false, "Gas limit exceeded");
        }

        // Check risk levels
        IChroniclerRegistry.Tool memory tool = registry.getTool(toolId);
        if (
            tool.riskLevel > agentPolicy.maxRisk ||
            tool.riskLevel > toolPolicy.maxRisk
        ) {
            return (false, "Risk level exceeded");
        }

        // Check rate limits
        RateLimit memory rateLimit = agentRateLimits[agentId];
        uint256 currentTime = block.timestamp;

        // Reset daily count if 24 hours have passed
        if (currentTime - rateLimit.lastResetTime >= 86400) {
            rateLimit.dailyActionCount = 0;
            rateLimit.lastResetTime = currentTime;
        }

        if (rateLimit.dailyActionCount >= agentPolicy.dailyLimit) {
            return (false, "Daily limit exceeded");
        }

        // Check cooldown
        if (
            currentTime - rateLimit.lastActionTime < agentPolicy.cooldownPeriod
        ) {
            return (false, "Cooldown period not met");
        }

        return (true, "");
    }

    /**
     * @dev Record action for rate limiting
     */
    function recordAction(
        bytes32 agentId,
        uint256 gasUsed
    ) external onlyRole(RATE_LIMITER_ROLE) {
        require(registry.isValidAgent(agentId), "Invalid agent");

        RateLimit storage rateLimit = agentRateLimits[agentId];
        uint256 currentTime = block.timestamp;

        // Reset daily count if 24 hours have passed
        if (currentTime - rateLimit.lastResetTime >= 86400) {
            rateLimit.dailyActionCount = 0;
            rateLimit.lastResetTime = currentTime;
        }

        rateLimit.lastActionTime = currentTime;
        rateLimit.dailyActionCount++;
        rateLimit.totalActions++;
        rateLimit.totalGasUsed += gasUsed;
    }

    /**
     * @dev Get agent rate limit info
     */
    function getAgentRateLimit(
        bytes32 agentId
    ) external view returns (RateLimit memory) {
        return agentRateLimits[agentId];
    }

    /**
     * @dev Get agent policy
     */
    function getAgentPolicy(
        bytes32 agentId
    ) external view returns (AgentPolicy memory) {
        return agentPolicies[agentId];
    }

    /**
     * @dev Get tool policy
     */
    function getToolPolicy(
        bytes32 toolId
    ) external view returns (ToolPolicy memory) {
        return toolPolicies[toolId];
    }

    /**
     * @dev Get policy by ID
     */
    function getPolicy(uint256 policyId) external view returns (Policy memory) {
        require(
            policyId > 0 && policyId <= _policyCounter,
            "Invalid policy ID"
        );
        return policies[policyId];
    }

    /**
     * @dev Get total policy count
     */
    function getPolicyCount() external view returns (uint256) {
        return _policyCounter;
    }

    // ============ INTERNAL FUNCTIONS ============

    function _createDefaultPolicy() private {
        policies[DEFAULT_POLICY_ID] = Policy({
            dailyLimit: 1000,
            maxGas: 500000,
            maxRisk: 50,
            cooldownPeriod: 0,
            isActive: true,
            createdAt: block.timestamp,
            updatedAt: block.timestamp
        });

        _policyCounter++;
    }

    // ============ ADMIN FUNCTIONS ============

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}
