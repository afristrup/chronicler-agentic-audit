// Test setup file for Jest

// Mock environment variables
process.env.SUPABASE_URL = 'https://test.supabase.co';
process.env.SUPABASE_KEY = 'test-key';
process.env.IPFS_GATEWAY = 'https://ipfs.io';
process.env.DASHBOARD_PORT = '3000';
process.env.CHAIN_ID = '1';
process.env.RPC_URL = 'http://localhost:8545';
process.env.REGISTRY_ADDRESS = '0x1234567890123456789012345678901234567890';
process.env.AUDIT_LOG_ADDRESS = '0x2345678901234567890123456789012345678901';
process.env.ACCESS_CONTROL_ADDRESS = '0x3456789012345678901234567890123456789012';

// Global test timeout
jest.setTimeout(30000);

// Mock console methods to reduce noise in tests
global.console = {
    ...console,
    log: jest.fn(),
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
};