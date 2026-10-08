#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const pyScript = path.join(__dirname, '..', 'ngelaprak', 'cli.py');
const args = process.argv.slice(2);

const py = spawn('python', [pyScript, ...args], { stdio: 'inherit' });
py.on('close', (code) => {
    process.exit(code);
});
