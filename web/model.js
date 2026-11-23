// Keras channels-last tensors, with kernels ordered by row, column, input, output.
const weights = new Float32Array(Uint8Array.from(atob(encodedWeights), c => c.charCodeAt(0)).buffer);
let offset = 0;
function take(count) {
  const values = weights.subarray(offset, offset + count);
  offset += count;
  return values;
}
const kernel1 = take(3 * 3 * 32), bias1 = take(32);
const kernel2 = take(3 * 3 * 32 * 64), bias2 = take(64);
const dense = take(1600 * 10), bias3 = take(10);

function convolveAndPool(input, side, channels, kernel, bias) {
  const filters = bias.length;
  const pooledSide = Math.floor((side - 2) / 2);
  const pooled = new Float32Array(pooledSide * pooledSide * filters);
  const sums = new Float32Array(filters);
  for (let y = 0; y < pooledSide * 2; y++) {
    for (let x = 0; x < pooledSide * 2; x++) {
      sums.set(bias);
      let k = 0;
      for (let dy = 0; dy < 3; dy++) {
        let i = ((y + dy) * side + x) * channels;
        for (let j = 0; j < 3 * channels; j++, i++) {
          const value = input[i];
          if (value) {
            for (let f = 0; f < filters; f++) sums[f] += value * kernel[k + f];
          }
          k += filters;
        }
      }
      const dst = ((y >> 1) * pooledSide + (x >> 1)) * filters;
      for (let f = 0; f < filters; f++) pooled[dst + f] = Math.max(pooled[dst + f], sums[f]);
    }
  }
  return pooled;
}

function predict(input) {
  const first = convolveAndPool(input, 28, 1, kernel1, bias1);
  const second = convolveAndPool(first, 13, 32, kernel2, bias2);
  const logits = Array.from(bias3);
  for (let i = 0; i < second.length; i++) {
    for (let d = 0; d < 10; d++) logits[d] += second[i] * dense[i * 10 + d];
  }
  const max = Math.max(...logits);
  const scores = logits.map(x => Math.exp(x - max));
  const total = scores.reduce((a, b) => a + b);
  return scores.map(x => x / total);
}
