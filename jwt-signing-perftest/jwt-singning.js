const jwt = require('jsonwebtoken');
const fs = require('fs');
const { performance } = require('perf_hooks');

function generateJWT(iterations, verbose) {
  const privateKey = fs.readFileSync('private.key', 'utf8');
  const payload = {
    sub: '1234567890',
    name: 'John Doe',
    // Add more claims as needed
  };
  const options = {
    algorithm: 'RS256',
    expiresIn: '1h',
  };

  let totalExecutionTime = 0;

  for (let i = 1; i <= iterations; i++) {
    const start = performance.now();
    const token = jwt.sign(payload, privateKey, options);
    const end = performance.now();
    const executionTime = end - start;

    totalExecutionTime += executionTime;

    if (verbose) {
      console.log('Generated JWT token:', token);
      console.log('Execution time:', executionTime.toFixed(2), 'ms');
      console.log('---');
    }
  }

  const averageExecutionTime = totalExecutionTime / iterations;
  console.log('Average execution time:', averageExecutionTime.toFixed(2), 'ms');
}

const iterations = process.argv[2] ? parseInt(process.argv[2]) : 1;
const verbose = process.argv.includes('--verbose');
generateJWT(iterations, verbose);

