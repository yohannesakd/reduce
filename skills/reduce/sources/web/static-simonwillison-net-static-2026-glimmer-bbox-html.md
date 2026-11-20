# glimmer-bbox.html, the page that the model wrote

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Simon Willison
- Original location: https://static.simonwillison.net/static/2026/glimmer-bbox.html
- Copied: 2026-11-20, from the HTML source of the page

## Text
````html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BBox Overlay 0-1000</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 24px; background:#f5f5f5; }
  .controls { display:grid; gap:12px; max-width:900px; margin-bottom:20px; }
  input, textarea, button { font-size:14px; padding:8px; }
  textarea { min-height:120px; font-family:monospace; }
  #container { position:relative; display:inline-block; max-width:100%; background:#000; }
  #container img { display:block; max-width:100%; height:auto; }
  .box {
    position:absolute;
    border:2px solid #ff3b30;
    background:rgba(255,59,48,0.15);
    pointer-events:none;
  }
  .label {
    position:absolute;
    top:-22px; left:0;
    background:#ff3b30;
    color:white;
    font-size:12px;
    padding:2px 6px;
    border-radius:3px;
    white-space:nowrap;
  }
</style>
</head>
<body>
<h2>BBox Overlay from 0-1000 coords</h2>

<div class="controls">
  <label>Image URL
    <input id="imgUrl" type="text" size="80" placeholder="https://.../image.jpg" style="width:100%">
  </label>
  <label>JSON annotations
    <textarea id="jsonInput">[
  {"bbox_2d": [195, 290, 370, 780], "label": "pelicans"},
  {"bbox_2d": [445, 320, 675, 850], "label": "pelicans"}
]</textarea>
  </label>
  <button id="loadBtn">Load & Render</button>
</div>

<div id="container"></div>

<script>
const imgUrlInput = document.getElementById('imgUrl');
const jsonInput = document.getElementById('jsonInput');
const loadBtn = document.getElementById('loadBtn');
const container = document.getElementById('container');

loadBtn.addEventListener('click', () => {
  const url = imgUrlInput.value.trim();
  if(!url){ alert('Enter image URL'); return; }
  let data;
  try { data = JSON.parse(jsonInput.value); } 
  catch(e){ alert('Invalid JSON'); return; }

  container.innerHTML = '';
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = url;

  container.appendChild(img);

  img.onload = () => {
    // wait for layout to get rendered size
    requestAnimationFrame(() => {
      const w = img.clientWidth;
      const h = img.clientHeight;
      if(w===0 || h===0) return;

      data.forEach(item => {
        const bbox = item.bbox_2d;
        if(!Array.isArray(bbox) || bbox.length !==4) return;
        const [x1, y1, x2, y2] = bbox.map(v => Number(v));
        const left   = x1/1000 * w;
        const top    = y1/1000 * h;
        const width  = (x2 - x1)/1000 * w;
        const height = (y2 - y1)/1000 * h;

        const box = document.createElement('div');
        box.className = 'box';
        box.style.left = left + 'px';
        box.style.top  = top + 'px';
        box.style.width = width + 'px';
        box.style.height = height + 'px';

        const label = document.createElement('div');
        label.className = 'label';
        label.textContent = item.label || '';
        box.appendChild(label);

        container.appendChild(box);
      });
    });
  };

  img.onerror = () => alert('Could not load image. Check URL / CORS.');
});
</script>
</body>
</html>


````
