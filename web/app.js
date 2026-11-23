const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d", {willReadFrequently:true});
const empty = document.querySelector("#empty");
const results = document.querySelector("#results");
const rows = Array.from({length:3}, () => {
  const row = document.createElement("div");
  row.className = "row";
  row.innerHTML = '<b></b><div class="track"><div class="fill"></div></div><span></span>';
  results.append(row);
  return row;
});
const sample = document.createElement("canvas");
sample.width = sample.height = 28;
const small = sample.getContext("2d", {willReadFrequently:true});
let pointer = null, previous, bounds, frame;
function render() {
  frame = null;
  const {left, top, right, bottom} = bounds;
  const width = right - left, height = bottom - top;
  const scale = 20 / Math.max(width, height);
  small.clearRect(0, 0, 28, 28);
  small.drawImage(canvas, left, top, width, height, (28-width*scale)/2, (28-height*scale)/2, width*scale, height*scale);
  const pixels = small.getImageData(0,0,28,28).data;
  const input = Float32Array.from({length:784}, (_, i) => pixels[4*i+3] / 255);
  const ranked = predict(input).map((p,d) => ({p,d})).sort((a,b) => b.p-a.p);
  rows.forEach((row,i) => {
    const {p,d} = ranked[i];
    row.firstChild.textContent = d;
    row.querySelector(".fill").style.width = p*100 + "%";
    row.lastChild.textContent = (p*100).toLocaleString("ru", {maximumFractionDigits:1}) + "%";
  });
  empty.hidden = true;
  results.hidden = false;
}
function stroke(event) {
  const box = canvas.getBoundingClientRect();
  const x = Math.max(0, Math.min(280,(event.clientX-box.left)*280/box.width));
  const y = Math.max(0, Math.min(280,(event.clientY-box.top)*280/box.height));
  const radius = 9;
  ctx.strokeStyle = ctx.fillStyle = "#253d34";
  ctx.lineWidth = radius*2;
  ctx.lineCap = "round";
  ctx.beginPath();
  if (previous) {
    ctx.moveTo(previous.x, previous.y);
    ctx.lineTo(x,y);
    ctx.stroke();
  } else {
    ctx.arc(x,y,radius,0,2*Math.PI);
    ctx.fill();
  }
  previous = {x,y};
  bounds.left = Math.max(0, Math.min(bounds.left,x-radius));
  bounds.right = Math.min(280, Math.max(bounds.right,x+radius));
  bounds.top = Math.max(0, Math.min(bounds.top,y-radius));
  bounds.bottom = Math.min(280, Math.max(bounds.bottom,y+radius));
  if (frame == null) frame = requestAnimationFrame(render);
}
function clear() {
  if (frame != null) cancelAnimationFrame(frame);
  pointer = previous = frame = null;
  bounds = {left:280,top:280,right:0,bottom:0};
  ctx.clearRect(0,0,280,280);
  empty.hidden = false;
  results.hidden = true;
}
canvas.onpointerdown = e => {
  if (pointer !== null || e.button !== 0) return;
  pointer = e.pointerId;
  canvas.setPointerCapture(pointer);
  stroke(e);
};
canvas.onpointermove = e => { if (e.pointerId === pointer) stroke(e); };
canvas.onlostpointercapture = () => { pointer = previous = null; };
document.querySelector("button").onclick = clear;
clear();
