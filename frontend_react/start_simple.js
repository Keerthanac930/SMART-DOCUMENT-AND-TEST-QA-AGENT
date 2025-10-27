#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting QA Agent Frontend...');
console.log('=' * 50);

// Check if node_modules exists
const nodeModulesPath = path.join(__dirname, 'node_modules');
const fs = require('fs');

if (!fs.existsSync(nodeModulesPath)) {
    console.log('📦 Installing dependencies...');
    const install = spawn('npm', ['install'], { 
        stdio: 'inherit',
        shell: true,
        cwd: __dirname
    });
    
    install.on('close', (code) => {
        if (code === 0) {
            console.log('✅ Dependencies installed successfully!');
            startDevServer();
        } else {
            console.log('❌ Failed to install dependencies');
            process.exit(1);
        }
    });
} else {
    startDevServer();
}

function startDevServer() {
    console.log('🎨 Starting development server...');
    console.log('📱 Frontend will be available at: http://localhost:3000');
    console.log('=' * 50);
    
    const dev = spawn('npm', ['run', 'dev'], { 
        stdio: 'inherit',
        shell: true,
        cwd: __dirname
    });
    
    dev.on('close', (code) => {
        console.log(`Frontend server exited with code ${code}`);
    });
    
    // Handle Ctrl+C
    process.on('SIGINT', () => {
        console.log('\n👋 Stopping frontend server...');
        dev.kill('SIGINT');
        process.exit(0);
    });
}
