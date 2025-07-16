import { run } from "hardhat";

async function main() {
    // Replace with actual deployed addresses and constructor arguments
    await run("verify:verify", {
        address: "DEPLOYED_REGISTRY_ADDRESS",
        constructorArguments: [],
    });

    await run("verify:verify", {
        address: "DEPLOYED_AUDITLOG_ADDRESS",
        constructorArguments: ["DEPLOYED_REGISTRY_ADDRESS"],
    });

    await run("verify:verify", {
        address: "DEPLOYED_ACCESSCONTROL_ADDRESS",
        constructorArguments: ["DEPLOYED_REGISTRY_ADDRESS"],
    });
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});
