import { execSync } from "child_process";

try {
    execSync("npx hardhat compile", { stdio: "inherit" });
    console.log("Contracts compiled successfully.");
} catch (error) {
    console.error("Compilation failed:", error);
    process.exit(1);
}
