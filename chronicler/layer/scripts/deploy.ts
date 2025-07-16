import { ethers } from "hardhat";

async function main() {
    // Deploy ChroniclerRegistry
    const Registry = await ethers.getContractFactory("ChroniclerRegistry");
    const registry = await Registry.deploy();
    await registry.deployed();
    console.log("ChroniclerRegistry deployed to:", registry.address);

    // Deploy ChroniclerAuditLog
    const AuditLog = await ethers.getContractFactory("ChroniclerAuditLog");
    const auditLog = await AuditLog.deploy(registry.address);
    await auditLog.deployed();
    console.log("ChroniclerAuditLog deployed to:", auditLog.address);

    // Deploy ChroniclerAccessControl
    const AccessControl = await ethers.getContractFactory("ChroniclerAccessControl");
    const accessControl = await AccessControl.deploy(registry.address);
    await accessControl.deployed();
    console.log("ChroniclerAccessControl deployed to:", accessControl.address);
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});
